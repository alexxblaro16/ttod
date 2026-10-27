from __future__ import annotations

import hashlib
import logging
import random
from contextlib import asynccontextmanager
from typing import Any

import redis
from fastapi import Cookie, Depends, FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response, StreamingResponse

from ttod_core.proposals import create_proposal

from .auth import (
    SESSION_COOKIE_NAME,
    AccessTokenClaims,
    AuthService,
    RequireAccessToken,
    RequireSession,
    SessionClaims,
)
from .config import Settings
from .favorites import FavoriteStore, MemoryFavoriteStore, RedisFavoriteStore
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
from .proposal_drafts import DualWriteProposalDraftStore, FilesystemProposalDraftStore, ProposalDraftStore
from .redis_client import create_redis_client, redis_ping
from .sessions import MemorySessionStore, RedisSessionStore, SessionStore
from .storage import SnapshotService
from .users import MemoryUserStore, RedisUserStore, UserStore


logger = logging.getLogger(__name__)


def _build_shore(
    settings: Settings,
    *,
    redis_client: Any | None = None,
    users: UserStore | None = None,
    sessions: SessionStore | None = None,
    favorites: FavoriteStore | None = None,
    proposals: ProposalDraftStore | None = None,
) -> tuple[Any | None, UserStore, SessionStore, FavoriteStore, ProposalDraftStore]:
    client = redis_client
    if client is None and settings.redis_url.strip():
        client = create_redis_client(settings.redis_url)

    if users is None:
        users = RedisUserStore(client=client) if client is not None else MemoryUserStore()
    if sessions is None:
        sessions = RedisSessionStore(client=client) if client is not None else MemorySessionStore()
    if favorites is None:
        favorites = (
            RedisFavoriteStore(settings.redis_url, client=client)
            if client is not None
            else MemoryFavoriteStore()
        )
    if proposals is None:
        proposals = (
            DualWriteProposalDraftStore(settings.proposal_dir, client=client)
            if client is not None
            else FilesystemProposalDraftStore(settings.proposal_dir)
        )
    return client, users, sessions, favorites, proposals


