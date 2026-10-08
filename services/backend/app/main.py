from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse
from ttod_core.proposals import create_proposal
from ttod_core.repository import ProposalStore

from .config import Settings
from .auth import require_reviewer_session, require_session_user
from .models import OracleProposeRequest, OracleQueryPayload, ProposalRequest
from .oracle import OracleService
from .storage import SnapshotService

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

    return app


app = create_app()

