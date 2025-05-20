from typing import Optional

from app.model.schema.base import BaseModel


class ClientBase(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]
    comment: Optional[str]


class ClientIn(ClientBase):
    ...


class Client(ClientBase):
    id: int
