from app.model.schema.order import Order
from app.model.schema.request import Request
from app.model.schema.service.core import ServiceBase, ServiceCategory


class ServiceList(ServiceBase):
    id: int
    category: ServiceCategory
    requests: list[Request]
    orders: list[Order]
