from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models_db.models_request import Requests, Status, PaymentStatus, Client, Employee, Address, Company
from database.database_app import engine_a

director_KanbanCurrentDay = APIRouter()


@director_KanbanCurrentDay.get('/getDataCanbanCurrentDay')
async def send_data_canban():
    try:
        current_date = datetime.now().date()
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
                    Requests.employeeid,
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
                .where(Requests.submissiondate == current_date)
            )
            result = await session.execute(query)
            rows = result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')