from enum import Enum


class RequestStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    ORDERED = "ordered"
    CANCELLED = "cancelled"


class OrderStatus(str, Enum):
    NEW = "new"
    PAYED = "payed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ActionEnum(str, Enum):
    USER_CREATE = "user_create"
    ADMIN_CREATE = "admin_create"
    UPDATE = "update"
    DELETE = "delete"
    CHANGE_STATUS = "change_status"
    LOGIN = "login"
    LOGOUT = "logout"


class EntityEnum(str, Enum):
    ORDER = "order"
    REQUEST = "request"
    CLIENT = "client"
    ADMIN = "admin"
    SERVICE = "service"
    SERVICE_CATEGORY = "service_category"
    PROJECT = "project"
    PROJECT_CATEGORY = "project_category"
    CONTACT = "contact"
