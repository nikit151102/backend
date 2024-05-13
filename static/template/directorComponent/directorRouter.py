from fastapi import APIRouter

from static.template.directorComponent.director.home import director_home
from static.template.directorComponent.director.canban import director_canban
from static.template.directorComponent.director.kanbanCurrentDay import director_KanbanCurrentDay
from static.template.directorComponent.director.application import director_viewApplicacion
from static.template.directorComponent.director.analytic import director_analytic
from static.template.directorComponent.director.setting import director_setting
from static.template.directorComponent.director.financeAnalytic import director_finance_analytic
from static.template.directorComponent.director.settingStatussesRequests import StatussesRequests_setting
from static.template.directorComponent.director.settingStatussesPayments import StatussesPayments_setting
from static.template.directorComponent.director.settingsEmployee import Employee_setting
from static.template.directorComponent.director.notes import NotesRouter


directorRouter = APIRouter()

directorRouter.include_router(director_home, prefix="/home", tags=["director home"])
directorRouter.include_router(director_canban, prefix="/canban", tags=["director canban"])
directorRouter.include_router(director_KanbanCurrentDay, prefix="/kanbanCurrentDay", tags=["director kanbanCurrentDay"])
directorRouter.include_router(director_viewApplicacion, prefix="/application", tags=["director Application"])
directorRouter.include_router(director_analytic, prefix="/analytic", tags=["director analytic"])
directorRouter.include_router(director_finance_analytic, prefix="/financeAnalytic", tags=["director financeAnalytic"])
directorRouter.include_router(director_setting, prefix="/setting", tags=["director setting"])
directorRouter.include_router(StatussesRequests_setting, prefix="/statussesRequests", tags=["director StatussesRequests"])
directorRouter.include_router(StatussesPayments_setting, prefix="/statussesPayments", tags=["director StatussesPayments"])
directorRouter.include_router(Employee_setting, prefix="/settingEmployee", tags=["director settingEmployee"])
directorRouter.include_router(NotesRouter, prefix="/Notes", tags=["director Notes"])

