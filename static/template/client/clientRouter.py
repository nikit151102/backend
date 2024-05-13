from datetime import date, timedelta
import datetime
from fastapi import APIRouter, HTTPException, Path
from database.database_app import engine_a
from sqlalchemy.ext.asyncio import AsyncSession
from models_db.models_request import Requests, Status, PaymentStatus, Client, Address, Company, RequestStatusHistory
from sqlalchemy import select, exists
from sqlalchemy import and_, cast, Date, func, select
from sqlalchemy.sql import union_all, literal

clientRouter = APIRouter()


@clientRouter.get('/getRequests/{client_id}')
async def send_data_table(client_id: str):
    try:
        async with AsyncSession(engine_a) as session:
            # Проверка существования клиента
            async with session.begin():
                client_exists = await session.execute(select(exists().where(Client.id == client_id)))
                if not client_exists.scalar():
                    return HTTPException(status_code=404, detail=f'Клиент с id {client_id} не найден')

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
                    Address.street,
                    Address.house,
                    Address.office,
                    Company.name.label("namecompany")
                )
                .select_from(Requests)
                .join(PaymentStatus, Requests.paymentstatusid == PaymentStatus.id, isouter=True)
                .join(Status, Requests.statusid == Status.id, isouter=True)
                .join(Client, Requests.clientid == Client.id, isouter=True)
                .join(Address, Requests.addressid == Address.id, isouter=True)
                .join(Company, Address.companyid == Company.id, isouter=True)
                .where(Client.id == client_id)
            )
            
            async with session.begin():
                result = await session.execute(query)
                rows = result.fetchall()
            
            # Проверка наличия заявок у клиента
            if not rows:
                return HTTPException(status_code=404, detail=f'У клиента с id {client_id} нет заявок')
            
            return [dict(row) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')


@clientRouter.get('/getСurrentRequests/{client_id}')
async def send_data_table(client_id: str = Path(...)):
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
                    Address.street,
                    Address.house,
                    Address.office,
                    Company.name.label("namecompany")
                )
                .select_from(Requests)
                .join(PaymentStatus, Requests.paymentstatusid == PaymentStatus.id, isouter=True)
                .join(Status, Requests.statusid == Status.id, isouter=True)
                .join(Client, Requests.clientid == Client.id, isouter=True)
                .join(Address, Requests.addressid == Address.id, isouter=True)
                .join(Company, Address.companyid == Company.id, isouter=True)
                .where(and_(Client.id == client_id,Status.name.notin_(['Закрытая', 'Выполненная'])
                ))
            )
            result = await session.execute(query)
            rows =  result.fetchall()
            return [dict(row) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

@clientRouter.get('/getRevenue/{client_id}')
async def send_data_table(client_id: str = Path(...)):
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                   func.sum(Requests.revenue).label("total_revenue"),
                )
                .select_from(Requests)
                .join(Client, Requests.clientid == Client.id, isouter=True)
                .where(Client.id == client_id)
            )
            result = await session.execute(query)
            rows =  result.fetchall()
            return [dict(row) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

@clientRouter.get("/request/{request_id}/status-history")
async def get_request_status_history(request_id: str = Path(...)):
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                    RequestStatusHistory.date,
                    RequestStatusHistory.time,
                    Status.name.label("statusrequest"),
                )
                .select_from(RequestStatusHistory)
                .join(Status, RequestStatusHistory.statusid == Status.id, isouter=True)
                .where(RequestStatusHistory.requestid == request_id)
            )
            result = await session.execute(query)
            rows =  result.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')




def transformation_dates(start_date, end_date):
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    return start_date_obj, end_date_obj

@clientRouter.get("/historyRequest/{client_id}")
async def send_data_history(beginDate: str, endDate: str, client_id: str = Path(...)):
    try:
        async with AsyncSession(engine_a) as session:
            start_date, end_date = transformation_dates(beginDate, endDate)
            results = []
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            query = (
                select(
                    cast(Requests.submissiondate, Date),
                    func.coalesce(func.sum(Requests.revenue), 0).label('revenue')
                )
                .select_from(Client)
                .join(Requests, isouter=True)
                .filter(
                    and_(
                        Client.id == client_id,
                        cast(Requests.submissiondate, Date) >= start_date,
                        cast(Requests.submissiondate, Date) <= end_date
                    )
                )
                .group_by(cast(Requests.submissiondate, Date))
            )
            result = await session.execute(query)
            rows = result.fetchall()
            revenue_dict = {row[0]: row[1] for row in rows}
            for date in date_range:
                revenue = revenue_dict.get(date, 0)
                results.append({'date': date.strftime('%Y-%m-%d'), 'revenue': revenue})
            return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')