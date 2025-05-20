from app.model.schema.history import ActionHistory
from .core import AdminBase


class AdminList(AdminBase):
    id: int
    actions: list[ActionHistory]
