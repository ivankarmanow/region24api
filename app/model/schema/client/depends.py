from app.model.schema.client.core import ClientBase
from app.model.schema.history import ActionHistory
from app.model.schema.order import Order
from app.model.schema.request import Request


class ClientList(ClientBase):
    id: int
    requests: list[Request]
    orders: list[Order]
    actions: list[ActionHistory]
