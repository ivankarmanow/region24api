import datetime as dt
from typing import Optional

from app.model.enum import ActionEnum, EntityEnum
from app.model.schema.admin.core import Admin
from app.model.schema.base import BaseModel
from app.model.schema.client.core import Client


class ActionHistoryBase(BaseModel):
    action: ActionEnum
    entity: EntityEnum
    data: dict


class ActionHistoryIn(ActionHistoryBase):
    admin_id: Optional[int]
    client_id: Optional[int]
    is_system_admin: bool = False


class ActionHistory(ActionHistoryBase):
    id: int
    timestamp: dt.datetime
    admin: Optional[Admin]
    client: Optional[Client]
    is_system: bool = False
