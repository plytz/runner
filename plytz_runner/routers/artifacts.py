from fastapi import APIRouter

from ..dependencies import WORKDIR
from ..services import artifacts as artifacts_service


router = APIRouter(
    prefix="/artifacts",
    tags=["artifacts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def artifacts():
    return await artifacts_service.list_artifacts()

@router.get("/{artifact_id}")
async def artifact(artifact_id: str):
    return await artifacts_service.get_artifact(artifact_id)

@router.get("/{artifact_id}/events")
async def artifact_events(artifact_id: str):
    return await artifacts_service.get_artifact_events(artifact_id)

