from django.shortcuts import render
from django.http import JsonResponse
from businessowner.schemas import *
from .utils import generate_token
from .helpers import *
from .models import *
from .authentication import JWTAuthentication
from ninja import Router
from ninja.errors import HttpError

router = Router()



@router.post("/login", response={200: LoginOut, 401: dict})
async def login(request, login_data: LoginIn):
    is_valid, message, user_id = await verify_user_credentials(login_data.email, login_data.password)
    
    if is_valid:
        token = generate_token(user_id)  # Generate the token here
        return create_login_response(login_data, is_valid, message, token)
    else:
        return create_login_response(login_data, is_valid, message)


@router.post("/changePassword", response={200: ChangePasswordOut, 400: dict, 401: dict})
def change_password(request, change_data: ChangePasswordIn):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = perform_change_password(change_data)
    response = generate_change_password_response(result)
    
    if not result["result"]:
        return JsonResponse(response, status=401)  
        
    return JsonResponse(response)


@router.post("/forgotPassword", response={400: dict, 401: dict})
def forgot_password(request):
    pass

@router.get("/planPurchase", response={200: dict, 400: dict, 401: dict})
def plan_purchase(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    print(user)
    return get_plan_purchase_response()


@router.get("/purchaseHistory", response={200: dict, 400: dict, 401: dict})
def purchase_history(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return get_purchase_history_response(user)


@router.get("/ownerProfile", response={200: dict})
def get_business_owner(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return create_owner_response(user, True, "Owner retrieved successfully")


@router.patch("/ownerProfile", response={200: dict})
def update_business_owner(request, data: BusinessOwnerIn):

    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    try:
        owner = BusinessOwners.objects.get(id=user.id)
        if owner:
            update_data = {field: value for field, value in data.dict().items() if value is not None}
            
            if update_data:
                update_owner_data(owner, update_data)
                updated_owner_data = create_owner_response(owner, True, message="Owner updated successfully")
                return updated_owner_data
            else:
                raise HttpError(400, "No fields to update")
        else:
            raise HttpError(404, "Owner not found")
    except BusinessOwners.DoesNotExist:
        return JsonResponse({"error": "Owner not found"}, status=404)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": "An error occurred"}, status=500)


@router.post("/competitive/batch", response={200: dict})
def add_competitive_batch(request, data: BatchIn):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    try:
        batch = CompetitiveBatches.objects.create(**data.dict())
        
        return JsonResponse({"message": "Batch created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@router.get("/competitive/batch",  response={200: dict, 400: dict, 401: dict})
def get_competitive_batch(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    return get_batches_response()