from uuid import UUID
from pydantic import BaseModel


class Artifact(BaseModel):
    id: UUID
    status: str
    rc: int
