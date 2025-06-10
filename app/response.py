from uuid import UUID

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    status: bool = Field(default=True)


class AuthToken(APIResponse):
    token: UUID


class UploadedFile(APIResponse):
    filename: str

class ClientCreated(APIResponse):
    client_id: int
