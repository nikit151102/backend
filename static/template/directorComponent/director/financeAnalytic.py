from datetime import date
import datetime
from fastapi import APIRouter, HTTPException, Path
from database.database_app import engine_a
from sqlalchemy.ext.asyncio import AsyncSession
from models_db.models_request import Requests, Status, PaymentStatus, Client,Employee, Address
from sqlalchemy import select
from sqlalchemy import and_, cast, Date, func, select
from sqlalchemy.sql import union_all, literal

director_finance_analytic = APIRouter()



@director_finance_analytic.get('/getDataRevenueAnalytic/{start_date}/{end_date}')
async def send_data_table(start_date: str = Path(...), end_date: str = Path(...)):
    try:
        # Преобразуем строки дат в объекты date
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        async with AsyncSession(engine_a) as session:
            stmt = (
                select(
                    Requests.submissiondate,
                    func.max(Requests.revenue).label("max_revenue"),
                    func.min(Requests.revenue).label("min_revenue"),
                    func.avg(Requests.revenue).label("avg_revenue"),
                    func.sum(Requests.revenue).label("total_revenue")
                )
                .where(
                    and_(
                        Requests.submissiondate >= start_date_obj,
                        Requests.submissiondate <= end_date_obj
                    )
                )
                .group_by(Requests.submissiondate)
                .order_by(Requests.submissiondate)
            )
            
            result = await session.execute(stmt)
            revenues_data = [
                {
                    "date": row[0],
                    "max_revenue": row[1],
                    "min_revenue": row[2],
                    "avg_revenue": row[3],
                    "total_revenue": row[4]
                }
                for row in result.fetchall()
            ]
            
            return  revenues_data
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')