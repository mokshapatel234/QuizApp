from ninja import Schema, UploadedFile
from datetime import datetime
from pydantic import BaseModel
from typing import Optional,List
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
class DeleteOut(Schema):
    result: bool
    message: str

class AcademicBoardSchema(Schema):
    id: str
    board_name: str
    business_owner: str
    status: str
    created_at: datetime
    updated_at: datetime

class BoardSchema(Schema):
    board_name: str

class BoardUpdateSchema(Schema):
    board_name: str = None
    status : str = None

class AcademicBoardListOut(Schema):
    result: bool
    data: List[AcademicBoardSchema]
    message: str  

class AcademicFilter(Schema):
    status : Optional[str] 
    board_id : Optional[str]

class AcademicBoardOut(Schema):
    result: bool
    data: AcademicBoardSchema=None
    message: str 

class BoardUpdateSchemaOut(Schema):
    result: bool
    data: AcademicBoardSchema
    message: str 




class AcademicMedium(Schema):
    id: str = None
    medium_name: str = None
    board_id: str = None 
    board_name: str = None
    status: str = None
    created_at: datetime  = None
    updated_at: datetime = None

class AcademicMediumListOut(Schema):
    result: bool
    data: List[AcademicMedium]
    message: str  

class AddAcademicMediumIn(Schema):
    medium_name: str
    board_id: str

class AddAcademicMediumOut(Schema):
    result: bool
    data: AcademicMedium
    message: str 

class updateMediumIn(Schema):
    medium_name: Optional[str]
    board_name: Optional[str]
    status: Optional[str] 

class UpdateAcademicMediumOut(Schema):
    result: bool
    data: AcademicMedium
    message: str 







class AcademicStandard(Schema):
    id: Optional[str]
    standard : Optional[str]
    medium_id: Optional[str]
    medium_name: Optional[str]
    status : Optional[str]
    created_at : Optional[datetime]
    updated_at : Optional[datetime]

class AcademicStandardList(Schema):
    result : bool
    data : List[AcademicStandard]
    message : str

class AcademicStandardOut(Schema):
    result : bool
    data : AcademicStandard
    message : str

class AcademicStandardIn(Schema):
    standard : Optional[str]
    medium_id: Optional[str]


class updateStandardIn(Schema):
    standard_name: Optional[str]
    medium_name: Optional[str]
    status: Optional[str] 



class AcademicSubject(Schema):
    id: Optional[str]
    subject_name : Optional[str]
    standard_id: Optional[str]
    standard: Optional[str]
    status : Optional[str]
    created_at : Optional[datetime]
    updated_at : Optional[datetime]

class AcademicSubjectList(Schema):
    result : bool
    data : List[AcademicSubject]
    message : str


class AcademicSubjectOut(Schema):
    result : bool
    data : AcademicSubject
    message : str

class AcademicSubjectIn(Schema):
    subject_name : Optional[str]
    standard_id: Optional[str]


class updateSubjectIn(Schema):
    subject_name: Optional[str]
    standard: Optional[str]
    status: Optional[str] 



class AcademicChapter(Schema):
    id: Optional[str]
    chapter_name : Optional[str]
    subject_id: Optional[str]
    subject_name: Optional[str]
    status : Optional[str]
    created_at : Optional[datetime]
    updated_at : Optional[datetime]

class AcademicChapterList(Schema):
    result : bool
    data : List[AcademicChapter]
    message : str


class AcademicChapterIn(Schema):
    chapter_name : Optional[str]
    subject_id: Optional[str]

class AcademicChapterOut(Schema):
    result : bool
    data : AcademicChapter
    message : str


class updateChaptertIn(Schema):
    chapter_name:Optional[str]
    subject_name: Optional[str]
    status: Optional[str] 



# class AcademicQuestion(Schema):
#     id: Optional[str]
#     chapter_id : Optional[str]
#     question: Optional[str]
#     options: Optional[str]
#     answer : Optional[str]
#     question_category: Optional[str]
#     marks : Optional[int]
#     time_duration: Optional[datetime]
#     owner_id : Optional[str]
#     status: Optional[str]
#     created_at : Optional[datetime]
#     updated_at : Optional[datetime]



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