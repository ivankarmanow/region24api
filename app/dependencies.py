import datetime as dt
import os
from typing import Any, Generator, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status, Query
from fastapi_mail import FastMail, ConnectionConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import Config
from app.model.db import ClientToken, Client, AdminToken, Admin

config = Config()
os.makedirs(config.upload_dir, exist_ok=True)
engine = create_engine(config.db_uri)
mail_config = ConnectionConfig(
    MAIL_FROM=config.mail_from,
    MAIL_PORT=config.mail_port,
    MAIL_SERVER=config.mail_host,
    MAIL_USERNAME=config.mail_username,
    MAIL_PASSWORD=config.mail_password,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)


def mail_data() -> FastMail:
    return FastMail(mail_config)


MailData = Annotated[FastMail, Depends(mail_data)]


def session() -> Generator[Session, Any, None]:
    with Session(engine) as _session:
        yield _session


SessionDep = Annotated[Session, Depends(session)]


def check_token(token: Annotated[UUID, Query(description="Client token")], session: SessionDep) -> Client:
    client_token = session.get(ClientToken, token)
    if not client_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if client_token.expires_at < dt.datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    if not client_token.is_confirmed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not confirmed")
    client = client_token.client
    return client


ClientAuth = Annotated[Client, Depends(check_token)]


def check_admin_token(token: Annotated[UUID, Query(description="Admin token")], session: SessionDep) -> Admin:
    admin_token = session.get(AdminToken, token)
    if not admin_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    if admin_token.expires_at < dt.datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    admin = admin_token.admin
    return admin


AdminAuth = Annotated[Admin, Depends(check_admin_token)]


def super_admin(token: Annotated[UUID, Query(description="Super admin token")], session: SessionDep) -> Admin:
    admin = check_admin_token(token, session)
    if admin.can_edit_content:
        return admin
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


SuperAdmin = Annotated[Admin, Depends(super_admin)]
