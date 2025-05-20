import datetime as dt
from typing import Optional

from app.model.enum import RequestStatus
from app.model.schema.base import BaseModel
from app.model.schema.client.core import Client
from app.model.schema.service.core import Service


class RequestBase(BaseModel):
    text: str


class RequestIn(RequestBase):
    service_id: Optional[int]


class RequestAdminIn(RequestIn):
    client_id: int


class Request(RequestBase):
    id: int
    client: Client
    service: Optional[Service]
    status: RequestStatus
    created_at: dt.datetime
    updated_at: dt.datetime
