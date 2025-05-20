from typing import Optional

from app.model.schema.base import BaseModel


class ContactBase(BaseModel):
    name: str
    contact: str
    icon: Optional[str]


class ContactIn(ContactBase):
    ...


class Contact(ContactBase):
    id: int
