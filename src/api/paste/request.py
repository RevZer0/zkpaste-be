from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional

from src.domain.paste import Paste


class CreatePasteRequestMetadata(BaseModel):
    password_protected: bool = False
    opens_count: Optional[int] = None
    ttl: Optional[int] = None


class CreatePasteRequest(BaseModel):
    ciphertext: str
    iv: str
    signature: str
    metadata: CreatePasteRequestMetadata


class SignedRequest(BaseModel):
    signature: str


class UpdatePasteViewsRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    paste: Paste
    signature: str

class DeletePasteRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    paste: Paste
    signature: str
