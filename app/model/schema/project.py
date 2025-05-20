from typing import Optional

from app.model.schema.base import BaseModel


class ProjectCategoryBase(BaseModel):
    title: str
    image: Optional[str]


class ProjectCategoryIn(ProjectCategoryBase):
    ...


class ProjectCategory(ProjectCategoryBase):
    id: int


class ProjectCategoryList(ProjectCategoryBase):
    id: int
    services: list["Project"]


class ProjectBase(BaseModel):
    title: str
    image: Optional[str]
    description: str


class ProjectIn(ProjectBase):
    category_id: int


class Project(ProjectBase):
    id: int
    category: ProjectCategory
