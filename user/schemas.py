from ninja import Schema
from datetime import datetime
from typing import Optional,List
from uuid import UUID

class LoginIn(Schema):
    contact_no: str

class Institute(Schema):
    id: str
    name: str
    type:str

class Login(Schema):
    first_name: str
    last_name: str
    email : str
    contact_no: str 
    address :str
    profile_imge: Optional[str]
    status: str
    token: str

class LoginOut(Schema):
    result: bool
    data: Login
    message: str
    
class ClassSelectIn(Schema):
    id: UUID

class InstituteOut(Schema):
    result: bool
    data: Institute
    message: str

class InstituteListOut(Schema):
    result: bool
    data: List[Institute]
    message: str


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------USER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class Profile(Schema):
    id: str
    first_name: str
    last_name: str
    email: str
    contact_no : str
    profile_image: Optional[str]

class ProfileOut(Schema):
    result: bool
    data: Profile
    message: str


class ProfileUpdate(Schema):
    email: Optional[str]
    profile_image: Optional[str]

