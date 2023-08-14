# from .views import router
from .helpers import *

# @router.get("/academic/board", response={200: dict})
# def get_competitive_batch(request):
#     user, error_response = authenticate_with_jwt_token(request)
#     if error_response:
#         return JsonResponse(error_response, status=401)

#     return board_get_response(user, True, "Owner retrieved successfully")
from ninja import Router

router = Router()

@router.get("/academic/boards", response={200:AcademicBoardSchema, 401:dict})
def get_academic_boards(request):
    user, error_response = authenticate_with_jwt_token(request)
    
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = get_boards(user)
    
    return result