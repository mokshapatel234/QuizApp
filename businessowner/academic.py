# from .views import router
from .helpers import *
from uuid import UUID 
from django.http import JsonResponse
from ninja import Router

router = Router()

@router.get("/academic/boards", response={200:AcademicBoardSchema, 401:dict})
def get_academic_boards(request):
    user, error_response = authenticate_with_jwt_token(request)
    
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = get_boards(user)
    
    return result

    
@router.post("/academic/addBoard", response={201: BoardSchema, 401: dict})
def add_boards(request,data: BoardSchema):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = add_baord(user,data)
    return result


@router.patch("/academic/updateBoard", response={200: BoardUpdateSchema, 401: dict})
def update_board(request, board_id: UUID, data: BoardUpdateSchema):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    result = update_board_data(user,data,board_id)
    return result
    

@router.delete("/academic/deleteBoard")
def delete_board(request, board_id):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = delete_board_data(user,board_id)
    return result



@router.get("/academic/medium", response={200:AcademicMedium, 401:dict})
def get_academic_medium(request):
    user, error_response = authenticate_with_jwt_token(request)
    
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = get_academic_mediums()
    
    return result



@router.post("/academic/addmedium", response={201: AddAcademicMedium, 401: dict})
def add_medium(request,data: AddAcademicMedium):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = add_medium_data(user, data.dict())  # Call the appropriate function
    return result


@router.patch("/academic/updateMedium", response={200: updateMedium, 401: dict})
def update_medium(request, medium_id: UUID, data: updateMedium):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    result = update_medium_data(user,data,medium_id)
    return result
    