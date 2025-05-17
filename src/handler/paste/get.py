from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import Session
from uuid import UUID

from src.domain.paste import Paste
from src.handler.abstract import RequestHandler
from src.handler.error import RequestHandlingError


class GetPasteRequestHandler(RequestHandler):
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, request: UUID) -> Paste:
        paste: Paste | None = self.session.get(Paste, request)

        if paste is None:
            raise RequestHandlingError('Paste has not been found.')

        if datetime.now() > paste.date_created + timedelta(seconds=paste.ttl):
            raise RequestHandlingError('Paste has been expired.')

        if paste.opens_limit and paste.current_opens >= paste.opens_limit:
            raise RequestHandlingError('Paste exceed opens limit')

        return paste
