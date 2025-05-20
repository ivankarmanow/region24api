from typing import Optional

from pydantic import Field

from app.model.schema.base import BaseModel


class AdminBase(BaseModel):
    login: str
    name: Optional[str]
    can_edit_content: bool = Field(default=False)


class AdminIn(AdminBase):
    password: str


class Admin(AdminBase):
    id: int
