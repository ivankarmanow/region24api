from uuid import UUID
import datetime as dt

import datetime as dt
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import status
from passlib.context import CryptContext
from sqlalchemy import select

from app.dependencies import AdminAuth, SuperAdmin
from app.dependencies import SessionDep
from app.model.db import Admin as AdminDB, AdminToken
from app.model.schema.admin.core import Admin, AdminIn
from app.model.schema.admin.depends import AdminList
from app.response import APIResponse, AdminTokenCheck
from app.response import AuthToken

admin = APIRouter(prefix="/admin", tags=["admin"])
auth = APIRouter(prefix="/auth", tags=["admin", "auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@admin.get("/list")
async def admin_list(session: SessionDep, admin_: SuperAdmin) -> list[Admin]:
    admins = session.scalars(select(AdminDB)).all()
    return admins


@admin.post("/create")
async def create_admin(session: SessionDep, admin: AdminIn, admin_: SuperAdmin) -> APIResponse:
    admin_db = AdminDB(
        login=admin.login,
        name=admin.name,
        can_edit_content=admin.can_edit_content,
        password_hash=get_password_hash(admin.password),
    )
    session.add(admin_db)
    session.commit()
    return APIResponse()


@admin.put("/edit")
async def edit_admin(session: SessionDep, admin_id: int, admin: AdminIn, admin_: SuperAdmin) -> APIResponse:
    old_obj = session.get(AdminDB, admin_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Admin not found")
    for key, value in admin.model_dump().items():
        if key == "password":
            key = "password_hash"
            value = get_password_hash(value)
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@admin.delete("/delete")
async def delete(session: SessionDep, admin_id: int, admin_: SuperAdmin) -> APIResponse:
    old_obj = session.get(AdminDB, admin_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Admin not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@admin.get("/{id}")
async def admin_get(session: SessionDep, id: int, admin_: SuperAdmin) -> AdminList:
    admin = session.get(AdminDB, id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


@auth.post("/login")
async def admin_login(login: str, password: str, session: SessionDep) -> AuthToken:
    admin = session.scalar(select(AdminDB).where(AdminDB.login == login))
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    if verify_password(password, admin.password_hash):
        token = AdminToken(expires_at=dt.datetime.now() + dt.timedelta(days=30), admin=admin)
        session.add(token)
        session.commit()
        session.refresh(token)
        return AuthToken(token=token.id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")


@auth.get("/check_token")
async def check_token(session: SessionDep, admin: AdminAuth) -> AdminTokenCheck:
    return AdminTokenCheck(admin_id=admin.id, superadmin=admin.can_edit_content)


@auth.post("/logout")
async def logout(token: UUID, session: SessionDep):
    admin_token = session.get(AdminToken, token)
    if not admin_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    session.delete(admin_token)
    session.commit()
    return APIResponse()
