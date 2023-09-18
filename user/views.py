from businessowner.schemas import *
from .heplers import *
from .models import *
from ninja import Router, Query
from .authentication import verify_token
from typing import List
from ninja.files import UploadedFile
from ninja.pagination import paginate, PaginationBase
from .paginator import CustomPagination


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


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------USER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/profile", response={200: ProfileOut, 400: dict, 401: dict})
@verify_token
def get_user_profile(request):
    return get_profile(request.user)


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