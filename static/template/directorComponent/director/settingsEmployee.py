from fastapi import APIRouter, HTTPException
from static.template.token import decryptToken
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database.database_app import engine_a
from models_db.models_request import Employee, PaymentStatus, Position, Status
from static.template.criptoPassword import encrypt
from pydantic import BaseModel
from typing import Optional

class UpdateEmployeeModel(BaseModel):
    lastname: Optional[str]
    firstname: Optional[str]
    middlename: Optional[str]
    initials: Optional[str]
    positionid: Optional[int]
    phone: Optional[str]
    email: Optional[str]
    login: Optional[str]
    password: Optional[str]
    emailtoken: Optional[str]

Employee_setting = APIRouter()

@Employee_setting.get("/getUsers")
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

from sqlalchemy.ext.asyncio import AsyncSession

@Employee_setting.post("/addUser")
async def set_users(lastname: str, firstname: str, middlename: str, initials: str,
                    positionid: int, phone: str, email: str, login: str,
                    password: str):
    try:
        async with AsyncSession(engine_a) as session:

            newPassword = encrypt(password)

            new_employee = Employee(
                lastname=lastname,
                firstname=firstname,
                middlename=middlename,
                initials=initials,
                positionid=positionid,
                phone=phone,
                email=email,
                login=login,
                password=newPassword["content"],
                iv=newPassword["iv"],
                emailtoken='true'
            )
            
            session.add(new_employee)
            await session.commit()
            
            return {"message": "Пользователи успешно добавлены"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')


@Employee_setting.delete("/deleteUser/{user_id}")
async def delete_status(user_id: str):
    try:
        async with AsyncSession(engine_a) as session:

            await session.execute(delete(Employee).where(Employee.id == user_id))
            
            await session.commit()
            
            check_query = (
                select(Employee)
                .where(Employee.id == user_id)
            )
            result = await session.execute(check_query)
            remaining_status = result.scalar_one_or_none()
            
            if remaining_status is not None:
                print(f"Сотрудник с ID {user_id} не удален")
            else:
                print(f"Сотрудник с ID {user_id} успешно удален")
            
            return {"message": "Сотрудник успешно удален"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

@Employee_setting.get("/getUser/{employee_id}")
async def get_user(employee_id: str):
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                    Employee.id,
                    Employee.lastname,
                    Employee.firstname,
                    Employee.middlename,
                    Employee.initials,
                    Position.name.label("position"),
                    Employee.phone,
                    Employee.email,
                )
                .join(Position, Employee.positionid == Position.id)
                .where(Employee.id == employee_id)
            )
            result = await session.execute(query)
            rows = result.fetchone()

            if rows is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            
            return rows
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

@Employee_setting.put("/updateUser/{employee_id}")
async def update_user(employee_id: str, employee_data: UpdateEmployeeModel):
    try:
        async with AsyncSession(engine_a) as session:

            employee = await session.get(Employee, employee_id)
            
            if employee is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            
            for field, value in employee_data.dict(exclude_unset=True).items():
                if field == "password":
                    newPassword = encrypt(value)
                    setattr(employee, "password", newPassword["content"])
                    setattr(employee, "iv", newPassword["iv"])
                else:
                    setattr(employee, field, value)
            
            await session.commit()
            
            return {"message": "Данные сотрудника успешно обновлены"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')
    


@Employee_setting.get('/getInitialsUsers')
async def send_data_table():
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                    Employee.initials.label("valueinitials")
                )
                .select_from(Employee)
                .distinct(Employee.initials) 
            )
            result = await session.execute(query)
            rows = result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

