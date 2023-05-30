from fastapi import FastAPI

from .routers import artifacts


app = FastAPI()
app.include_router(artifacts.router)


