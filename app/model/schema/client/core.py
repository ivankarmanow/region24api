from typing import Optional

from pydantic import Field

from app.model.schema.base import BaseModel


class ClientBase(BaseModel):
    name: str
    phone: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    comment: Optional[str] = Field(None)


class ClientIn(ClientBase):
    ...


class Client(ClientBase):
    id: int
