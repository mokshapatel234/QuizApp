from businessowner.schemas import *
from .helpers import *
from .models import *
from ninja import Router, Query
from .authentication import verify_token
from typing import List
from ninja.files import UploadedFile
from ninja.pagination import paginate, PaginationBase
from .paginator import CustomPagination


router = Router()

@router.post("/login", response={200: LoginOut, 401: dict})
def login(request, data: LoginIn):
    return perform_login(data)
   

@router.post("/changePassword", response={200: ChangePasswordOut, 400: dict, 401: dict})
@verify_token
def change_password(request, data: ChangePasswordIn):
    
    return perform_change_password(data, request.user) 


@router.post("/forgotPassword", response={400: dict, 401: dict})
def forgot_password(request):
    pass


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------CITY & STATE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/city", response={200: CityOut, 400: dict, 401: dict})
@verify_token
def get_city(request):
    return get_citylist() 


@router.get("/state", response={200: StateOut, 400: dict, 401: dict})
@verify_token
def get_state(request):
    return get_statelist() 


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------PLAN PURCHASE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/planPurchase", response={200: PlanSchemaOut, 400: dict, 401: dict})
@verify_token
def plan_purchase(request):
    return get_plan_purchase_response()


@router.get("/purchaseHistory", response={200: PurchaseHistoryOut, 400: dict, 401: dict})
@verify_token
def purchase_history(request):
    return get_purchase_history_response(request.user)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------OWNER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/ownerProfile", response={200: BusinessOwnerOut, 400: dict, 401: dict})
@verify_token
def get_business_owner(request):
    return create_owner_response(request.user, True, "Owner retrieved successfully")


@router.patch("/ownerProfile", response={200: BusinessOwnerOut, 400: dict, 401: dict})
@verify_token
def update_business_owner(request, data: BusinessOwnerIn):
    return update_owner_data(data, request.user)
    
    

#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/batch", response={200: BatchOut, 400: dict, 401: dict})
@verify_token
def add_competitive_batch(request, data: BatchIn):
    return add_batch(data, request.user)


@router.get("/competitive/batch",  response={200: List[Batch], 400: dict, 401: dict})
@verify_token
@paginate(CustomPagination)
def get_competitive_batchlist(request, query:BatchFilter = Query(...)):
    return get_batchlist(request.user, query)


@router.get("/competitive/batch/{batch_id}",  response={200: BatchOut, 400: dict, 401: dict})
@verify_token
def get_competitive_batch(request, batch_id):
    return get_batch(batch_id, request.user)


@router.patch("/competitive/batch/{batch_id}",  response={200: BatchOut, 400: dict, 401: dict})
@verify_token
def update_competitive_batch(request, batch_id, data: BatchUpdate):
    return update_batch(batch_id, data, request.user)


