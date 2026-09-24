from __future__ import annotations

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field

from .config import Settings
from .models import OracleProposeRequest, OracleQueryPayload
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
    if ttod_session and ttod_session.strip():
        return ttod_session.strip()
    if authorization and authorization.startswith("Bearer "):
        user_id = authorization.removeprefix("Bearer ").strip()
        if user_id:
            return user_id
    raise HTTPException(status_code=401, detail="Authentication required")


def create_app(settings: Settings | None = None, oracle: OracleService | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
    oracle = oracle or OracleService(settings, snapshots)
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

    @app.get("/api/v1/graph")
    def graph():
        return Response(content=snapshots.graph_bytes(), media_type="application/json")

    @app.post("/api/v1/oracle/stream")
    def oracle_stream(payload: OracleQueryPayload):
        return StreamingResponse(oracle.stream(payload), media_type="text/event-stream")

    @app.post("/api/v1/oracle/propose", status_code=201)
    async def oracle_propose(payload: OracleProposeRequest):
        return await oracle.propose(payload)

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

