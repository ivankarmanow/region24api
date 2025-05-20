from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dependencies import SessionDep, SuperAdmin, AdminAuth, ClientAuth
from app.model.db import Order as OrderDB, OrderService
from app.model.enum import OrderStatus
from app.model.schema.order import Order, OrderIn, OrderList, OrderElementIn
from app.response import APIResponse

order = APIRouter(tags=["order"], prefix="/order")


@order.get("/list")
async def order_list(session: SessionDep, admin: AdminAuth) -> list[Order]:
    orders = session.scalars(select(OrderDB)).all()
    return orders


@order.post("/create")
async def create_order(session: SessionDep, order: OrderIn, admin: AdminAuth) -> APIResponse:
    db = OrderDB(
        comment=order.comment,
        price=order.price,
        client_id=order.client_id,
        request_id=order.request_id
    )
    for elem in order.elements:
        db.elements.append(OrderService(**elem.model_dump()))
    session.add(db)
    session.commit()
    return APIResponse()


@order.put("/edit")
async def edit_order(session: SessionDep, order_id: int, order: OrderIn, admin: AdminAuth) -> APIResponse:
    old_obj = session.get(OrderDB, order_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@order.delete("/delete")
async def delete(session: SessionDep, order_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(OrderDB, order_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@order.post("/status")
async def order_status(session: SessionDep, id: int, status: OrderStatus, admin: AdminAuth) -> APIResponse:
    old_obj = session.get(OrderDB, id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    old_obj.status = status
    session.add(old_obj)
    session.commit()
    return APIResponse()


@order.get("/{id}")
async def order_get(session: SessionDep, id: int, admin: AdminAuth) -> OrderList:
    order = session.get(OrderDB, id, )
    # options=(selectinload(OrderDB.elements).selectinload(OrderService.service))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
