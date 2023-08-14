from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import *
import jwt
from rest_framework import permissions
from functools import wraps
from django.http import JsonResponse

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.headers.get('Authorization', None)
        
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, 'secret', algorithm='HS256')
            except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
                print(e)
                raise exceptions.AuthenticationFailed('Token is invalid')
        else:
            raise exceptions.AuthenticationFailed('Token is required')
        
    

        try:
            request.user = BusinessOwners.objects.get(id=payload['user_id'])
        except BusinessOwners.DoesNotExist:
            raise exceptions.AuthenticationFailed('Business owner not found.')

        return (request.user, jwt_token)

def verify_token(controller):
    """
   Decorator that verifies the correctness of the returning token.

        If the token is correct, user is fetched and set as
        the requested user. Otherwise, it raises an authorization error.
    """

    @wraps(controller)
    def wrapper(request,*args, **kwargs):
        jwt_token = request.headers.get("Authorization", None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
            except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
                print(e)
                return JsonResponse({"result":False,'error':"Authorization Token is invalid"},status=400)
        else:
            return JsonResponse({"result":False,"error": "Authorization Token is required"},status=400)

       
        jwt_auth = JWTAuthentication()
        request.user, jwt_token = jwt_auth.authenticate(request)
        
        if not request.user:
            return None, {"result":False,"message": "Authorization Token is invalid"}
        return controller(request,*args,**kwargs)

    return wrapper