@router.delete("/competitive/batch/{batch_id}",  response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def delete_competitive_batch(request, batch_id):    
    return delete_batch(batch_id)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE SUBJECT----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/subject", response={200: CompSubjectOut, 400: dict, 401: dict})
@verify_token
def add_competitive_subject(request, data: CompSubjectIn):
    return add_comp_subect(data, request.user)


@router.get("/competitive/subject",  response={200: List[CompSubject], 400: dict, 401: dict})
@verify_token
@paginate(CustomPagination)
def get_competitive_subjectlist(request, query:BatchFilter = Query(...)):
    return get_comp_subjectlist(request.user, query)


@router.get("/competitive/subject/{subject_id}",  response={200: CompSubjectOut, 400: dict, 401: dict})
@verify_token
def get_competitive_subject(request, subject_id):
    return get_comp_subject(subject_id, request.user)


@router.patch("/competitive/subject/{subject_id}",  response={200: CompSubjectOut, 400: dict, 401: dict})
@verify_token
def update_competitive_subject(request, subject_id, data: CompSubjectUpdate):
    return update_comp_subject(subject_id, data, request.user)


@router.delete("/competitive/subject/{subject_id}",  response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def delete_competitive_subject(request, subject_id):
    return delete_comp_subject(subject_id)
    

#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE CHAPTER----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/chapter", response={200: CompChapterOut, 400: dict, 401: dict})
@verify_token
def add_competitive_chapter(request, data: CompChapterIn):
    return add_comp_chapter(data, request.user)
    

@router.get("/competitive/chapter", response={200: List[CompChapter], 400: dict, 401: dict})
@verify_token
@paginate(CustomPagination)
def get_competitive_chapterlist(request, query:CompChapterFilter = Query(...)):
    return get_comp_chapterlist(request.user, query)


@router.get("/competitive/chapter/{chapter_id}", response={200: CompChapterOut, 400: dict, 401: dict})
@verify_token
def get_competitive_chapter(request, chapter_id):
    return get_comp_chapter(request.user, chapter_id)


@router.patch("/competitive/chapter/{chapter_id}",  response={200: CompChapterOut, 400: dict, 401: dict})
@verify_token
def update_competitive_chapter(request, chapter_id, data: CompChapterUpdate):
    return update_comp_chapter(chapter_id, data, request.user)


@router.delete("/competitive/chapter/{chapter_id}",  response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def delete_competitive_chapter(request, chapter_id):
    return delete_comp_chapter(chapter_id)
    

#-----------------------------------------------------------------------------------------------------------#
#-----------------------------------------COMPETITIVE QUESTIONS---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/question", response={200: QuestionOut, 400: dict, 401: dict})
@verify_token
def add_competitive_question(request, data: QuestionIn):
    return add_comp_question(request.user,data)
    

@router.get("/competitive/question", response={200: List[Question], 400: dict, 401: dict})
@verify_token
@paginate(CustomPagination)
def get_competitive_questionlist(request, query:CompQuestionFilter = Query(...)):
    return get_comp_questionlist(request.user, query)


@router.get("/competitive/question/{question_id}", response={200: QuestionOut, 400: dict, 401: dict})
@verify_token
def get_competitive_question(request, question_id):
    return get_comp_question(request.user, question_id)


@router.patch("/competitive/question/{question_id}",  response={200: QuestionOut, 400: dict, 401: dict})
@verify_token
def update_competitive_question(request, question_id, data: QuestionUpdate):
    return update_comp_question(question_id, data)


@router.delete("/competitive/question/{question_id}",  response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def delete_competitive_question(request, question_id):
    return delete_comp_question(question_id)


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------COMPETITIVE EXAM-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

@router.post("/competitive/exam", response={200: dict, 400: dict, 401: dict})
@verify_token
def create_competitive_exam(request, data: CompExamIn):
    return create_comp_exam(request.user, data)

@router.post("/competitive/startExam/{exam_id}", response={200: dict, 400: dict, 401: dict})
@verify_token
def start_competitive_exam(request, exam_id, data:CompExamQuestion):
    return start_comp_exam(exam_id, data)


@router.get("/competitive/exam", response={200: List[dict], 400: dict, 401: dict})
@verify_token
def get_competitive_examlist(request, query:CompExamFilter = Query(...)):
    return get_comp_examlist(request.user, query)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------STUDENT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/student", response={200: StudentOut, 400: dict, 401: dict})
@verify_token
def add_student(request, data: StudentIn):
    return create_student(data, request.user)

@router.post("/student/upload", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def upload_studentfile(request, xl_file: UploadedFile = File(...)):
    return upload_student(xl_file, request.user)
 

@router.get("/student", response={200: StudentListOut, 400: dict, 401: dict})
@verify_token
def get_student_list(request, query: StudentFilter = Query(...)):
    return student_list(request.user, query)


@router.get("/student/{student_id}", response={200: StudentOut, 400: dict, 401: dict})
@verify_token
def get_student(request, student_id):
    return student_detail(student_id)


@router.patch("/student/{student_id}", response={200: StudentOut, 400: dict, 401: dict})
@verify_token
def update_student(request, student_id, data:StudentUpdate):
    return student_updation(student_id, data)

@router.patch("/student/uploads", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def update_studentfile(request, xl_file: UploadedFile = File(...)):
    return student_file_updation(xl_file, request.user)

@router.delete("/student/{student_id}", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def delete_student(request, student_id):
    return remove_student(student_id)
    

#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------REPORT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

