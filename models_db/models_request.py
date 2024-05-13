from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, DECIMAL,Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

Base = declarative_base()

class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class PaymentStatus(Base):
    __tablename__ = 'paymentstatuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class RequestAct(Base):
    __tablename__ = 'request_acts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)

class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    lastname = Column(String(255))
    firstname = Column(String(255))
    middlename = Column(String(255))
    initials= Column(String(15))
    positionid = Column(Integer, ForeignKey('positions.id'))
    phone = Column(String(15))
    email = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    iv = Column(String(255))
    emailtoken = Column(String(255))

    position = relationship("Position")

class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    lastname = Column(String(255))
    firstname = Column(String(255))
    middlename = Column(String(255))
    phone = Column(String(15))
    email = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    iv = Column(String(255))
    emailtoken = Column(String(255))

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    accounturl = Column(String(255))

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    street = Column(String(255))
    house = Column(String(10))
    office = Column(String(10))
    companyid = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company")

class ClientAddress(Base):
    __tablename__ = 'clientaddresses'

    clientid = Column(UUID(as_uuid=True), primary_key=True)
    addressid = Column(Integer, ForeignKey('addresses.id'), primary_key=True)

class TypesRequest(Base):
    __tablename__ = 'typesrequest'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class Notes(Base):
    __tablename__ = 'notes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    employeeid = Column(UUID(as_uuid=True), ForeignKey('employees.id'))

    employee = relationship("Employee")

class Requests(Base):
    __tablename__ = 'requests'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    requestnumber = Column(Integer)
    statusid = Column(Integer, ForeignKey('statuses.id'))
    paymentstatusid = Column(Integer, ForeignKey('paymentstatuses.id'))
    employeeid = Column(UUID(as_uuid=True), ForeignKey('employees.id'))
    clientid = Column(UUID(as_uuid=True), ForeignKey('clients.id'))
    addressid = Column(Integer, ForeignKey('addresses.id'))
    discharged = Column(Text)
    reason = Column(Text)
    comment = Column(Text)
    submissiondate = Column(Date)
    completiondate = Column(Date)
    estimation = Column(Integer)
    actid = Column(Integer, ForeignKey('request_acts.id'))
    revenue = Column(DECIMAL(10, 2))
    expenses = Column(DECIMAL(10, 2))
    profit = Column(DECIMAL(10, 2))

    status = relationship("Status")
    payment_status = relationship("PaymentStatus")
    employee = relationship("Employee")
    client = relationship("Client")
    address = relationship("Address")
    act = relationship("RequestAct")

class RequestStatusHistory(Base):
    __tablename__ = 'requeststatushistory'

    id = Column(Integer, primary_key=True)
    requestid = Column(UUID(as_uuid=True), ForeignKey('requests.id'))
    statusid = Column(Integer, ForeignKey('statuses.id'))
    date = Column(Date)
    time = Column(Time)

    request = relationship("Requests")
    status = relationship("Status")


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    quantity = Column(Integer)
    request_id = Column(Integer, ForeignKey('requests.id'))

    request = relationship("Requests")

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    quantity = Column(Integer)
    request_id = Column(Integer, ForeignKey('requests.id'))

    request = relationship("Requests")
