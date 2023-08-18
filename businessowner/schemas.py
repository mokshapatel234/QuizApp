from ninja import Schema, UploadedFile
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class CitySchema(Schema):
    city_id: str
    city_name: str
    state_id: str
    state_name: str


class LoginIn(Schema):
    email: str
    password: str

class Login(Schema):
    id: str
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
    city: CitySchema
    is_reset: bool
    token: str

class LoginOut(Schema):
    result:bool
    data: Login
    message: str
    


class ChangePasswordIn(Schema):
    old_password: str
    new_password: str

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

class PlanSchemaOut(Schema):
    result: bool
    data: PlanSchemaIn
    message: str

class PurchaseHistory(Schema):
    plan_name: str
    order_id: str
    status: str
    purchase_date: datetime

class PurchaseHistoryOut(Schema):
    result: bool
    data: PurchaseHistory
    message: str

class BusinessOwnerIn(Schema):
    business_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str] 
    email: Optional[str]  
    address: Optional[str]  
    tuition_tagline: Optional[str]  
    city: Optional[UUID]  
    logo: Optional[str]  
    status: Optional[str]  


class BusinessOwner(Schema):
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


class BusinessOwnerOut(Schema):
    result: bool
    data: BusinessOwner
    message: str 


####################################################################################################
####---------------------------------------COMPETITIVE------------------------------------------####
####################################################################################################


class DeleteOut(Schema):
    result: bool
    message: str


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class BatchIn(Schema):
    batch_name :str

class BatchUpdate(Schema):
    batch_name: Optional[str] 
    status: Optional[str]

class Batch(Schema):
    id: str 
    batch_name: str
    status: str 
    business_owner_id: str
    business_owner_name: str 
    status: str 
    created_at: datetime  
    updated_at: datetime 

class BatchOut(Schema):
    result: bool
    data: Batch
    message: str 

class BatchListout(Schema):
    result: bool
    data: List[Batch]
    message: str 

class BatchFilter(Schema):
    status: Optional[str]


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE SUBJECT----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class CompSubjectIn(Schema):
    subject_name :str

class CompSubjectUpdate(Schema):
    subject_name: Optional[str] 
    status: Optional[str] 

class CompSubject(Schema):
    id: str 
    subject_name: str
    status: str 
    business_owner_id: str
    business_owner_name: str 
    status: str 
    created_at: datetime  
    updated_at: datetime 


class CompSubjectOut(Schema):
    result: bool
    data: CompSubject
    message: str 


class CompSubjectListOut(Schema):
    result: bool
    data: List[CompSubject]
    message: str 


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE CHAPTER----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class CompChapterIn(Schema):
    subject_id: UUID
    chapter_name: str
    batches: list[UUID]
  
class CompChapterUpdate(Schema):
    subject_id: Optional[UUID]  
    chapter_name: Optional[str] 
    batches: list[UUID] =None
    status: Optional[str]  


class CompChapterFilter(Schema):
    status: Optional[str]
    batch: Optional[UUID]
    subject: Optional[UUID]

class ChapterBatch(Schema):
    id: str
    batch_name: str

class CompChapter(Schema):
    id: str
    chapter_name: str 
    subject_id: str 
    subject_name: str 
    batches: List[ChapterBatch]
    status: str 
    created_at: datetime  
    updated_at: datetime 


class CompChapterOut(Schema):
    result: bool
    data: CompChapter
    message: str 

class CompChapterListOut(Schema):
    result: bool
    data: List[CompChapter]
    message: str 


#-----------------------------------------------------------------------------------------------------------#
#-----------------------------------------COMPETITIVE QUESTIONS---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class Optionschema(Schema):
    option1: str
    option2: str
    option3: Optional[str]
    option4: Optional[str]

class QuestionIn(Schema):
   question: str
   options: Optionschema
   answer: str 
   chapter: UUID
   question_category: str
   marks: int
   time: str


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------STUDENT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class StudentIn(Schema):
    first_name: str
    last_name: str
    email: str
    contact_no: str
    parent_name: str
    parent_contact_no: str
    profile_image: Optional[str]  
    address: Optional[str]  
    batch: Optional[UUID]  
    standard: Optional[UUID]  

class StudentUpdate(Schema):
    first_name: Optional[str]  
    last_name: Optional[str]  
    email: Optional[str]  
    contact_no: Optional[str]  
    parent_name: Optional[str]  
    parent_contact_no: Optional[str]  
    profile_image: Optional[str]  
    address: Optional[str]  
    batch: Optional[UUID]  
    standard: Optional[UUID] 
    status: Optional[str] 

class StudentFilter(Schema):
    status: Optional[str]
    batch: Optional[UUID]
    board: Optional[UUID]
    medium: Optional[UUID]
    standard: Optional[UUID]

class Competitive(Schema):
    batch: str =None
    batch_name: str =None

class Academic(Schema):
    board: str =None
    board_name: str =None
    medium: str =None
    medium_name: str =None
    standard: str =None
    standard_name: str =None

class Student(Schema):
    id: str
    first_name: str
    last_name: str
    email: str
    contact_no: str
    parent_name: str
    parent_contact_no: str
    profile_image: str =None
    address: str =None
    competitive: Competitive =None
    academic: Academic =None


class StudentOut(Schema):
    result: bool
    data: Student
    message: str

class StudentListOut(Schema):
    result: bool
    data: List[Student]
    message: str















































































































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