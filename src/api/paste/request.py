from typing import Optional
from pydantic import BaseModel

class CreatePasteRequestMetadata(BaseModel):
    password_protected: bool = False
    opens_count: Optional[int] = None
    ttl: Optional[int] = None 


class CreatePasteRequest(BaseModel):
    ciphertext: str
    iv: str
    signature: str
    metadata: CreatePasteRequestMetadata


