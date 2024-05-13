from ast import List
from datetime import datetime, timedelta, date
from fastapi import APIRouter, HTTPException
from models_db.models_request import Requests, Status
from fastapi import Request
from pydantic import BaseModel
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Date, cast 
from database.database_app import engine_a

director_home = APIRouter()


# #------------------------------------------------------------------------------------------------------------------------
def monday_and_sunday() -> Tuple[date, date]:
    current_date = datetime.now().date()
    day_of_week = current_date.weekday()
    diff = (day_of_week if day_of_week != 0 else 7) - 1
    monday = current_date - timedelta(days=diff)
    sunday = current_date + timedelta(days=(6 - diff))
    return monday, sunday

class ChartData(BaseModel):
    datas: str
    data_count: int
    closed_count: int
    completed_count: int

def generate_date_range(daymonday: date, daysunday: date) -> List[date]:
    delta = daysunday - daymonday
    date_range = [daymonday + timedelta(days=i) for i in range(delta.days)]
    return date_range

async def fetch_data_for_chart(daymonday: date, daysunday: date) -> List[ChartData]:
    async with AsyncSession(engine_a) as session:
        date_range = generate_date_range(daymonday, daysunday)
        
        query = (
            select(
                func.count(Requests.id).label('data_count'),
                func.count().filter(Status.name == 'Закрытая').label('closed_count'),
                func.count().filter(Status.name == 'Выполненная').label('completed_count'),
                cast(Requests.submissiondate, Date).label('datas')
            )
            .join(Status, Requests.statusid == Status.id)
            .where(cast(Requests.submissiondate, Date).between(daymonday, daysunday))
            .group_by(cast(Requests.submissiondate, Date))
            .order_by(cast(Requests.submissiondate, Date).asc())
        )
        
        result = await session.execute(query)
        rows = result.all()

        data_map = {row.datas: row for row in rows}
        
        chart_data_list = []
        for day in date_range:
            row = data_map.get(day)
            if row:
                chart_data = ChartData(
                    datas=row.datas.strftime("%d-%m-%Y"),
                    data_count=row.data_count,
                    closed_count=row.closed_count,
                    completed_count=row.completed_count
                )
            else:
                chart_data = ChartData(
                    datas=day.strftime("%d-%m-%Y"),
                    data_count=0,
                    closed_count=0,
                    completed_count=0
                )
            chart_data_list.append(chart_data)
        
        return chart_data_list

@director_home.get('/statisticsForTheWeek', response_model=List[ChartData])
async def statistics_for_the_week(request: Request):
    try:
        daymonday, daysunday = monday_and_sunday()
        print("daymonday, daysunday", daymonday, daysunday)
        result = await fetch_data_for_chart(daymonday, daysunday)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')






# #------------------------------------------------------------------------------------------------------------------------

@director_home.get("/todaydoughnut")
async def today_doughnut():

    current_date = datetime.now().date()

    async with AsyncSession(engine_a) as session:
        query = (
            select(
                func.count(Requests.id).label('data_count'),
                func.count().filter(Status.name == 'Закрытая').label('closed_count'),
                func.count().filter(Status.name == 'Выполненная').label('completed_count')
            )
            .join(Status, Requests.statusid == Status.id)
            .where(cast(Requests.submissiondate, Date) == current_date)
            .group_by(Status.name)
        )
        result = await session.execute(query)
        rows = result.all()

    if rows:  
        row = rows[0]  
        doughnut_today = [{
            "label": "Не назначенные",
            "value": row['data_count'],
        },{
            "label": "Выполненные",
            "value": row['closed_count'],
        },{
            "label": "Закрытые",
            "value": row['completed_count'],
        }]

        return doughnut_today
    else:
        raise HTTPException(status_code=404, detail="Данные за текущую дату не найдены")  # Здесь ошибка HTTP 404
    






# #------------------------------------------------------------------------------------------------------------------------

class financeData(BaseModel):
    total_obfaia_sale: int or None # type: ignore
    total_sale_zatrat: int or None # type: ignore
    total_pribl: int or None # type: ignore

@director_home.get('/sendfinance')
async def send_finance_statistics():
    async with AsyncSession(engine_a) as session:
        result = await session.execute(
            select(
                func.coalesce(func.sum(Requests.revenue), 0).label('total_obfaia_sale'),
                func.coalesce(func.sum(Requests.expenses), 0).label('total_sale_zatrat'),
                func.coalesce(func.sum(Requests.profit), 0).label('total_pribl')
            )
        )
        row = result.fetchone()

        total_obfaia_sale, total_sale_zatrat, total_pribl = row

        formatted_result = [
            financeData(
                total_obfaia_sale=int(total_obfaia_sale),
                total_sale_zatrat=int(total_sale_zatrat),
                total_pribl=int(total_pribl)
            )
        ]
        return formatted_result

