from businessowner.schemas import *
from .helpers import *
from .models import *
from ninja import Router, Query
from .authentication import verify_token
from typing import List
from ninja.pagination import paginate, PaginationBase
from .paginator import CustomPagination
from .schemas import MonthFilter, ExamFilter


router = Router()


@router.post("/login", response={200: LoginOut, 400: dict})
def login(request, data: LoginIn):
    return perform_login(data)


@router.get("/institues", response={200: InstituteListOut, 400: dict, 401: dict})
@verify_token
def get_institute_list(request):
    return get_class_list(request.user)


@router.post("/institues", response={200: InstituteOut, 400: dict, 401: dict})
@verify_token
def select_institute(request, data:ClassSelectIn):
    return select_class(request.user, data)


@router.post("/languageSelect", response={200: LanguageOut, 400: dict, 401: dict})
@verify_token
def select_language(request, data:LanguageSelectIn):
    return select_lan(request.user, data)



#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------USER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/profile", response={200: ProfileOut, 400: dict, 401: dict})
@verify_token
def get_user_profile(request, query:MonthFilter = Query(...)):
    return get_profile(request.user, query)


@router.put("/profile", response={200: ProfileOut, 400: dict, 401: dict})
@verify_token
def update_user_profile(request, data:ProfileUpdate):
    return update_profile(request.user, data)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------DASHBOARD--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/dashboard", response={200: dict, 400: dict, 401: dict})
@verify_token
def get_dashboard(request):
    return dashboard(request.user)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------------NEWS----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/news", response={200: List[NewsOut], 400: dict, 401: dict})
@paginate(CustomPagination)
@verify_token
def get_user_news(request):
    return get_news(request.user)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------TERMS & CONDITION-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/termsAndPolicy", response={200: TermsOut, 400: dict, 401: dict})
@verify_token
def get_terms(request):
    return get_termsandcondtion(request.user)


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------EXAM-----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/examHistory", response={200: List[ExamDetail], 400: dict, 401: dict})
@verify_token
@paginate(CustomPagination)
def get_examlist(request, query:ExamFilter = Query(...)):
    return get_exam_history(request.user, query)


@router.get("/examDetail/{exam_id}", response={200: dict, 400: dict, 401: dict})
@verify_token
def get_exam(request, exam_id ):
    return get_exam_detail(request.user, exam_id)


@router.get("/examDetailQuestion/{exam_id}", response={200: ExamDetailModel, 400: dict, 401: dict})
@verify_token
def get_exam(request, exam_id, subject_id=None): 
    if not subject_id:
        return {"error": "Subject ID is required"} 
    return get_exam_detail_question(request.user, exam_id, subject_id)