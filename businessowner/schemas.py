from ninja import Schema, UploadedFile
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class LoginIn(Schema):
    email: str
    password: str


class LoginOut(Schema):
    email: str
    password: str
    message: str
    result:bool
    data: list[LoginIn]


class ChangePasswordIn(Schema):
    email: str
    old_password: str
    new_password: str
    confirm_password: str


class ChangePasswordOut(Schema):
    result: bool
    message: str


class ForgotPasswordIn(Schema):
    email: str


class PlanSchemaIn(Schema):
    plan_name: str
    description: str
    price: float
    validity: int
    image: str
    status: str
    

class PurchaseHistoryOut(Schema):
    plan_name: str
    order_id: str
    status: str
    purchase_date: datetime


class BusinessOwnerIn(BaseModel):
    business_name: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    address: str = None
    tuition_tagline: str = None
    city: int = None  
    logo: str = None
    status: str = None


class CitySchema(Schema):
    city_id: int
    city_name: str
    state_id: int
    state_name: str


class BusinessOwnerOut(Schema):
    business_name: str
    business_type: str
    first_name: str
    last_name: str
    email: str
    contact_no: str 
    address: str
    logo: str = None
    tuition_tagline: str= None
    status: str
    created_at: datetime
    city: CitySchema 


####################################################################################################
####---------------------------------------COMPETITIVE------------------------------------------####
####################################################################################################

class BatchIn(Schema):
    batch_name :str

class BatchUpdate(Schema):
    id: int =None
    batch_name: str = None
    status: str = None


class SubjectIn(Schema):
    subject_name :str

class SubjectUpdate(Schema):
    id: int =None
    subject_name: str = None
    status: str = None


class ChapterIn(Schema):
    subject_name: UUID
    chapter_name: str
    batches: list[UUID]
  

























































































































####################################################################################
####--------------------------------ACADEMIC------------------------------------####
####################################################################################


class AcademicBoardSchema(Schema):
    id: int
    board_name: str
    business_owner_id: int
    status: str
    created_at: datetime
    updated_at: datetime
  

    class Config:
        orm_mode = True