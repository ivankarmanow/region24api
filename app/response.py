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


class AuthRequired(APIResponse):
    client_id: int
    auth_required: bool = Field(default=False)


class EmailExists(APIResponse):
    email: str
    exists: bool = Field(default=True)
    client_id: int | None = Field(default=None)


class AdminTokenCheck(APIResponse):
    admin_id: int
    superadmin: bool = Field(default=False)

class ClientTokenCheck(APIResponse):
    client_id: int
    name: str
    email: str
    phone: str | None = Field(default=None)

