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


@router.post("/forgotPassword", response={200:dict, 400: dict, 401: dict})
def forgot_password(request, data: ForgotPasswordIn):
    return perform_forgot_password(data)


@router.get("/resetPasswordLink/{token}", response={200:dict, 400: dict, 401: dict})
def reset_password_link(request, token):
    return verify_reset_password_link(token)


@router.post("/resetPassword", response={200:dict, 400: dict, 401: dict})
def reset_password_link(request, data: ResetPasswordIn):
    return perform_reset_password(data)


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------CITY & STATE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/city", response={200: CitySchemaResponse, 400: dict, 401: dict})
@verify_token
def get_city(request):
    return get_citylist(request) 


@router.get("/state", response={200: StateSchemaResponse, 400: dict, 401: dict})
@verify_token
def get_state(request):
    return get_statelist(request) 


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------PLAN PURCHASE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/planPurchase", response={200: PlanSchemaResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_plans(request):
    return get_plan_list(request)


@router.post("/planPurchase", response={200: dict, 400: dict, 401: dict})
@verify_token
def purchase_plans(request, data: PurchasePlanIn):
    return purchase_plan(data, request.user)


@router.post("/verifyPayment", response={200: dict, 400: dict, 401: dict})
@verify_token
def verify_payment(request, data: PurchasePlanIn):
    return verify_plan_payment(data, request.user)


@router.get("/purchaseHistory", response={200: PurchaseHistoryOutResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def purchase_history(request):
    return get_purchase_history(request)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------DASHBOARD--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/dashboard", response={200: dict, 400: dict, 401: dict})
@verify_token
def get_dashboard(request):
    return dashboard(request.user)


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
#---------------------------------------------------NEWS----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

@router.post("/news", response={200: NewsOut, 400: dict, 401: dict})
@verify_token
def add_business_news(request, data: NewsIn):
    return add_news(data, request.user)


@router.get("/news", response={200: NewsResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_business_news_list(request):
    return get_news_list(request)


@router.get("/news/{news_id}",  response={200: NewsOut, 400: dict, 401: dict})
@verify_token
def get_business_news(request, news_id):
    return get_news(news_id, request.user)


@router.patch("/news/{news_id}",  response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def update_business_news(request, news_id, data:NewsUpdateIn):
    return update_news(news_id, data)


@router.delete("/news/{news_id}",  response={200: dict, 400: dict, 401: dict})
@verify_token
def delete_business_news(request, news_id):
    return delete_news(news_id)
    
    
#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/batch", response={200: BatchOut, 400: dict, 401: dict})
@verify_token
def add_competitive_batch(request, data: BatchIn):
    return add_batch(data, request.user)


@router.get("/competitive/batch",  response={200: BatchResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_competitive_batchlist(request, query:BatchFilter = Query(...)):
    return get_batchlist(request, query)


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


@router.get("/competitive/subject",  response={200: CompSubjectResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_competitive_subjectlist(request, query:BatchFilter = Query(...)):
    return get_comp_subjectlist(request, query)


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
    

@router.get("/competitive/chapter", response={200:dict, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_competitive_chapterlist(request, query:CompChapterFilter = Query(...)):
    return get_comp_chapterlist(request, query)


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


@router.post("/competitive/question", response={200: CompQuestionOut, 400: dict, 401: dict})
@verify_token
def add_competitive_question(request, data: QuestionIn):
    return add_comp_question(request.user,data)
    

@router.get("/competitive/question", response={200: dict, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_competitive_questionlist(request, query:CompQuestionFilter = Query(...)):
    return get_comp_questionlist(request, query)


@router.get("/competitive/question/{question_id}", response={200: CompQuestionOut, 400: dict, 401: dict})
@verify_token
def get_competitive_question(request, question_id):
    return get_comp_question(request.user, question_id)


@router.patch("/competitive/question/{question_id}",  response={200: CompQuestionOut, 400: dict, 401: dict})
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


@router.post("/competitive/startExam", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def start_competitive_exam(request, data:CompExamQuestion):
    return start_comp_exam(data)


@router.get("/competitive/exam", response={200: CompExamOutResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_competitive_examlist(request, query:CompExamFilter = Query(...)):
    return get_comp_examlist(request, query)


@router.post("/competitive/CreateExam", response={200: AcadeCreatestartExamOut, 400: dict, 401: dict})
@verify_token
def start_CompExam(request, data:CompCreatestartExam):
    return start_comp_CompExam(request.user,data)

#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------STUDENT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/student", response={200: StudentOut, 400: dict, 401: dict})
@verify_token
def add_student(request, data: StudentIn):
    return create_student(data, request.user)


@router.post("/student/import-data", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def upload_studentfile(request, xl_file: UploadedFile = File(...)):
    return upload_student(xl_file, request.user)

@router.post("/student/download-data-format", response={200: dict, 400: dict, 401: dict})
@verify_token
def download_student_file(request,flag: str = Query(...),related_id: StudentdData = Query(...)):
    if flag not in ["standard","batch"]:
        return JSONResponse(content={"message": "Invalid flag."}, status_code=400)
    result = create_excel_with_column_names_student("output.xlsx",flag,related_id)
    return result

@router.get("/student", response={200: StudentResponse, 400: dict, 401: dict})
@verify_token
# @paginate(CustomPagination)
def get_student_list(request, query: StudentFilter = Query(...)):
    return student_list(request, query)


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


# @router.get("/competitive/examReport", response={200: List[dict], 400: dict, 401: dict})
# @verify_token
# @paginate(CustomPagination)
# def get_competitive_examreport(request, query:CompExamFilter = Query(...)):
#     return get_comp_examreport(request.user, query)


