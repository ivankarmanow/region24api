from app.model.schema.order import Order
from app.model.schema.project import Project
from app.model.schema.request import Request
from app.model.schema.service.core import ServiceBase


class ServiceList(ServiceBase):
    id: int
    requests: list[Request]
    orders: list[Order]
    projects: list[Project]
