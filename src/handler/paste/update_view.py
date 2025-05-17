import base64
from sqlalchemy.orm import Session

from src.api.paste.request import UpdatePasteViewsRequest
from src.handler.abstract import RequestHandler
from src.handler.error import RequestHandlingError


class UpdatePasteViewRequestHandler(RequestHandler):
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, request: UpdatePasteViewsRequest) -> None:
        if request.signature != base64.b64encode(request.paste.signature).decode():
            raise RequestHandlingError("Invalid paste signature")

        with self.session as s:
            s.add(request.paste)
            request.paste.current_opens += 1
            s.commit()
