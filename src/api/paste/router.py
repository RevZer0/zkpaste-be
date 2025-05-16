from fastapi import APIRouter, Depends
from .response import CreatePasteResponse
from .request import CreatePasteRequest
from ...handler.abstract import RequestHandler
from uuid import UUID
from ...container import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter()

@router.post('/paste', response_model=CreatePasteResponse)
@inject
def create_paste(
    request: CreatePasteRequest,
    handler: RequestHandler[CreatePasteRequest, UUID] = Depends(
        Provide[Container.handlers.paste_create]
    )
) -> CreatePasteResponse:
    return CreatePasteResponse(paste_id=handler.handle(request))

