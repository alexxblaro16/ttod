from __future__ import annotations

import logging
import random

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field

from ttod_core.proposals import create_proposal
from ttod_core.repository import ProposalStore

from .config import Settings
from .auth import AccessTokenClaims, AuthService, RequireAccessToken, RequireSession
from .models import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthUser,
    OracleProposeRequest,
    OracleQueryPayload,
    ProposalRequest,
    TokenResponse,
)
from .oracle import OracleService
from .favorites import add_favorite, get_favorites, remove_favorite
from .storage import SnapshotService


logger = logging.getLogger(__name__)


class FavoriteRequest(BaseModel):
    quoteId: str = Field(min_length=1)


def create_app(settings: Settings | None = None, oracle: OracleService | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
    oracle = oracle or OracleService(settings, snapshots)
    auth_service = AuthService(
        settings.pat_secret,
        settings.pat_ttl_seconds,
        settings.admin_email,
        settings.admin_password_hash,
        settings.session_ttl_seconds,
    )
    require_session = RequireSession(auth_service)
    require_session_cookie = RequireSession(auth_service, cookie_only=True)
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

    @app.post("/api/v1/auth/token", response_model=TokenResponse)
    def issue_access_token(claims: AccessTokenClaims = Depends(require_session_cookie)):
        return TokenResponse(
            access_token=auth_service.issue_pat(claims.user_id, claims.role, claims.email),
            expires_in=auth_service.pat_ttl_seconds,
        )

    @app.post("/api/v1/auth/login", response_model=AuthLoginResponse)
    def login(payload: AuthLoginRequest):
        user = auth_service.authenticate_admin(payload.email, payload.password)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return AuthLoginResponse(
            session_token=auth_service.issue_session(
                user.user_id,
                user.role,
                user.email,
                user.roles,
            ),
            expires_in=auth_service.session_ttl_seconds,
            user=AuthUser(
                id=user.user_id,
                email=user.email,
                role="admin",
                roles=list(user.roles),
            ),
        )

    @app.get("/api/v1/auth/session", response_model=AuthUser)
    def auth_session(claims: AccessTokenClaims = Depends(require_session)):
        if claims.role not in {"admin", "user"} or not claims.email.strip():
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        return AuthUser(
            id=claims.user_id,
            email=claims.email,
            role=claims.role,
            roles=list(claims.roles),
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
    async def oracle_propose(
        payload: OracleProposeRequest,
        claims: AccessTokenClaims = Depends(require_session),
    ):
        return await oracle.propose(payload)

    @app.post("/api/v1/proposals", status_code=201)
    def create_user_proposal(
        payload: ProposalRequest,
        claims: AccessTokenClaims = Depends(require_session),
    ):
        user_id = claims.user_id
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
                proposer_id=user_id,
                generation_method="api-proposal-create",
            )
            ProposalStore(settings.proposal_dir).save(proposal)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except OSError as exc:
            logger.exception("Unable to persist proposal")
            raise HTTPException(status_code=500, detail="Unable to save proposal") from exc

        return proposal.to_dict()

    @app.get("/api/v1/proposals")
    def list_proposals(claims: AccessTokenClaims = Depends(require_session)):
        if not {"reviewer", "instructor"}.intersection(claims.roles):
            raise HTTPException(status_code=403, detail="Reviewer role required")
        return [proposal.to_dict() for proposal in ProposalStore(settings.proposal_dir).list()]

    @app.post("/api/v1/favorites", status_code=201)
    def create_favorite(
        payload: FavoriteRequest,
        claims: AccessTokenClaims = Depends(require_session),
    ):
        return add_favorite(claims.user_id, payload.quoteId)

    @app.get("/api/v1/favorites")
    def list_favorites(claims: AccessTokenClaims = Depends(require_session)):
        return get_favorites(claims.user_id)

    @app.delete("/api/v1/favorites/{quote_id}")
    def delete_favorite(
        quote_id: str,
        claims: AccessTokenClaims = Depends(require_session),
    ):
        if not remove_favorite(claims.user_id, quote_id):
            raise HTTPException(status_code=404, detail="Favorite not found")
        return Response(status_code=204)

    return app


app = create_app()
