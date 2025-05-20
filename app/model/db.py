import datetime as dt
import uuid
from typing import Optional

from sqlalchemy import func, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.model.enum import RequestStatus, OrderStatus, ActionEnum, EntityEnum


class Base(DeclarativeBase):
    ...


class ServiceCategory(Base):
    __tablename__ = "service_category"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    image: Mapped[Optional[str]]

    services: Mapped[list["Service"]] = relationship(back_populates="category")


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    image: Mapped[Optional[str]]
    description: Mapped[str]

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("service_category.id"))

    category: Mapped[Optional[ServiceCategory]] = relationship(back_populates="services")
    requests: Mapped[list["Request"]] = relationship(back_populates="service")
    orders: Mapped[list["Order"]] = relationship(secondary="order_service", back_populates="services")


class ProjectCategory(Base):
    __tablename__ = "project_category"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    image: Mapped[Optional[str]]

    projects: Mapped[list["Project"]] = relationship(back_populates="category")


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    image: Mapped[Optional[str]]
    description: Mapped[str]

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("project_category.id"))
    category: Mapped[Optional[ProjectCategory]] = relationship(back_populates="projects")


class Contact(Base):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    contact: Mapped[str]
    icon: Mapped[Optional[str]]


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    phone: Mapped[Optional[str]]
    email: Mapped[str]
    comment: Mapped[Optional[str]]

    requests: Mapped[list["Request"]] = relationship(back_populates="client")
    orders: Mapped[list["Order"]] = relationship(back_populates="client")
    actions: Mapped[list["ActionHistory"]] = relationship(back_populates="client")
    tokens: Mapped[list["ClientToken"]] = relationship(back_populates="client")


class ClientToken(Base):
    __tablename__ = "client_token"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    created_at: Mapped[dt.datetime] = mapped_column(default=func.now())
    expires_at: Mapped[dt.datetime]
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    code: Mapped[int]

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    client: Mapped[Client] = relationship(back_populates="tokens")


class Request(Base):
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str]
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.NEW)
    created_at: Mapped[dt.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(default=func.now(), onupdate=func.now())

    service_id: Mapped[Optional[int]] = mapped_column(ForeignKey("service.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))

    service: Mapped[Optional[Service]] = relationship(back_populates="requests")
    client: Mapped[Client] = relationship(back_populates="requests")
    order: Mapped[Optional["Order"]] = relationship(back_populates="request")


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)

    comment: Mapped[Optional[str]]
    price: Mapped[Optional[int]] = mapped_column(default=0)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.NEW)
    created_at: Mapped[dt.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(default=func.now(), onupdate=func.now())

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    request_id: Mapped[Optional[int]] = mapped_column(ForeignKey("request.id"))

    client: Mapped[Client] = relationship(back_populates="orders")
    request: Mapped[Request] = relationship(back_populates="order")
    services: Mapped[list[Service]] = relationship(secondary="order_service", back_populates="orders")
    elements: Mapped[list["OrderService"]] = relationship(back_populates="order")


class OrderService(Base):
    __tablename__ = "order_service"

    id: Mapped[int] = mapped_column(primary_key=True)

    price: Mapped[Optional[int]] = mapped_column(default=0)
    start: Mapped[Optional[dt.date]]
    end: Mapped[Optional[dt.date]]
    comment: Mapped[Optional[str]]

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))

    order: Mapped[Order] = relationship(back_populates="elements")
    service: Mapped[Service] = relationship()


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    name: Mapped[Optional[str]]
    password_hash: Mapped[str]
    can_edit_content: Mapped[bool] = mapped_column(default=False)

    actions: Mapped[list["ActionHistory"]] = relationship(back_populates="admin")
    tokens: Mapped[list["AdminToken"]] = relationship(back_populates="admin")


class AdminToken(Base):
    __tablename__ = "admin_token"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    created_at: Mapped[dt.datetime] = mapped_column(default=func.now())
    expires_at: Mapped[dt.datetime]

    admin_id: Mapped[int] = mapped_column(ForeignKey("admin.id"))
    admin: Mapped[Admin] = relationship(back_populates="tokens")


class ActionHistory(Base):
    __tablename__ = "action_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[ActionEnum]
    entity: Mapped[EntityEnum]
    timestamp: Mapped[dt.datetime] = mapped_column(default=func.now())
    data: Mapped[dict] = mapped_column(JSON)

    admin_id: Mapped[Optional[int]] = mapped_column(ForeignKey("admin.id"))
    client_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client.id"))
    is_system: Mapped[bool] = mapped_column(default=False)

    admin: Mapped[Optional[Admin]] = relationship(back_populates="actions")
    client: Mapped[Optional[Client]] = relationship(back_populates="actions")
