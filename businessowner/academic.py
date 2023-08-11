from .views import router
from .helpers import *

@router.get("/academic/board", response={200: dict})
def get_competitive_batch(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return create_owner_response(user, True, "Owner retrieved successfully")