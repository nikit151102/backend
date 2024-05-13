from fastapi import APIRouter
from ..criptoPassword import encrypt
from ..randomPassword import generate_temp_password
from ..sendToMail import MailRequest, send_email
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.database_app import engine_a
from models_db.models_request import Address, Client, ClientAddress, Company, Requests, RequestStatusHistory
from .models import RequestModel
from datetime import datetime

new_application = APIRouter()

async def search_clients(session, request):
    existing_client = await session.execute(select(Client).filter(Client.email == request.email, Client.phone == request.nomer))
    existing_client = existing_client.fetchone()
    if existing_client:
        return existing_client[0].id
    else:
        generate_password = generate_temp_password()
        new_password = encrypt(generate_password)
        token = secrets.token_hex(16)
        client = Client(
            lastname=request.lastname,
            firstname=request.firstname,
            middlename=request.middlename,
            phone=request.nomer,
            email=request.email,
            login=request.email,
            password=new_password["content"],
            iv=new_password["iv"],
            emailtoken=token
        )
        await send_email(MailRequest(email=request.email, token=generate_password, generatePassword=new_password["content"]))
        session.add(client)
        await session.commit()
        await session.refresh(client)
        return client.id


async def create_company(session, companyName):
    new_company = Company(
        name=companyName,
        accounturl=''
    )
    session.add(new_company)
    await session.commit()
    await session.refresh(new_company)
    return new_company.id

async def search_adres(session, typeClient, street, houseNumber, apartmentOrOffice, company):
    if typeClient == 'бизнес':
        address_query = (
            select(Address)
            .join(Company)  
            .filter(
                Address.street == street,
                Address.house == houseNumber,
                Address.office == apartmentOrOffice,
                Company.name == company 
            )
        )
    else:
        address_query = (
            select(Address)
            .filter(
                Address.street == street,
                Address.house == houseNumber,
                Address.office == apartmentOrOffice,
                Address.companyid == None  
            )
        )
    existing_adres = await session.execute(address_query)
    return existing_adres.fetchone()

async def get_adres(session, request):
    existing_adres = await search_adres(session, request.typeClient, request.street, request.houseNumber, request.apartmentOrOffice, request.companyName)
    if existing_adres:
        return existing_adres[0].id
    else:
        if request.typeClient == "бизнес":
            company = await create_company(session, request.companyName)
        else:
            company = None

        new_address = Address(
            street=request.street,
            house=request.houseNumber,
            office=request.apartmentOrOffice,
            companyid=company,
        )
        session.add(new_address)
        await session.commit()
        await session.refresh(new_address)
        return new_address.id

async def createRequest(session, request,clientid,adresid):
    new_request = Requests(
                requestnumber=1,
                statusid=1,
                paymentstatusid=None,
                employeeid=None,
                clientid=clientid,
                addressid=adresid,
                reason=request.problema,
                comment=request.comments,
                submissiondate=None,
                completiondate=None,
                estimation=None,
                actid=None,
                revenue=None,
                expenses=None,
                profit=None
            )
    session.add(new_request)
    await session.commit()
    await session.refresh(new_request)
    return new_request.id

async def createStatusRequest(session, request_id):
    current_date = datetime.now().date()  
    current_time = datetime.now().time()  
    current_date_str = current_date.strftime("%Y-%m-%d")
    current_time_str = current_time.strftime("%H:%M")

    RequestStatus = RequestStatusHistory(
        requestid = request_id,
        statusid = 1,
        date = current_date,
        time = current_time
    )
    session.add(RequestStatus)
    await session.commit()
    await session.refresh(RequestStatus)

@new_application.put("/request")
async def create_request(request: RequestModel):
    print("получение новой заявки")
    async with AsyncSession(engine_a) as session:
        client_id = await search_clients(session, request)
        address_id = await get_adres(session, request)
        existing_address_client = await session.execute(select(ClientAddress).filter(ClientAddress.clientid == client_id, ClientAddress.addressid == address_id))
        existing_address_client = existing_address_client.fetchone()
        if existing_address_client:
            new_request = await createRequest(session, request,client_id,address_id)
            await createStatusRequest(session, new_request)
            return {"message": f"Заявка принята {client_id} -------{address_id}"}
        else:
            client_address = ClientAddress(
                clientid=client_id,
                addressid=address_id
            )
            session.add(client_address)
            await session.commit()
            new_request = await createRequest(session, request,client_id,address_id)
            await createStatusRequest(session, new_request)
            return {"message": f"Заявка принята {client_id} -------{address_id}"}
