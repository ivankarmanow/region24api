from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, AdminAuth
from app.model.db import Client as ClientDB
from app.model.schema.client.core import Client, ClientIn
from app.model.schema.client.depends import ClientList
from app.response import APIResponse, ClientCreated

client = APIRouter(tags=["client"], prefix="/client")


@client.get("/list")
async def client_list(session: SessionDep, admin: AdminAuth) -> list[Client]:
    clients = session.scalars(select(ClientDB)).all()
    return clients


@client.post("/create")
async def create_client(session: SessionDep, client: ClientIn) -> ClientCreated:
    client_db = session.execute(select(ClientDB).where(ClientDB.email == client.email)).scalar_one_or_none()
    if client_db:
        client_id = client_db.id
    else:
        client = ClientDB(**client.model_dump())
        session.add(client)
        session.commit()
        client_id = client.id
    return ClientCreated(client_id=client_id)


@client.put("/edit")
async def edit_client(session: SessionDep, client_id: int, client: ClientIn, admin: AdminAuth) -> APIResponse:
    old_obj = session.get(ClientDB, client_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@client.delete("/delete")
async def delete(session: SessionDep, client_id: int, admin: AdminAuth) -> APIResponse:
    old_obj = session.get(ClientDB, client_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Client not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@client.get("/{id}")
async def client_get(session: SessionDep, id: int, admin: AdminAuth) -> ClientList:
    client = session.get(ClientDB, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
