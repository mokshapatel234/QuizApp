from ninja import Schema
from datetime import datetime
from typing import Optional,List,Dict, Union
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
    selected_language: str
    token: str

class LoginOut(Schema):
    result: bool
    data: Login
    message: str
    
class ClassSelectIn(Schema):
    id: UUID

class LanguageSelectIn(Schema):
    language: str

class InstituteOut(Schema):
    result: bool
    data: Institute
    message: str

class InstituteListOut(Schema):
    result: bool
    data: List[Institute]
    message: str


class Language(Schema):
    id: str
    selected_language: str

class LanguageOut(Schema):
    result: bool
    data: Language
    message: str    

#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------USER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class Profile(Schema):
    id: str
    first_name: str
    last_name: str
    email: str
    contact_no: str
    profile_image: Optional[str]
    selected_language: str
    total_exams:Optional[int]
    passed_exams:Optional[int]
    failed_exams:Optional[int]
    
class ProfileOut(Schema):
    result: bool
    data: Profile
    message: str


class ProfileUpdate(Schema):
    email: Optional[str]
    profile_image: Optional[str]


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------------NEWS----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
class NewsOut(Schema):
    id: str
    text: Optional[str]
    image: Optional[str] 
    standard : Optional[UUID]
    batch : Optional[UUID]
    status: str
    is_image: bool
    created_at: str
    updated_at: str


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------TERMS & CONDITION-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


class Terms(Schema):
    terms_and_condition: str
    privacy_policy: str

class TermsOut(Schema):
    result: bool
    data: Optional[Terms]
    message: str

class MonthFilter(Schema):
    month: Optional[int]

class ExamFilter(Schema):
    subject_id: Optional[str]
    month: Optional[int]
    year: Optional[int]
    search: Optional[str]

class ExamData(Schema):
    subject_id: Optional[str]
    subject: Optional[str]
    
class ExamDetail(Schema):
    id: Optional[str]
    exam_title: Optional[str]
    total_marks: Optional[int]
    start_date: Optional[str]
    exam_datas: Optional[List[ExamData]]
    result: Optional[str]


class OptionModel(Schema):
    option1: str
    option2: str
    option3: str
    option4: str

class QuestionModel(Schema):
    question_text: str
    question_image:Optional[str]
    subject_name: str
    right_answer: str
    options: OptionModel
    selected_answer: Optional[str]

class ExamDetailModel(Schema):
    easy_questions: List[QuestionModel]
    medium_questions: List[QuestionModel]
    hard_questions: List[QuestionModel]

class ExamDetailModelResponse(Schema):
    result: bool
    data: Optional[ExamDetailModel]
    message: str

class SubjectList(Schema):
    id: Optional[str]
    subject_name : Optional[str]

class SubjectListResponse(Schema):
    result: bool
    data: List[Optional[SubjectList]]
    message: str