from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, AdminAuth, ClientAuth
from app.model.db import Client as ClientDB
from app.model.schema.client.core import Client, ClientIn
from app.model.schema.client.depends import ClientList
from app.response import APIResponse, ClientCreated, AuthRequired, EmailExists

client = APIRouter(tags=["client"], prefix="/client")


@client.get("/list")
async def client_list(session: SessionDep, admin: AdminAuth) -> list[Client]:
    clients = session.scalars(select(ClientDB)).all()
    return clients


@client.get("/email_exists")
async def client_email_exists(session: SessionDep, email: str) -> EmailExists:
    resp = EmailExists(email=email)
    clt = session.execute(select(ClientDB).where(ClientDB.email == email)).scalar_one_or_none()
    if clt:
        resp.exists = True
        resp.client_id = clt.id
    else:
        resp.exists = False
    return resp



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


@client.put("/edit_my")
async def edit_my_client(session: SessionDep, old_client: ClientAuth, new_client: ClientIn) -> AuthRequired:
    resp = AuthRequired(client_id=old_client.id)
    old_client.name = new_client.name
    if new_client.email and new_client.email != old_client.email:
        if session.execute(select(ClientDB).where(ClientDB.email == new_client.email)).one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
        old_client.email = new_client.email
        old_client.tokens = []
        resp.auth_required = True
    if new_client.phone:
        old_client.phone = new_client.phone
    session.add(old_client)
    session.commit()
    return resp


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
