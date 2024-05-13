from pydantic import BaseModel,EmailStr

class ConnectModel(BaseModel):
    UserLogin: str
    UserPassword: str

class registrationModel(BaseModel):
    Login: str
    Email: str
    Phone: str


class MailRequest(BaseModel):
    email: EmailStr  
    token: str 
    generatePassword: str
