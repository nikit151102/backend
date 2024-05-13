from fastapi import APIRouter, HTTPException
from static.template.token import decryptToken
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database_app import engine_a
from models_db.models_request import Employee, Position

director_setting = APIRouter()

# Определение схемы OAuth2 для заголовка Authorization типа Bearer Token
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl="authorization",  # Добавленный параметр
)

# Пример использования схемы в зависимостях (Depends)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Здесь вы можете выполнить проверку токена, например, декодировать JWT или проверить в базе данных
    # В этом примере просто вернем значение токена
    return token


@director_setting.get("/getDataAnalytic")
async def read_users_me(current_user: str = Depends(get_current_user)):
    currentuser = decryptToken(current_user)
    print("qw", currentuser)
    return currentuser




@director_setting.get("/getDataUsers")
async def read_users():
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                    Employee.id,
                    Employee.lastname,
                    Employee.firstname,
                    Employee.middlename,
                    Position.name.label("position")
                )
                .join(Position, Employee.positionid == Position.id)
                .where(Employee.positionid != 1)
            )
            result = await session.execute(query)
            rows = result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')