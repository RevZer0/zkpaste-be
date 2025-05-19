import base64
from sqlalchemy.orm import Session

from src.api.paste.request import DeletePasteRequest
from src.handler.abstract import RequestHandler
from src.handler.error import RequestHandlingError


class DeletePasteRequestHandler(RequestHandler):
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, request: DeletePasteRequest) -> None:
        if request.paste.signature != base64.b64decode(request.signature):
            raise RequestHandlingError('Invalid paste signature')

        with self.session as s:
            s.add(request.paste)
            s.delete(request.paste)
            s.commit()
