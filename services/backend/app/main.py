from __future__ import annotations

import json
import random

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field

from ttod_core.proposals import create_proposal
from ttod_core.repository import ProposalStore

from .config import Settings
from .auth import AccessTokenClaims, AuthService, RequireAccessToken
from .models import OracleProposeRequest, OracleQueryPayload, ProposalRequest, TokenResponse
from .oracle import OracleService
from .favorites import add_favorite, get_favorites, remove_favorite
from .storage import SnapshotService


class FavoriteRequest(BaseModel):
    quoteId: str = Field(min_length=1)


def require_session_user(
    authorization: str | None = Header(default=None),
    ttod_session: str | None = Cookie(default=None),
) -> str:
    """Resolve the authenticated user from the session boundary."""
    raw = ttod_session.strip() if ttod_session and ttod_session.strip() else None
    if raw is None and authorization and authorization.startswith("Bearer "):
        raw = authorization.removeprefix("Bearer ").strip()
    if raw:
        try:
            claims = json.loads(raw)
            user_id = claims.get("userId")
            if isinstance(user_id, str) and user_id.strip():
                return user_id.strip()
        except json.JSONDecodeError:
            return raw
    raise HTTPException(status_code=401, detail="Authentication required")


def require_reviewer_session(
    authorization: str | None = Header(default=None),
    ttod_session: str | None = Cookie(default=None),
) -> str:
    user_id = require_session_user(authorization, ttod_session)
    raw = ttod_session.strip() if ttod_session and ttod_session.strip() else authorization.removeprefix("Bearer ").strip() if authorization and authorization.startswith("Bearer ") else ""
    try:
        roles = json.loads(raw).get("roles", [])
    except json.JSONDecodeError:
        roles = []
    if not isinstance(roles, list) or not {"reviewer", "instructor"}.intersection(roles):
        raise HTTPException(status_code=403, detail="Reviewer role required")
    return user_id


def require_session_cookie_user(ttod_session: str | None = Cookie(default=None)) -> str:
    return require_session_user(authorization=None, ttod_session=ttod_session)


def create_app(settings: Settings | None = None, oracle: OracleService | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
    oracle = oracle or OracleService(settings, snapshots)
    auth_service = AuthService(settings.pat_secret, settings.pat_ttl_seconds)
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
    def issue_access_token(user_id: str = Depends(require_session_cookie_user)):
        return TokenResponse(
            access_token=auth_service.issue_pat(user_id),
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
    async def oracle_propose(payload: OracleProposeRequest, _user_id: str = Depends(require_session_user)):
        return await oracle.propose(payload)

    @app.post("/api/v1/proposals", status_code=201)
    def create_user_proposal(
        payload: ProposalRequest,
        user_id: str = Depends(require_session_user),
    ):
        candidate = {
            "text": payload.text,
            "section": payload.section,
            "level": payload.level,
            "origin": payload.origin,
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
            path = ProposalStore(settings.proposal_dir).save(proposal)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Unable to save proposal") from exc

        result = proposal.to_dict()
        result["stored_at"] = str(path)
        return result

    @app.get("/api/v1/proposals")
    def list_proposals(_user_id: str = Depends(require_reviewer_session)):
        return [proposal.to_dict() for proposal in ProposalStore(settings.proposal_dir).list()]

    @app.post("/api/v1/favorites", status_code=201)
    def create_favorite(payload: FavoriteRequest, user_id: str = Depends(require_session_user)):
        return add_favorite(user_id, payload.quoteId)

    @app.get("/api/v1/favorites")
    def list_favorites(user_id: str = Depends(require_session_user)):
        return get_favorites(user_id)

    @app.delete("/api/v1/favorites/{quote_id}")
    def delete_favorite(quote_id: str, user_id: str = Depends(require_session_user)):
        if not remove_favorite(user_id, quote_id):
            raise HTTPException(status_code=404, detail="Favorite not found")
        return Response(status_code=204)

    return app


app = create_app()

