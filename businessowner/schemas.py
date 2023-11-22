from ninja import Schema
from datetime import datetime
from typing import Optional,List,Dict
from uuid import UUID

class PaginationInfo(Schema):
    page: int
    total_docs: int
    total_pages: int
    per_page: int

class CitySchema(Schema):
    city_id: str
    city_name: str
    state_id: str
    state_name: str

class CitySchemaResponse(Schema):
    result: bool
    data: List[CitySchema]
    message: str
    pagination: PaginationInfo

class StateSchema(Schema):
    state_id: str
    state_name: str

class StateSchemaResponse(Schema):
    result: bool
    data: List[StateSchema]
    message: str
    pagination: PaginationInfo

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
    logo: Optional[str] 
    tuition_tagline: Optional[str]
    status: str
    city: CitySchema
    is_reset: bool
    is_plan_purchased: bool
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

class ResetPasswordIn(Schema):
    token: str
    new_password: str
    confirm_password: str

class PlanSchema(Schema):
    id: str
    plan_name: str
    description: str
    price: float
    validity: int
    image: Optional[str]
    status: str


class PlanSchemaResponse(Schema):
    result: bool
    data: List[PlanSchema]
    message: str
    pagination: PaginationInfo

class PurchasePlanIn(Schema):
    id: str


class PurchaseHistoryOut(Schema):
    plan_name: str
    order_id: str
    status: str
    purchase_date: datetime


class PurchaseHistoryOutResponse(Schema):
    result: bool
    data: List[PurchaseHistoryOut]
    message: str
    pagination: PaginationInfo

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
    logo: Optional[str]
    tuition_tagline: Optional[str]
    status: str
    created_at: datetime
    city: CitySchema


class BusinessOwnerOut(Schema):
    result: bool
    data: BusinessOwner
    message: str 


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------------NEWS----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
import uuid

class NewsIn(Schema):
    standard: Optional[UUID]
    batch: Optional[UUID]
    text: Optional[str]
    image: Optional[str] 

class NewsUpdateIn(Schema):
    text: Optional[str]
    image: Optional[str] 
    standard : Optional[uuid.UUID]
    batch : Optional[uuid.UUID]
    status: Optional[str]

class News(Schema):
    id: str
    text: Optional[str]
    image: Optional[str] 
    standard : Optional[UUID]
    batch : Optional[UUID]
    status: str

class NewsResponse(Schema):
    result: bool
    data: List[News]
    message: str
    pagination: PaginationInfo

class NewsOut(Schema):
    result: bool
    data: News
    message: str


#############################################################################################################
####--------------------------------------------COMPETITIVE----------------------------------------------####
#############################################################################################################


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

class BatchResponse(Schema):
    result: bool
    data: List[Batch]
    message: str
    pagination: Optional[PaginationInfo]

class BatchOut(Schema):
    result: bool
    data: Batch
    message: str 

class BatchFilter(Schema):
    status: Optional[str]
    search: Optional[str]
    chapter_id: Optional[str]
    all_data : Optional[bool]


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

class CompSubjectResponse(Schema):
    result: bool
    data: List[CompSubject]
    message: str
    pagination: Optional[PaginationInfo]

class CompSubjectOut(Schema):
    result: bool
    data: CompSubject
    message: str 


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE CHAPTER----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class CompChapterIn(Schema):
    subject_id: UUID
    chapter_name: str
    batches: List[UUID]
  
class CompChapterUpdate(Schema):
    subject_id: Optional[UUID]  
    chapter_name: Optional[str] 
    batches: List[UUID] =None
    status: Optional[str]  


class CompChapterFilter(Schema):
    status: Optional[str]
    batch_id: Optional[str]
    subject_id: Optional[str]
    search: Optional[str]
    subject_ids: Optional[str]
    all_data : Optional[bool]

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

class CompChapterResponse(Schema):
    result: bool
    data: List[CompChapter]
    message: str
    pagination: PaginationInfo

class CompChapterOut(Schema):
    result: bool
    data: CompChapter
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
   time: float

class CompQuestionFilter(Schema):
    status: Optional[str]
    chapter_id: Optional[str]
    subject_id: Optional[str]
    batch_id: Optional[str]
    question_category: Optional[str]
    search: Optional[str]
    all_data : Optional[bool]
    
