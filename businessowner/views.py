from django.shortcuts import render
from django.http import JsonResponse
from businessowner.schemas import *
# from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from .utils import generate_token
from .helpers import *
# Create your views here.

from ninja import NinjaAPI
ownerapi = NinjaAPI()
@ownerapi.post("/login", response={200: LoginSchema, 401: dict})
async def login(request, login_data: LogininSchema):
    is_valid, message, user_id = await verify_user_credentials(login_data.email, login_data.password)
    
    if is_valid:
        token = generate_token(user_id)  # Generate the token here
        return create_login_response(login_data, is_valid, message, token)
    else:
        return create_login_response(login_data, is_valid, message)


@ownerapi.post("/changePassword", response={200: ChangePasswordOutput, 400: dict, 401: dict})
def change_password(request, change_data: ChangePasswordInput):
    result = perform_change_password(change_data)
    response = generate_change_password_response(result)
    
    if not result["result"]:
        return JsonResponse(response, status=401)  
        
    return JsonResponse(response)
