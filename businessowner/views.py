from django.shortcuts import render
from django.http import JsonResponse
from businessowner.schemas import *
from .utils import generate_token
from ninja import NinjaAPI
from .helpers import *
from .models import *
from .authentication import JWTAuthentication

ownerapi = NinjaAPI()


@ownerapi.post("/login", response={200: LoginOut, 401: dict})
async def login(request, login_data: LoginIn):
    is_valid, message, user_id = await verify_user_credentials(login_data.email, login_data.password)
    
    if is_valid:
        token = generate_token(user_id)  # Generate the token here
        return create_login_response(login_data, is_valid, message, token)
    else:
        return create_login_response(login_data, is_valid, message)


@ownerapi.post("/changePassword", response={200: ChangePasswordOut, 400: dict, 401: dict})
def change_password(request, change_data: ChangePasswordIn):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    result = perform_change_password(change_data)
    response = generate_change_password_response(result)
    
    if not result["result"]:
        return JsonResponse(response, status=401)  
        
    return JsonResponse(response)


@ownerapi.post("/forgotPassword", response={400: dict, 401: dict})
def forgot_password(request):
    pass

@ownerapi.get("/planPurchase", response={200: dict, 400: dict, 401: dict})
def plan_purchase(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    print(user)
    return get_plan_purchase_response()


@ownerapi.get("/purchaseHistory", response={200: dict, 400: dict, 401: dict})
def purchase_history(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return get_purchase_history_response(user)


@ownerapi.get("/businessOwner", response={200: dict})
def get_business_owner(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return create_owner_response(user, True, "Owner retrieved successfully")

