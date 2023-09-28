from fastapi import FastAPI, WebSocket, Query, Depends, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from pymongo import MongoClient
from typing import Optional
from fastapi import WebSocketDisconnect
import os
import dotenv
import jwt
import uuid
from rest_framework import exceptions
from fastapi import HTTPException
from starlette.websockets import WebSocketState
from django.db import transaction
from asgiref.sync import sync_to_async
dotenv.load_dotenv()
import os
from django import setup


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quizapp.settings")  

setup()
from businessowner.models import BusinessOwners, Students

app = FastAPI()

client = MongoClient(os.getenv('DATABASE'))
db = client["mindscapeqdb_staging"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()  
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client #{id(websocket)} left the chat")

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def send_personal_message(self, message: str, receiver: str):
        for connection in self.active_connections:
            websocket = connection
            if id(websocket) == receiver:
                await websocket.send_text(message)


    async def broadcast(self, message: str):
        for client_id, data in self.active_connections.items():
            websocket = data["websocket"]
            await websocket.send_text(message)

    async def join_room(self, websocket: WebSocket, room_id: str):
        self.active_connections.append((websocket, room_id))


    def get_connection_by_user_id(self, user_id: str) -> Optional[WebSocket]:
        for connection, uid in self.active_connections:
            if uid == user_id:
                return connection
        return None


manager = ConnectionManager() 

def generate_unique_room_id():
    return str(uuid.uuid4())


class JWTAuthentication:
    async def authenticate(self, request, token, user_type):
        if token:
            try:
                payload = jwt.decode(token, 'secret', algorithm='HS256')
            except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
                print(e)
                raise exceptions.AuthenticationFailed('Token is invalid')
        else:
            raise exceptions.AuthenticationFailed('Token is required')

        user = None

        try:
            user_id = payload.get('user_id')
            if user_type == 'business_owner':
                user = await self.get_business_owner(user_id)
            elif user_type == 'student':
                user = await self.get_student(user_id)
            else:
                raise exceptions.AuthenticationFailed('Invalid user_type in token.')

        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed('Error fetching user from the database')

        if not user:
            raise exceptions.AuthenticationFailed('User not found.')

        request.user = user

        return (request.user, token)

    @sync_to_async
    def get_business_owner(self, user_id):
        try:
            return BusinessOwners.objects.get(id=user_id)
        except BusinessOwners.DoesNotExist:
            return None

    @sync_to_async
    def get_student(self, user_id):
        try:
            return Students.objects.get(id=user_id)
        except Students.DoesNotExist:
            return None


async def verify_token(token: str, user_type: str, request: Request = Depends()):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        print(e)
        raise HTTPException(status_code=400, detail="Authorization Token is invalid")

    jwt_auth = JWTAuthentication()
    user, token = await jwt_auth.authenticate(request, token, user_type)

    if not user:
        raise HTTPException(status_code=400, detail="Authorization Token is invalid")

    return user


async def get_current_user(token: str, user_type: str):
    """Helper function for auth with Firebase."""
    if not token:
        return ""
    try:
        user_info = await verify_token(token, user_type)
        return user_info
    except HTTPException as e:
        raise e

owner_id = None

@app.websocket("/ws/room_connection")
async def room_connection(
    websocket: WebSocket,
    token: str = Query(None),
    room_id: str = Query(None),
    user_type: str = Query(None)
):
    global owner_id  

    user_info = await get_current_user(token, user_type)
    print(user_info)
    if not user_info:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    
    await manager.connect(websocket)
    if owner_id is None:
        owner_id = id(websocket)
        print(owner_id, "Student")
        
    if room_id:
        await manager.join_room(websocket, room_id)
        await websocket.send_text(f"You are now connected to room {room_id}.")
        if isinstance(user_info, Students):
                print("info", user_info)
                student_id = user_info.id
                message = f"Student {user_info.first_name} {user_info.last_name} entered the room."
                await manager.send_personal_message(message, owner_id)
    else:
        room_id = generate_unique_room_id()
        await manager.join_room(websocket, room_id)
        await websocket.send_text(f"Room ID: {room_id}")
        await websocket.send_text("You are now connected to the room.")

    try:
        while True:
            message = await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(websocket)


if __name__ == '__main__':

    uvicorn.run("websocket:app", host="0.0.0.0", port=5000, log_level="info", reload=True)



