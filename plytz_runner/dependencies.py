import os

from typing import Annotated
from fastapi import Header, HTTPException

WORKDIR = os.environ["WORKDIR"]

async def check_auth_token(x_plytz_auth: Annotated[str, Header()]):
    if x_plytz_auth != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

