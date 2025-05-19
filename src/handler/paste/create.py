import binascii
from sqlalchemy.orm import Session
from uuid import UUID

from src.api.paste.request import CreatePasteRequest
from src.domain.paste import Paste
from src.handler.error import RequestHandlingError

from ..abstract import RequestHandler


class CreatePasteRequestHandler(RequestHandler):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.limits = {"iv": 12, "signature": 32, "paste": 128 * 1024}
        self.defaults = {"ttl": 86400}

    def handle(self, request: CreatePasteRequest) -> UUID:
        try:
            paste = Paste.init(
                binascii.a2b_base64(request.ciphertext, strict_mode=True),
                binascii.a2b_base64(request.iv, strict_mode=True),
                binascii.a2b_base64(request.signature, strict_mode=True),
                request.metadata.password_protected,
                request.metadata.ttl if request.metadata.ttl else self.defaults["ttl"],
                request.metadata.opens_count
            )
        except binascii.Error:
            raise RequestHandlingError()

        if len(paste.iv) != self.limits["iv"]:
            raise RequestHandlingError()

        if len(paste.signature) != self.limits["signature"]:
            raise RequestHandlingError()

        with self.session as s:
            s.add(paste)
            s.commit()
        return paste.id
