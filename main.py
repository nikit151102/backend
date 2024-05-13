from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from static.template.newApplication.RouternewApplication import new_application
from static.template.verifications.isVerification import isVerification
from static.template.connectAccount.routerConnectAccount import personal_account

from static.template.directorComponent.directorRouter import directorRouter
from static.template.client.clientRouter import clientRouter

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(new_application, prefix="/newClientApplication", tags=["New request"])

app.include_router(isVerification, prefix="/Verification" , tags=["Verification client"])
app.include_router(personal_account, prefix="/personal_account")

app.include_router(directorRouter, prefix="/director")

app.include_router(clientRouter, prefix="/client", tags=["client"])



@app.get("/images/logo.webp")
async def get_image():
    image_path = "static/images/logo.webp"
    return FileResponse(image_path)



@app.get("/")
async def read_root():
    return {"Hello": "World"}
