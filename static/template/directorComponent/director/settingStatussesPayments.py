from fastapi import APIRouter, HTTPException, Request
from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database.database_app import engine_a
from models_db.models_request import  PaymentStatus

StatussesPayments_setting = APIRouter()

    


@StatussesPayments_setting.post("/setStatussPayment")
async def set_statusses(request: Request):
    try:
        data = await request.json()
        newname = data.get('newname')
        
        async with AsyncSession(engine_a) as session:
            new_status = PaymentStatus(name=newname)
            session.add(new_status)
            await session.commit()
            await session.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')
    
@StatussesPayments_setting.delete("/deleteStatusPayment/{status_id}")
async def delete_status(status_id: int):
    try:
        async with AsyncSession(engine_a) as session:

            await session.execute(delete(PaymentStatus).where(PaymentStatus.id == status_id))
            
            await session.commit()
            
            check_query = (
                select(PaymentStatus)
                .where(PaymentStatus.id == status_id)
            )
            result = await session.execute(check_query)
            remaining_status = result.scalar_one_or_none()
            
            if remaining_status is not None:
                print(f"Статус с ID {status_id} не удален")
                raise HTTPException(status_code=404, detail=f'Статус с ID {status_id} не найден')
            else:
                print(f"Статус с ID {status_id} успешно удален")
                return {"message": "Статус успешно удален"}    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')
    
@StatussesPayments_setting.get("/getStatussesPayments")
async def get_statusses():
    try:
        async with AsyncSession(engine_a) as session:
            query = (
                select(
                    PaymentStatus.id,
                    PaymentStatus.name
                ) 
                .select_from(PaymentStatus)
            )
            result = await session.execute(query)
            rows = result.fetchall()
            await session.commit()  
            await session.close()
            
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')
    

@StatussesPayments_setting.put("/updateStatusPayment/")
async def update_status(request: Request):
    try:
        async with AsyncSession(engine_a) as session:
            data = await request.json()
            status_id = data.get('id')

            check_query = (
                select(PaymentStatus)
                .where(PaymentStatus.id == status_id)
            )
            result = await session.execute(check_query)
            existing_status = result.scalar_one_or_none()

            if existing_status is None:
                raise HTTPException(status_code=404, detail=f"Статус с ID {status_id} не найден")

            existing_status.name = data.get('name')

            await session.commit()
            await session.close()

            return {"message": f"Статус с ID {status_id} успешно обновлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')