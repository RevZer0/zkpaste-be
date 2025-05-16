from ..abstract import RequestHandler
from src.api.paste.request import CreatePasteRequest
from sqlalchemy.orm import Session
from uuid import UUID
from src.domain.paste import Paste
import base64


class CreatePasteRequestHandler(RequestHandler):
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, request: CreatePasteRequest) -> UUID:
        paste = Paste.init(
            base64.b64decode(request.ciphertext),
            base64.b64decode(request.iv),
            base64.b64decode(request.signature),
            request.metadata.password_protected,
            request.metadata.opens_count,
            request.metadata.ttl
        )
        with self.session as s:
            s.add(paste)
            s.commit()
        return paste.id

