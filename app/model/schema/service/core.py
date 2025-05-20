from typing import Optional

from app.model.schema.base import BaseModel


class ServiceCategoryBase(BaseModel):
    title: str
    image: Optional[str]


class ServiceCategoryIn(ServiceCategoryBase):
    ...


class ServiceCategory(ServiceCategoryBase):
    id: int


class ServiceCategoryList(ServiceCategoryBase):
    id: int
    services: list["Service"]


class ServiceBase(BaseModel):
    title: str
    image: Optional[str]
    description: str


class ServiceIn(ServiceBase):
    category_id: int


class Service(ServiceBase):
    id: int
    category: ServiceCategory
