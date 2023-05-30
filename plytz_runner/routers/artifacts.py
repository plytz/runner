import os
import aiofiles
import json

from aiofiles.os import scandir
from fastapi import APIRouter, HTTPException

from ..dependencies import WORKDIR
from ..models.artifact import Artifact


ARTIFACTS_DIR = os.path.join(WORKDIR, "artifacts")

router = APIRouter(
    prefix="/artifacts",
    tags=["artifacts"],
    responses={404: {"description": "Not found"}},
)

def check_if_artifact_exists(artifact_id: str):
    if not os.path.isdir(f"{ARTIFACTS_DIR}/{artifact_id}"):
        raise HTTPException(status_code=404, detail="Artifact not found")

async def get_artifact(artifact_id: str):
    check_if_artifact_exists(artifact_id)

    async with aiofiles.open(f"{ARTIFACTS_DIR}/{artifact_id}/status", mode="r") as f:
        status = await f.read()
    async with aiofiles.open(f"{ARTIFACTS_DIR}/{artifact_id}/rc", mode="r") as f:
        rc = int(await f.read())
    return Artifact(id=artifact_id, rc=rc, status=status)

async def get_artifact_events(artifact_id: str):
    check_if_artifact_exists(artifact_id)

    events = []
    entries = await scandir(f"{ARTIFACTS_DIR}/{artifact_id}/job_events")
    for entry in entries:
        if entry.name.endswith('.json') and entry.is_file():
            async with aiofiles.open(entry.path, mode="r") as f:
                events.append(json.loads(await f.read()))
    return events

async def list_artifact_ids():
    artifact_ids = []
    entries = await scandir(ARTIFACTS_DIR)
    for entry in entries:
        if not entry.name.startswith('.') and entry.is_dir():
            artifact_ids.append(entry.name)
    return artifact_ids

@router.get("/")
async def artifacts():
    artifact_ids = await list_artifact_ids()
    artifacts = []
    for artifact_id in artifact_ids:
        artifacts.append(await get_artifact(artifact_id))
    return artifacts

@router.get("/{artifact_id}")
async def artifact(artifact_id: str):
    return await get_artifact(artifact_id)

@router.get("/{artifact_id}/events")
async def artifact_events(artifact_id: str):
    return await get_artifact_events(artifact_id)