class OptionUpdateSchema(Schema):
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    option4: Optional[str]

class QuestionUpdate(Schema):
   question: Optional[str]
   question_image: Optional[str]
   options: Optional[OptionUpdateSchema]
   answer: Optional[str] 
   chapter_id: Optional[str]
   question_category: Optional[str]
   marks: Optional[int]
   time: Optional[str]
   status: Optional[str]

class CompetitiveQuestion(Schema):
    id: str
    question: str
    question_image: Optional[str]
    options: Optionschema
    answer: str 
    chapter_id: str
    chapter_name: str
    subject_id: str
    subject_name: str
    batches: List[ChapterBatch]
    question_category: str
    marks: int
    time: str
    status: str
    created_at: datetime  
    updated_at: datetime 


class CompQuestionOut(Schema):
    result: bool
    data: CompetitiveQuestion
    message: str


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------COMPETITIVE EXAM-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class CompExamData(Schema):
    subject_id: UUID
    chapter: List[UUID]
    easy_question: int
    medium_question: int
    hard_question: int

class CompExamIn(Schema):
    exam_title: str
    batch_id: UUID
    total_questions: int
    time_duration: float
    negative_marks: str
    passing_marks: int
    total_marks: int
    option_e: bool
    exam_data: List[CompExamData]


class CompExamFilter(Schema):
    batch_id: Optional[str]
    subject_id: Optional[str]
    chapter_id: Optional[str]
    search: Optional[str]

class CompExam(Schema):
    id: str
    question:str
    question_image:Optional[str]
    question_category: str
    time: float
    mark: int
    options: Optionschema
    answer: str 
    subject: str

class CompExamQuestion(Schema):
    exam_id: UUID

class CompExamChapter(Schema):
    # id: UUID
    chapter_name: str
class Exammm(Schema):
    subject: str
    chapters: str

class CompExamOut(Schema):
    id:str
    exam_title: str
    batch: str  
    batch_name: str
    total_question:int
    time_duration: float
    negative_marks: str
    total_marks:int
    start_date: Optional[datetime]
    exam_datas: List[Exammm]


class CompExamOutResponse(Schema):
    result: bool
    data: List[CompExamOut]
    message: str
    pagination: PaginationInfo
    

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
    batch_id: Optional[str]  
    standard_id: Optional[str]  

class StudentUpdate(Schema):
    first_name: Optional[str]  
    last_name: Optional[str]  
    email: Optional[str]  
    contact_no: Optional[str]  
    parent_name: Optional[str]  
    parent_contact_no: Optional[str]  
    profile_image: Optional[str]  
    address: Optional[str]  
    batch_id: Optional[UUID]  
    standard_id: Optional[UUID] 
    status: Optional[str] 

class StudentFilter(Schema):
    status: Optional[str]
    batch_id: Optional[str]
    board_id: Optional[str]
    medium_id: Optional[str]
    standard_id: Optional[str]
    search: Optional[str]
    all_data : Optional[bool]

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
    # status: str
    competitive: Optional[Competitive] 
    academic: Optional[Academic] 

class StudentResponse(Schema):
    result: bool
    data: List[Student]
    message: str
    pagination: Optional[PaginationInfo]

class StudentOut(Schema):
    result: bool
    data: Student
    message: str



class AcadeCreatestartExamOut(Schema):
    result: bool
    message: str
    exam_id : UUID

class AcadExamData(Schema):
    subject_id: UUID
    chapters: List[UUID]
    easy_question: int
    medium_question: int
    hard_question: int

class subjectinfo(Schema):
    subject_id: UUID
    subject_time: int
    subject_marks: int


class CompExamData(Schema):
    subject_id: UUID
    chapter: List[UUID]
    easy_question: int
    medium_question: int
    hard_question: int

class CompCreatestartExam(Schema):
    exam_title: str
    batch_id: UUID
    total_questions: int
    time_duration: float
    negative_marks: str
    passing_marks: int
    total_marks: int
    option_e: bool
    question:List[UUID]
    exam_data: List[CompExamData]
    subject_data: List[subjectinfo]
    

#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------REPORT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class ReportFilter(Schema):
    batch_id: Optional[str]
    board_id: Optional[str]
    medium_id: Optional[str]
    standard_id: Optional[str]
    subject_id: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]


