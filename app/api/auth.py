import datetime as dt
import random
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, status, HTTPException
from fastapi_mail import MessageSchema, MessageType
from sqlalchemy import select

from app.dependencies import SessionDep, MailData, ClientAuth
from app.model.db import Client, ClientToken
from app.response import APIResponse, AuthToken

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/send_code")
async def send_code(
    client_id: int,
    session: SessionDep,
    mail_data: MailData,
    background_tasks: BackgroundTasks
) -> APIResponse:
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    token = ClientToken(
        expires_at=dt.datetime.now() + dt.timedelta(days=30), client=client, code=random.randint(100000, 999999)
        )
    session.add(token)
    session.commit()
    session.refresh(token)
    try:
        message = MessageSchema(
            subject="Подтверждение электронной почты",
            recipients=[client.email],
            body=f"Ваш адрес электронной почты был использован для авторизации на сайте Регион24.<br>"
                 f"<b>Если это были не вы, игнорируйте это сообщение</b><br>"
                 f"Если вы действительно авторизовались через данную почту, используйте код ниже.<br><br>"
                 f"<h3>{token.code}</h3>",
            subtype=MessageType.html,
        )
        background_tasks.add_task(mail_data.send_message, message)
        return AuthToken(token=token.id)
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось отправить письмо")


@auth.get("/verify")
async def verify(code: int, session: SessionDep):
    client_token = session.scalar(select(ClientToken).where(ClientToken.code == code))
    if not client_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    if client_token.expires_at < dt.datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    if client_token.is_confirmed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token yet confirmed")
    client_token.is_confirmed = True
    session.add(client_token)
    session.commit()
    return AuthToken(token=client_token.id)


@auth.get("/check_token")
async def check_token(client: ClientAuth):
    return APIResponse()


@auth.post("/logout")
async def logout(token: UUID, session: SessionDep):
    client_token = session.get(ClientToken, token)
    if not client_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    session.delete(client_token)
    session.commit()
    return APIResponse()
