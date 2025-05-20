from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, SuperAdmin, AdminAuth, ClientAuth
from app.model.db import Request as RequestDB
from app.model.enum import RequestStatus
from app.model.schema.request import Request, RequestIn, RequestAdminIn
from app.response import APIResponse

request = APIRouter(tags=["request"], prefix="/request")


@request.get("/list")
async def request_list(session: SessionDep, admin: AdminAuth) -> list[Request]:
    requests = session.scalars(select(RequestDB)).all()
    return requests


@request.post("/new")
async def request_new(session: SessionDep, request: RequestIn, client: ClientAuth) -> APIResponse:
    db = RequestDB(**request.model_dump())
    db.client = client
    session.add(db)
    session.commit()
    return APIResponse()


@request.post("/create")
async def create_request(session: SessionDep, request: RequestAdminIn, admin: AdminAuth) -> APIResponse:
    session.add(RequestDB(**request.model_dump()))
    session.commit()
    return APIResponse()


@request.put("/edit")
async def edit_request(session: SessionDep, request_id: int, request: RequestIn, admin: AdminAuth) -> APIResponse:
    old_obj = session.get(RequestDB, request_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in request.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@request.delete("/delete")
async def delete(session: SessionDep, request_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(RequestDB, request_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@request.post("/status")
async def request_status(session: SessionDep, id: int, status: RequestStatus, admin: AdminAuth) -> APIResponse:
    old_obj = session.get(RequestDB, id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    old_obj.status = status
    session.add(old_obj)
    session.commit()
    return APIResponse()


@request.get("/{id}")
async def request_get(session: SessionDep, id: int, admin: AdminAuth) -> Request:
    request = session.get(RequestDB, id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request
