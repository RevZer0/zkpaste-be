from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable

from src.api.paste.router import router as paste_router

from . import api
from .container import Container
from pathlib import Path

env = dotenv_values((Path(__file__).parent / '../.env').resolve())

container = Container()
application = FastAPI()
container.config.from_dict({
    'db_connection': env['DATABASE_CONNECTION']
})
container.wire(packages=[api])

@application.middleware('http')
async def init_container_resources(request: Request, call_next: Callable) -> Response:
    container.init_resources()
    response = await call_next(request)

    container.shutdown_resources()
    return response

application.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

application.include_router(paste_router)

