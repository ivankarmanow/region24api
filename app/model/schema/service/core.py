from typing import Optional

from pydantic import model_validator, field_validator

from app.model.schema.base import BaseModel


class ServiceBase(BaseModel):
    title: str
    image: Optional[str]
    description: str
    stages: list[str]
    advantages: list[str]

    @field_validator("stages", mode="before")
    @classmethod
    def extract_stages(cls, values: list[object]) -> list[str]:
        return [stage.stage if hasattr(stage, "stage") else stage for stage in values]

    @field_validator("advantages", mode="before")
    @classmethod
    def extract_advs(cls, values: list[object]) -> list[str]:
        return [adv.advantage if hasattr(adv, "advantage") else adv for adv in values]


class ServiceIn(ServiceBase):
    ...


class Service(ServiceBase):
    id: int
