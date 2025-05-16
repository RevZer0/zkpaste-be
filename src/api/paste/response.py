from uuid import UUID
from pydantic import BaseModel

class CreatePasteResponse(BaseModel):
    paste_id: UUID

