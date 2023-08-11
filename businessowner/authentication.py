from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import *
import jwt
from rest_framework import permissions

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
