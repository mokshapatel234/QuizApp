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
def select_institute(request):
    return select_class(request.user)
