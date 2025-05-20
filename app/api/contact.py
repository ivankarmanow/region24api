from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, SuperAdmin
from app.model.db import Contact as ContactDB
from app.model.schema.contact import Contact, ContactIn
from app.response import APIResponse

contact = APIRouter(tags=["contact"], prefix="/contact")


@contact.get("/list")
async def contact_list(session: SessionDep) -> list[Contact]:
    contacts = session.scalars(select(ContactDB)).all()
    return contacts


@contact.post("/create")
async def create_contact(session: SessionDep, contact: ContactIn, admin: SuperAdmin) -> APIResponse:
    session.add(ContactDB(**contact.model_dump()))
    session.commit()
    return APIResponse()


@contact.put("/edit")
async def edit_contact(session: SessionDep, contact_id: int, contact: ContactIn, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ContactDB, contact_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@contact.delete("/delete")
async def delete(session: SessionDep, contact_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ContactDB, contact_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@contact.get("/{id}")
async def contact_get(session: SessionDep, id: int) -> Contact:
    contact = session.get(ContactDB, id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
