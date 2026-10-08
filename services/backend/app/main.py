from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse

from .auth import AuthService, RequireSession, SessionClaims
from .config import Settings
from .models import AuthLoginRequest, AuthLoginResponse, AuthUser, OracleProposeRequest, OracleQueryPayload
from .oracle import OracleService
from .storage import SnapshotService


def create_app(settings: Settings | None = None, oracle: OracleService | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
    oracle = oracle or OracleService(settings, snapshots)
    auth_service = AuthService(
        settings.session_secret,
        settings.session_ttl_seconds,
        settings.admin_email,
        settings.admin_password_hash,
    )
    require_session = RequireSession(auth_service)
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

    @app.get("/api/v1/graph")
    def graph():
        return Response(content=snapshots.graph_bytes(), media_type="application/json")

    @app.post("/api/v1/oracle/stream")
    def oracle_stream(payload: OracleQueryPayload):
        return StreamingResponse(oracle.stream(payload), media_type="text/event-stream")

    @app.post("/api/v1/oracle/propose", status_code=201)
    async def oracle_propose(payload: OracleProposeRequest):
        return await oracle.propose(payload)

    return app


app = create_app()

