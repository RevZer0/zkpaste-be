from typing import Callable

from dotenv import dotenv_values
from fastapi import FastAPI, Request, Response

from src.api.paste.router import router as paste_router

from . import api
from .container import Container

env = dotenv_values('.env')

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

application.include_router(paste_router)