class PdfDownload(Schema):
    generate_pdf: bool


























































































































































































































####################################################################################
####--------------------------------ACADEMIC------------------------------------####
####################################################################################


class DeleteOut(Schema):
    result: bool
    message: str


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------BOARD----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class AcademicBoardSchema(Schema):
    id: str
    board_name: str
    business_owner: str
    status: str
    created_at: datetime
    updated_at: datetime

class BoardsListResponse(Schema):
    result: bool
    data: List[AcademicBoardSchema]
    message: str
    pagination: Optional[PaginationInfo]

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
    
    standard_id : Optional[str]
    search : Optional[str]
    status : Optional[str] 
    board_id : Optional[str]
    medium_id : Optional[str]
    subject_id : Optional[str]
    chapter_id : Optional[str]
    subject_ids: Optional[str]
    all_data : Optional[bool]

class AcademicBoardOut(Schema):
    result: bool
    data: AcademicBoardSchema=None
    message: str 

class BoardUpdateSchemaOut(Schema):
    result: bool
    data: AcademicBoardSchema
    message: str 


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------MEDIUM----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class AcademicMedium(Schema):
    id: str = None
    medium_name: str = None
    board_id: str = None 
    board_name: str = None
    status: str = None
    created_at: datetime  = None
    updated_at: datetime = None


class AcademicMediumResponse(Schema):
    result: bool
    data: List[AcademicMedium]
    message: str
    pagination: Optional[PaginationInfo]

class AddAcademicMediumIn(Schema):
    medium_name: str
    board_id: str

class AddAcademicMediumOut(Schema):
    result: bool
    data: AcademicMedium
    message: str 

class updateMediumIn(Schema):
    medium_name: Optional[str]
    board_id: Optional[str]
    status: Optional[str] 

class UpdateAcademicMediumOut(Schema):
    result: bool
    data: AcademicMedium
    message: str 


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------STANDARD--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class AcademicStandard(Schema):
    id: Optional[str]
    standard : Optional[str]
    medium_id: Optional[str]
    medium_name: Optional[str]
    board_id : Optional[str]
    board_name : Optional[str]
    status : Optional[str]
    created_at : Optional[datetime]
    updated_at : Optional[datetime]

class AcademicStandardResponse(Schema):
    result: bool
    data: List[AcademicStandard]
    message: str
    pagination: Optional[PaginationInfo]

class AcademicStandardOut(Schema):
    result : bool
    data : AcademicStandard
    message : str

class AcademicStandardIn(Schema):
    standard : Optional[str]
    medium_id: Optional[str]


class updateStandardIn(Schema):
    standard: Optional[str]
    medium_id: Optional[str]
    status: Optional[str] 


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------SUBJECT--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class AcademicSubject(Schema):
    id: Optional[str]
    subject_name : Optional[str]
    board_id: Optional[str]
    board_name: Optional[str]
    medium_id: Optional[str]
    medium_name: Optional[str]
    standard_id: Optional[str]
    standard: Optional[str]
    status : Optional[str]
    created_at : Optional[datetime]
    updated_at : Optional[datetime]

class AcademicSubjectResponse(Schema):
    result: bool
    data: List[AcademicSubject]
    message: str
    pagination: Optional[PaginationInfo]

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
    standard_id: Optional[str]
    status: Optional[str] 


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------CHAPTER--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class AcademicChapter(Schema):
    id: Optional[str]
    chapter_name : Optional[str]
    board_id: Optional[str]
    board_name: Optional[str]
    medium_id: Optional[str]
    medium_name: Optional[str]
    standard_id: Optional[str]
    standard: Optional[str]
    subject_id: Optional[str]
    subject_name: Optional[str]
    status : Optional[str]
    created_at : Optional[datetime]
    updated_at : Optional[datetime]


class AcademicChapterResponse(Schema):
    result: bool
    data: List[AcademicChapter]
    message: str
    pagination: PaginationInfo

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
    subject_id: Optional[str]
    status: Optional[str] 


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------QUESTION--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class Question(Schema):
    id : str
    question: str
    question_image: Optional[str]
    options: Optionschema
    answer: str 
    board_id: str
    board_name: str
    medium_id: str
    medium_name: str
    standard_id: str
    standard_name: str
    subject_id: str
    subject_name: str
    chapter_id: str
    chapter_name: str
    question_category: str
    marks: str
    time: str
    status: str
    created_at: datetime  
    updated_at: datetime 

