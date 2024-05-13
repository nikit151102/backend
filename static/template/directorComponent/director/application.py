import uuid
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy import select
from database.database_app import engine_a
from models_db.models_request import Requests, Status, PaymentStatus, Client, Employee, Address, Company
from sqlalchemy.orm.exc import NoResultFound

director_viewApplicacion = APIRouter()


@director_viewApplicacion.get('/getDataApplicacions')
async def send_data_table():
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                    Requests.id,
                    Requests.requestnumber,
                    Status.name.label("statusrequest"),
                    PaymentStatus.name.label("statuspayment"),
                    Requests.reason,
                    Requests.comment,
                    Requests.submissiondate,
                    Requests.completiondate,
                    Requests.estimation,
                    Requests.revenue,
                    Requests.expenses,
                    Requests.profit,
                    Employee.lastname.label("EmployeeLastName"),
                    Employee.firstname.label("EmployeeFirstName"),
                    Employee.middlename.label("EmployeeMiddleName"),
                    Client.lastname.label("ClientLastName"),
                    Client.firstname.label("ClientFirstName"),
                    Client.middlename.label("ClientMiddleName"),
                    Client.phone.label("ClientPhone"),
                    Address.street,
                    Address.house,
                    Address.office,
                    Company.name.label("namecompany")
                )
                .select_from(Requests)
                .join(PaymentStatus, Requests.paymentstatusid == PaymentStatus.id, isouter=True)
                .join(Status, Requests.statusid == Status.id, isouter=True)
                .join(Employee, Requests.employeeid == Employee.id, isouter=True)
                .join(Client, Requests.clientid == Client.id, isouter=True)
                .join(Address, Requests.addressid == Address.id, isouter=True)
                .join(Company, Address.companyid == Company.id, isouter=True)
            )
            result = await session.execute(query)
            rows =  result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')



@director_viewApplicacion.post('/getApplication/{application_id}')
async def get_data_Application(application_id: str):
    try:
        async with AsyncSession(engine_a) as session:
            application_uuid = uuid.UUID(application_id)
            query = (
                select(
                    Requests.id,
                    Requests.requestnumber,
                    Status.name.label("statusrequest"), 
                    PaymentStatus.name.label("statuspayment"), 
                    Requests.reason,  
                    Requests.comment, 
                    Requests.submissiondate,
                    Requests.completiondate,
                    Requests.estimation,
                    Requests.revenue,
                    Requests.expenses,
                    Requests.profit,
                    Employee.lastname.label("EmployeeLastName"),
                    Employee.firstname.label("EmployeeFirstName"),
                    Employee.middlename.label("EmployeeMiddleName"),
                    Client.lastname.label("ClientLastName"),
                    Client.firstname.label("ClientFirstName"),
                    Client.middlename.label("ClientMiddleName"),
                    Client.phone.label("ClientPhone"),
                    Address.street,
                    Address.house,
                    Address.office,
                    Company.name.label("namecompany")
                )
                .select_from(Requests)
                .join(PaymentStatus, Requests.paymentstatusid == PaymentStatus.id, isouter=True)
                .join(Status, Requests.statusid == Status.id, isouter=True)
                .join(Employee, Requests.employeeid == Employee.id, isouter=True)
                .join(Client, Requests.clientid == Client.id, isouter=True)
                .join(Address, Requests.addressid == Address.id, isouter=True)
                .join(Company, Address.companyid == Company.id, isouter=True)
                .where(Requests.id == application_uuid)
                )
            result = await session.execute(query)
            row =  result.fetchone()
            return row
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')


@director_viewApplicacion.get('/getStatusApplication')
async def get_data_statusApplication():
    try:
        async with AsyncSession(engine_a) as session:
            query = select(Status.name.label("status_application"))
            result = await session.execute(query)
            rows = result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

@director_viewApplicacion.get('/getStatusPayment')
async def get_data_statusApplication():
    try:
        async with AsyncSession(engine_a) as session:
            query = select(PaymentStatus.name.label("status_payment"))
            result = await session.execute(query)
            rows = result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')
    
@director_viewApplicacion.delete('/deleteApplication/{application_id}')
async def delete_application(application_id: str):
    try:
        async with AsyncSession(engine_a) as session:
            query = delete(Requests).where(Requests.id == application_id)
            result = await session.execute(query)
            await session.commit()
            deleted_rows = result.rowcount
            if deleted_rows == 0:
                raise NoResultFound
            return {"message": "Заявка успешно удалена"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')