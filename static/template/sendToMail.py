from fastapi import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr  
import smtplib

class MailRequest(BaseModel):
    email: EmailStr  
    token: str 
    generatePassword: str


conf = ConnectionConfig(
   MAIL_PORT=587,
   MAIL_SERVER="smtp.yandex.ru",
   MAIL_USERNAME="nikit5090135@yandex.ru",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False,
   MAIL_FROM="nikit5090135@yandex.ru",
   MAIL_PASSWORD="ycnjnxwqpajtwjqx",
)

async def send_email(mail_request: dict):
    message = MessageSchema(
       subject="Fastapi-Mail module",
       recipients=[mail_request.email],   
       body=f"""
        <div style="text-align: center;">
           <img src=`http://127.0.0.1:8000/images/logo.webp` alt="Описание изображения" style="width: 190px; height: 190px;">
        </div>

        <p>Здравствуйте,</p>

        <p>Мы рады приветствовать вас в нашей компании! Ниже приведена ваша ссылка для проверки почты:</p>
         <p>Логин:{mail_request.email}</p>
         <p>Пароль{mail_request.generatePassword}</p>

         <a href="http://localhost:4200/VerificationUser/{mail_request.token}">http://localhost:4200/VerificationUser/{mail_request.token}</a>

        <p>Пожалуйста, перейдите по этой ссылке для активации вашей учетной записи. Если у вас возникнут какие-либо вопросы или затруднения, не стесняйтесь обращаться в нашу службу поддержки.</p>

        <p>С уважением, ТОО "ВИТКОН Сервис"</p>
        """,
        subtype="html"
    )
   
    fm = FastMail(conf)
    await fm.send_message(message)

