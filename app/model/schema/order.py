import datetime as dt
from typing import Optional

from app.model.enum import OrderStatus
from app.model.schema.base import BaseModel
from app.model.schema.client.core import Client
from app.model.schema.request import Request
from app.model.schema.service.core import Service


class OrderElement(BaseModel):
    price: Optional[int]
    start: Optional[dt.datetime]
    end: Optional[dt.datetime]
    comment: Optional[str]
    service: Service


class OrderElementIn(BaseModel):
    price: Optional[int]
    start: Optional[dt.datetime]
    end: Optional[dt.datetime]
    comment: Optional[str]
    service_id: int


class OrderBase(BaseModel):
    comment: Optional[str]
    price: Optional[int]


class OrderIn(OrderBase):
    client_id: int
    request_id: Optional[int]
    elements: list[OrderElementIn]


class Order(OrderBase):
    id: int
    status: OrderStatus
    created_at: dt.datetime
    updated_at: dt.datetime
    client: Client
    request: Request


class OrderList(Order):
    elements: list[OrderElement]
