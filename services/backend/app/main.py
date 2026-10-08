from __future__ import annotations

import logging
import random

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse

from ttod_core.proposals import create_proposal
from ttod_core.repository import ProposalStore

from .auth import AccessTokenClaims, AuthService, RequireAccessToken, RequireSession, SessionClaims
from .config import Settings
from .favorites import add_favorite, get_favorites, remove_favorite
from .models import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthUser,
    FavoriteRequest,
    OracleProposeRequest,
    OracleQueryPayload,
    ProposalCreated,
    ProposalRequest,
    TokenResponse,
)
from .oracle import OracleService
from .storage import SnapshotService


logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None, oracle: OracleService | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
    oracle = oracle or OracleService(settings, snapshots)
    auth_service = AuthService(
        settings.session_secret,
        settings.session_ttl_seconds,
        settings.admin_email,
        settings.admin_password_hash,
        settings.pat_secret,
        settings.pat_ttl_seconds,
    )
    require_session = RequireSession(auth_service)
    require_access_token = RequireAccessToken(auth_service)
    app = FastAPI(title="TTOD Oracle Backend", version="1.0.0")

    @app.get("/health")
    def health():
        try:
            return snapshots.health()
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"TTOD repository unavailable: {exc}") from exc

    @app.get("/api/v1/schema/definitions")
    def definitions():
        return snapshots.definitions()

    @app.get("/api/v1/wisdom/sample")
    def wisdom_sample():
        return snapshots.wisdom()

    @app.post("/api/v1/auth/login", response_model=AuthLoginResponse)
    def login(payload: AuthLoginRequest):
        claims = auth_service.authenticate(payload.email, payload.password)
        if claims is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return AuthLoginResponse(
            session_token=auth_service.issue_session(claims),
            expires_in=auth_service.session_ttl_seconds,
            user=AuthUser(id=claims.user_id, email=claims.email, roles=list(claims.roles)),
        )

    @app.get("/api/v1/auth/session", response_model=AuthUser)
    def auth_session(claims: SessionClaims = Depends(require_session)):
        return AuthUser(id=claims.user_id, email=claims.email, roles=list(claims.roles))

    @app.post("/api/v1/auth/token", response_model=TokenResponse)
    def issue_access_token(claims: SessionClaims = Depends(require_session)):
        return TokenResponse(
            access_token=auth_service.issue_pat(claims.user_id),
            expires_in=auth_service.pat_ttl_seconds,
        )

    @app.get("/api/v1/wisdom/random")
    def wisdom_random(_claims: AccessTokenClaims = Depends(require_access_token)):
        quotes = snapshots.wisdom()
        if not quotes:
            raise HTTPException(status_code=404, detail="No public wisdom available")
        return random.choice(quotes)

    @app.get("/api/v1/graph")
    def graph():
        return Response(content=snapshots.graph_bytes(), media_type="application/json")

    @app.post("/api/v1/oracle/stream")
    def oracle_stream(payload: OracleQueryPayload):
        return StreamingResponse(oracle.stream(payload), media_type="text/event-stream")

    @app.post("/api/v1/oracle/propose", status_code=201)
    async def oracle_propose(payload: OracleProposeRequest):
        return await oracle.propose(payload)

    # El usuario de cada favorito sale siempre de la sesión, nunca del cuerpo de la petición.
    @app.post("/api/v1/favorites", status_code=201)
    def create_favorite(payload: FavoriteRequest, claims: SessionClaims = Depends(require_session)):
        return add_favorite(claims.user_id, payload.quoteId)

    @app.get("/api/v1/favorites")
    def list_favorites(claims: SessionClaims = Depends(require_session)):
        return get_favorites(claims.user_id)

    @app.delete("/api/v1/favorites/{quote_id}", status_code=204)
    def delete_favorite(quote_id: str, claims: SessionClaims = Depends(require_session)):
        if not remove_favorite(claims.user_id, quote_id):
            raise HTTPException(status_code=404, detail="Favorite not found")
        return Response(status_code=204)

    @app.post("/api/v1/proposals", status_code=201, response_model=ProposalCreated)
    def create_user_proposal(
        payload: ProposalRequest,
        claims: SessionClaims = Depends(require_session),
    ):
        # `origin` y el autor los fija el servidor: el cliente no puede declarar otra procedencia.
        candidate = {
            "text": payload.text,
            "section": payload.section,
            "level": payload.level,
            "origin": "human",
            "lang": payload.lang,
        }
        if payload.source is not None:
            candidate["source"] = payload.source
        if payload.tags:
            candidate["tags"] = payload.tags
        if payload.teaches is not None:
            candidate["teaches"] = payload.teaches

        try:
            proposal = create_proposal(
                candidate_content=candidate,
                proposer_kind="human",
                proposer_id=claims.user_id,
                generation_method="api-proposal-create",
            )
            ProposalStore(settings.proposal_dir).save(proposal)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except OSError as exc:
            logger.exception("Unable to persist proposal")
            raise HTTPException(status_code=500, detail="Unable to save proposal") from exc

        return ProposalCreated(proposal_id=proposal.proposal_id, status=proposal.status.value)

    # La cola solo la ve quien revisa: el rol se comprueba en el servidor, no ocultando la vista.
    @app.get("/api/v1/proposals")
    def list_proposals(claims: SessionClaims = Depends(require_session)):
        if not {"reviewer", "instructor"}.intersection(claims.roles):
            raise HTTPException(status_code=403, detail="Reviewer role required")
        return [proposal.to_dict() for proposal in ProposalStore(settings.proposal_dir).list()]

    return app


app = create_app()

