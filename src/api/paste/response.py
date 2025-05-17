import base64
from pydantic import BaseModel
from typing import Self
from uuid import UUID

from src.domain.paste import Paste


class CreatePasteResponse(BaseModel):
    paste_id: UUID


class GetPasteResponse(BaseModel):
    paste_id: UUID
    paste: str
    iv: str
    password_protected: bool

    @classmethod
    def from_paste(cls, paste: Paste) -> Self:
        return cls(
            paste_id=paste.id,
            paste=base64.b64encode(paste.paste).decode(),
            iv=base64.b64encode(paste.iv).decode(),
            password_protected=paste.password_protected,
        )


class OKResponse(BaseModel):
    status: str = "OK"
