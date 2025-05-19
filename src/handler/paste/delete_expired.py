from datetime import datetime
from sqlalchemy import cast
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import Session

from src.domain.paste import Paste
from src.handler.abstract import RequestHandler


class DeleteExpiredPasteRequestHandler(RequestHandler):
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, request: None = None) -> None:
        with self.session as s:
            to_remove = s.execute(
                select(Paste).where(
                    Paste.date_created + cast('1 second', INTERVAL) * Paste.ttl <= datetime.now()
                )
            ).scalars().all()
            [s.delete(p) for p in to_remove]
            s.commit()
