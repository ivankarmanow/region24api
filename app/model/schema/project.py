from typing import Optional
import datetime as dt

from pydantic import Field, field_validator

from app.model.schema.base import BaseModel
from app.model.schema.service.core import Service


class ProjectMedia(BaseModel):
    image: str
    is_main: bool = Field(default=False)


class ProjectBase(BaseModel):
    title: str
    media: list[ProjectMedia]
    description: str
    datetime: dt.date
    address: str
    area: Optional[int]
    period: int
    price: int
    features: list[str]

    @field_validator("features", mode="before")
    @classmethod
    def extract_features(cls, values: list[object]) -> list[str]:
        return [ftr.feature if hasattr(ftr, "feature") else ftr for ftr in values]


class ProjectIn(ProjectBase):
    service_id: int


class Project(ProjectBase):
    id: int
    service: Service
