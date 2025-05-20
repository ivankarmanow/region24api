from pydantic import BaseModel as BaseModelPD, ConfigDict


class BaseModel(BaseModelPD):
    model_config = ConfigDict(from_attributes=True)
