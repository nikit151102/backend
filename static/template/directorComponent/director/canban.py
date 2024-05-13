from datetime import datetime
from fastapi import APIRouter, HTTPException
from database.database_app import engine_a
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models_db.models_request import Requests, Status, PaymentStatus, Client, Employee, Address, Company

director_canban = APIRouter()

class CanbanRequestModel(BaseModel):
    startdate: str
    enddate: str

@director_canban.post('/getDataCanban')
async def send_data_canban(data: CanbanRequestModel):
    try:
        startdate = datetime.strptime(data.startdate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат начальной даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.")
    try:
        enddate = datetime.strptime(data.enddate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Недопустимый формат конечной даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.")
    
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
                Company.name.label("namecompany"),
                Company.accounturl.label("accounturlcompany")
            )
            .select_from(Requests)
            .join(PaymentStatus, Requests.paymentstatusid == PaymentStatus.id, isouter=True)
            .join(Status, Requests.statusid == Status.id, isouter=True)
            .join(Employee, Requests.employeeid == Employee.id, isouter=True)
            .join(Client, Requests.clientid == Client.id, isouter=True)
            .join(Address, Requests.addressid == Address.id, isouter=True)
            .join(Company, Address.companyid == Company.id, isouter=True)
            .where(Requests.submissiondate.between(startdate, enddate))
        )
        result = await session.execute(query)
        rows = result.fetchall()
        return [dict(row) for row in rows]