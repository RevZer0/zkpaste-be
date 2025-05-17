from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from src.handler.error import RequestHandlingError

from ...container import Container
from ...handler.abstract import RequestHandler
from .request import CreatePasteRequest
from .response import CreatePasteResponse

router = APIRouter()


@router.post("/paste", response_model=CreatePasteResponse)
@inject
def create_paste(
    request: CreatePasteRequest,
    handler: RequestHandler[CreatePasteRequest, UUID] = Depends(
        Provide[Container.handlers.paste_create]
    ),
) -> CreatePasteResponse:
    try:
        return CreatePasteResponse(paste_id=handler.handle(request))
    except RequestHandlingError:
        raise HTTPException(status_code=409, detail="PASTE_CREATE_FAILED")