def create_app(
    settings: Settings | None = None,
    oracle: OracleService | None = None,
    favorites: FavoriteStore | None = None,
    *,
    users: UserStore | None = None,
    sessions: SessionStore | None = None,
    proposals: ProposalDraftStore | None = None,
    redis_client: Any | None = None,
) -> FastAPI:
    settings = settings or Settings.from_env()
    snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
    oracle = oracle or OracleService(settings, snapshots)
    shore_client, users, sessions, favorites, proposals = _build_shore(
        settings,
        redis_client=redis_client,
        users=users,
        sessions=sessions,
        favorites=favorites,
        proposals=proposals,
    )
    auth_service = AuthService(
        settings.session_secret,
        settings.session_ttl_seconds,
        settings.admin_email,
        settings.admin_password_hash,
        settings.pat_secret,
        settings.pat_ttl_seconds,
        users=users,
        sessions=sessions,
    )
    require_session = RequireSession(auth_service)
    require_access_token = RequireAccessToken(auth_service)
    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        # El primer `ttod.yml` se lee al arrancar y no en la primera visita: cargarlo y
        # validarlo cuesta ~1 s, y sin esto lo pagaba quien abriese la portada primero.
        # Si falla, el backend arranca igual y la primera petición lo vuelve a intentar.
        try:
            await run_in_threadpool(snapshots.wisdom)
        except Exception:  # noqa: BLE001
            logging.getLogger(__name__).warning("No se pudo precargar ttod.yml al arrancar", exc_info=True)
        yield

    app = FastAPI(title="TTOD Oracle Backend", version="1.0.0", lifespan=lifespan)

    @app.get("/health")
    def health():
        try:
            payload = snapshots.health()
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"TTOD repository unavailable: {exc}") from exc
        if settings.redis_url.strip() or shore_client is not None:
            payload = {
                **payload,
                "redis": "ok" if shore_client is not None and redis_ping(shore_client) else "down",
            }
        return payload

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
        try:
            session_token = auth_service.issue_session(claims)
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Session store unavailable") from exc
        return AuthLoginResponse(
            session_token=session_token,
            expires_in=auth_service.session_ttl_seconds,
            user=AuthUser(id=claims.user_id, email=claims.email, roles=list(claims.roles)),
        )

    @app.get("/api/v1/auth/session", response_model=AuthUser)
    def auth_session(claims: SessionClaims = Depends(require_session)):
        return AuthUser(id=claims.user_id, email=claims.email, roles=list(claims.roles))

    @app.post("/api/v1/auth/logout", status_code=204)
    def logout(
        session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    ):
        try:
            auth_service.revoke_session(session_token or "")
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Session store unavailable") from exc
        return Response(status_code=204)

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
    def graph(request: Request):
        body = snapshots.graph_bytes()
        # ETag del cuerpo: quien ya lo tiene recibe un 304 vacío en vez de 138 KB.
        # Un minuto de vida (más diez de margen sirviendo el viejo mientras se revalida)
        # deja que Caddy o un CDN lo sirvan sin despertar al backend.
        etag = f'"{hashlib.sha256(body).hexdigest()[:32]}"'
        headers = {"ETag": etag, "Cache-Control": "public, max-age=60, stale-while-revalidate=600"}
        if etag in request.headers.get("if-none-match", ""):
            return Response(status_code=304, headers=headers)
        return Response(content=body, media_type="application/json", headers=headers)

    @app.post("/api/v1/oracle/stream")
    def oracle_stream(payload: OracleQueryPayload):
        return StreamingResponse(oracle.stream(payload), media_type="text/event-stream")

    @app.post("/api/v1/oracle/propose", status_code=201)
    async def oracle_propose(payload: OracleProposeRequest):
        return await oracle.propose(payload)

    # El usuario de cada favorito sale siempre de la sesión, nunca del cuerpo de la petición.
    @app.post("/api/v1/favorites", status_code=201)
    def create_favorite(payload: FavoriteRequest, claims: SessionClaims = Depends(require_session)):
        if not any(entry["id"] == payload.quoteId for entry in snapshots.wisdom()):
            raise HTTPException(status_code=404, detail="Quote not found or not publicly active")
        try:
            return favorites.save(claims.user_id, payload.quoteId)
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Favorites store unavailable") from exc

    @app.get("/api/v1/favorites")
    def list_favorites(claims: SessionClaims = Depends(require_session)):
        try:
            entries = favorites.list(claims.user_id)
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Favorites store unavailable") from exc
        # Una cita retirada del corpus público deja de aparecer aunque siga guardada.
        active_ids = {entry["id"] for entry in snapshots.wisdom()}
        return [entry for entry in entries if entry["quoteId"] in active_ids]

    @app.delete("/api/v1/favorites/{quote_id}", status_code=204)
    def delete_favorite(quote_id: str, claims: SessionClaims = Depends(require_session)):
        try:
            removed = favorites.remove(claims.user_id, quote_id)
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Favorites store unavailable") from exc
        if not removed:
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
            proposals.save(proposal)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Proposal store unavailable") from exc
        except OSError as exc:
            logger.exception("Unable to persist proposal")
            raise HTTPException(status_code=500, detail="Unable to save proposal") from exc

        return ProposalCreated(proposal_id=proposal.proposal_id, status=proposal.status.value)

    # La cola solo la ve quien revisa: el rol se comprueba en el servidor, no ocultando la vista.
    @app.get("/api/v1/proposals")
    def list_proposals(claims: SessionClaims = Depends(require_session)):
        if not {"reviewer", "instructor"}.intersection(claims.roles):
            raise HTTPException(status_code=403, detail="Reviewer role required")
        try:
            return [proposal.to_dict() for proposal in proposals.list()]
        except redis.RedisError as exc:
            raise HTTPException(status_code=503, detail="Proposal store unavailable") from exc

    return app


app = create_app()
