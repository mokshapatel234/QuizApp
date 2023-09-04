from ninja import Schema
from datetime import datetime
from typing import Optional,List
from uuid import UUID

class LoginIn(Schema):
    contact_no: str

class Institute(Schema):
    id: str
    name: str

class LoginOut(Schema):
    first_name: str
    last_name: str
    email : str
    contact_no: str 
    address :str
    profile_imge: str
    status: str
    token: str
    
class InstituteOut(Schema):
    result: bool
    message: str

class InstituteListOut(Schema):
    result: bool
    data: List[Institute]
    message: str