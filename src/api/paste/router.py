from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from uuid import UUID

from src.domain.paste import Paste
from src.handler.error import RequestHandlingError

from ...container import Container
from ...handler.abstract import RequestHandler
from .request import CreatePasteRequest
from .request import DeletePasteRequest
from .request import SignedRequest
from .request import UpdatePasteViewsRequest
from .response import CreatePasteResponse
from .response import GetPasteResponse
from .response import OKResponse

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


@router.get('/paste/{paste_id}', response_model=GetPasteResponse)
@inject
def get_paste(
    paste_id: UUID,
    handler: RequestHandler[UUID, Paste] = Depends(
        Provide[Container.handlers.paste_get]
    ),
) -> GetPasteResponse:
    try:
        return GetPasteResponse.from_paste(handler.handle(paste_id))
    except RequestHandlingError:
        raise HTTPException(status_code=404, detail="NOT_FOUND_OR_EXPIRED")


@router.put('/paste/{paste_id}/view', response_model=OKResponse)
@inject
def update_paste_views(
    paste_id: UUID,
    request: SignedRequest,
    get_paste_handler: RequestHandler[UUID, Paste] = Depends(
        Provide[Container.handlers.paste_get]
    ),
    handler: RequestHandler[UpdatePasteViewsRequest, None] = Depends(
        Provide[Container.handlers.paste_update_view]
    ),
) -> OKResponse:
    try:
        paste = get_paste_handler.handle(paste_id)
        update_request = UpdatePasteViewsRequest(
            paste=paste, signature=request.signature
        )
        handler.handle(update_request)
    except RequestHandlingError:
        pass
    return OKResponse()

@router.post('/paste/{paste_id}/delete', response_model=OKResponse)
@inject
def delete_paste(
    paste_id: UUID, 
    request: SignedRequest,
    get_paste_handler: RequestHandler[UUID, Paste] = Depends(
        Provide[Container.handlers.paste_get]
    ),
    handler: RequestHandler[DeletePasteRequest, None] = Depends(
        Provide[Container.handlers.paste_delete]
    )
) -> OKResponse:
    try:
        paste = get_paste_handler.handle(paste_id)
        handler.handle(DeletePasteRequest(paste=paste, signature=request.signature))
    except RequestHandlingError:
        pass
    return OKResponse()
