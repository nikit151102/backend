from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from fastapi import Request
import json
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from database.database_app import database,on_startup

programmer_swaggerUi = APIRouter()


@programmer_swaggerUi.get("/docs", include_in_schema=False)
async def get_swagger_ui():
    return RedirectResponse("/redoc?lang=ru")



@programmer_swaggerUi.get("/redoc", include_in_schema=False)
async def get_redoc():
    return await get_swagger_ui()