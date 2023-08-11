from ninja import Schema
from datetime import datetime
from pydantic import BaseModel
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
    
class PurchaseHistorySchema(Schema):
    plan_name: str
    order_id: str
    status: str
    purchase_date: datetime

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
    logo: str
    tuition_tagline: str
    status: str
    created_at: datetime
    city: CitySchema 