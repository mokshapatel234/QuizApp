from pydantic import BaseModel
from typing import List
from fastapi import (
    FastAPI, WebSocketDisconnect,
    Request, Response
)
from starlette.websockets import WebSocket, WebSocketState
from rest_framework.authentication import BaseAuthentication
import jwt
from .main import database
from rest_framework import exceptions   
from businessowner.models import BusinessOwners
from fastapi import HTTPException

class Singleton:
    _instances = {}

    @classmethod
    def get_instance(cls, args, *kwargs):
        """ Static access method. """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)

        return cls._instances[cls]

    @classmethod
    def initialize(cls, args, *kwargs):
        """ Static access method. """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)


class ConnectionManager(Singleton):
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client #{id(websocket)} left the chat")

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def broadcast_message(self, message: str):
        for connection in self.active_connections:
            if connection.application_state == WebSocketState.CONNECTED:
                await connection.send_text(message)


def get_connection_manager():
    return ConnectionManager.get_instance()

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
            owner = database["businessowners"].find_one({"id": payload['user_id']})
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed('Error fetching business owner from the database')

        if not owner:
            raise exceptions.AuthenticationFailed('Business owner not found.')

        request.user = BusinessOwners(
            id=owner.get('id'),
        )

        return (request.user, jwt_token)
    
def verify_token(jwt_token):
    
    try:
        payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        print(e)
        raise HTTPException(status_code=400, detail="Authorization Token is invalid")

    jwt_auth = JWTAuthentication()
    request = None  # You need to define the 'request' object
    user, jwt_token = jwt_auth.authenticate(request)
    
    if not user:
        raise HTTPException(status_code=400, detail="Authorization Token is invalid")

    return user