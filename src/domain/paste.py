from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Self
from uuid import UUID
from uuid import uuid4

from .base import Base


class Paste(Base):
    __tablename__ = 'paste'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    paste: Mapped[bytes]
    iv: Mapped[bytes]
    signature: Mapped[bytes]
    password_protected: Mapped[bool] = False
    ttl: Mapped[int | None]
    opens_limit: Mapped[int | None]
    current_opens: Mapped[int]
    date_created: Mapped[datetime]

    @classmethod
    def init(
        cls,
        paste: bytes,
        iv: bytes,
        signature: bytes,
        password_protected: bool,
        ttl: int | None,
        opens_limit: int | None,
    ) -> Self:
        instance = cls()

        instance.id = uuid4()
        instance.paste = paste
        instance.iv = iv
        instance.signature = signature
        instance.password_protected = password_protected
        instance.ttl = ttl
        instance.opens_limit = opens_limit

        instance.current_opens = 0
        instance.date_created = datetime.now()

        return instance