class Optionschema(Schema):
    option1: str
    option2: str
    option3: Optional[str]
    option4: Optional[str]

class QuestionIn(Schema):
   question: str
   question_image: Optional[str]
   options: Optionschema
   answer: str 
   chapter_id: UUID
   question_category: str
   marks: int
   time: float


class QuestionOut(Schema):
    result: bool
    data: Question
    message: str

class QuestionListOut(Schema):
    result: bool
    data: List[Question]
    message: str


class UpdateQuestionIn(Schema):
   question: Optional[str]
   question_image: Optional[str]
   options: Optional[Optionschema]
   answer: Optional[str] 
   chapter_id: Optional[UUID]
   question_category: Optional[str]
   marks: Optional[int]
   time: Optional[str]
   status: Optional[str]

class PresignedUrl(Schema):
    file_name: str
#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------------EXAM----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class AcademicExamChapter(Schema):
    id: UUID
    chapter_name: str

class AcadExam(Schema):
    id: str
    question:str
    question_image: Optional[str]
    question_category: str
    time: float
    mark: int
    options: Optionschema
    answer: str
    subject: str
    

class AcadExamData(Schema):
    subject_id: UUID
    chapter: List[UUID]
    easy_question: int
    medium_question: int
    hard_question: int

class AcademicExamIn(Schema):
    exam_title: str
    standard_id: UUID
    total_questions: int
    time_duration: float
    negative_marks: str
    passing_marks: int
    total_marks: int
    option_e: bool
    exam_data: List[AcadExamData]


class AcadExamFilter(Schema):
    standard: Optional[str]
    subject: Optional[str]
    chapter: Optional[str]
    search: Optional[str]


class AcadExamQuestion(Schema):
    exam_id:UUID


class AcadeExamOut(Schema):
    id:str
    exam_title: str
    board_id: str
    board_name: str
    medium_id:str
    medium_name: str
    standard_id: str
    standard_name: str
    total_question:int
    time_duration: float
    negative_marks:float
    total_marks:int
    start_date: datetime
    exam_data: List[Exammm]



class   QuestionItem(Schema):
    id: UUID
    question: str
    question_category: str
    time: float
    mark: int
    options: Dict[str, str]
    answer: str
    subject: str

class subjectinfo(Schema):
    subject_id: UUID
    subject_time: int
    subject_marks: int
    
class AcadeCreatestartExam(Schema):
    exam_title: str
    standard_id: UUID
    total_questions: int
    time_duration: float
    negative_marks: str
    passing_marks: int
    total_marks: int
    option_e: bool
    question:List[UUID]
    exam_data: List[AcadExamData]
    subject_data: List[subjectinfo]

class AcadeCreatestartExamOut(Schema):
    result: bool
    message: str
    exam_id : UUID

class UploadData(Schema):
     board_id: Optional[UUID] = None
     medium_id: Optional[UUID]
     standard_id: Optional[UUID]
     subject_id: Optional[UUID]
     chapter_id: Optional[UUID]
     competitive_subject_id: Optional[UUID]
     competitive_chapter_id: Optional[UUID]


class DownloadData(Schema):
     board_id: Optional[str] = None
     medium_id: Optional[str]
     standard_id: Optional[str]
     subject_id: Optional[str]
     subject_ids: Optional[str]
     chapter_id: Optional[str]
     competitive_subject_id: Optional[str]
     competitive_chapter_id: Optional[str]
     batch_ids: Optional[str]



class StudentdData(Schema):
     batch_id: Optional[str]
     standard_id: Optional[str]



class Exammm(Schema):
    subject: str
    chapters: str

class AcadExamOut(Schema):
    id:str
    exam_title: str
    board_id: str
    board_name: str
    medium_id:str
    medium_name: str
    standard_id: str
    standard_name: str
    total_question:int
    time_duration: float
    negative_marks: str
    total_marks:int
    exam_data: List[Exammm]

class AcadExamOutResponse(Schema):
    result: bool
    data: List[AcadExamOut]
    message: str
    pagination: PaginationInfo