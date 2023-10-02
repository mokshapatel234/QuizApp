from fastapi import FastAPI, WebSocket, Query, Depends, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from pymongo import MongoClient
from typing import Optional
from fastapi import WebSocketDisconnect
import os
import dotenv
import jwt
import random
import uuid
import json
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
from businessowner.models import BusinessOwners, Students, StudentAnswer, CompetitiveExams, AcademicExams, CompetitiveQuestions, AcademicQuestions, Options

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
        self.room_clients = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()  
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client #{id(websocket)} left the chat")

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def send_personal_message(self, message: str, receiver_id: int):
        for connection in self.active_connections:
            if id(connection) == receiver_id:
                await connection.send_text(message)

    async def join_room(self, websocket: WebSocket, room_id: str):
        self.room_clients[room_id] = websocket

    async def leave_room(self, room_id: str):
        del self.room_clients[room_id]

    async def broadcast_to_room(self, room_id: str, message: str):
        for websocket in self.active_connections:
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Failed to send message to client : {e}")

manager = ConnectionManager() 

def generate_unique_room_id():
    # return str(uuid.uuid4())
    return str(random.randint(1000000000, 9999999999))

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


@sync_to_async
def save_student_answer(academic_question, competitive_question, selected_answer, student_instance, competitive_exam, academic_exam):
    student_answer = StudentAnswer(
        academic_question=academic_question,
        competitive_question=competitive_question,
        selected_answer=selected_answer,
        student=student_instance,
        competitive_exam=competitive_exam,
        academic_exam=academic_exam,
    )
    student_answer.save()

@sync_to_async
def get_student(student_id):
    try:
        return Students.objects.get(id=student_id)
    except Students.DoesNotExist:
        return None


@sync_to_async
def get_academic_exam(exam_id):
    try:
        return AcademicExams.objects.get(id=exam_id)
    except AcademicExams.DoesNotExist:
        return None
    

@sync_to_async
def get_academic_question(question_id):
    try:
        return AcademicQuestions.objects.get(id=question_id)
    except AcademicQuestions.DoesNotExist:
        return None
    
    
@sync_to_async
def get_competitive_exam(exam_id):
    try:
        return CompetitiveExams.objects.get(id=exam_id)
    except CompetitiveExams.DoesNotExist:
        return None
    except Exception as e:
        print(e)
    

@sync_to_async
def get_competitive_question(question_id):
    try:
        return CompetitiveQuestions.objects.get(id=question_id)
    except CompetitiveQuestions.DoesNotExist:
        return None
    

@sync_to_async
def get_options(option_id):
    try:
        options_data = Options.objects.get(id=option_id)
        if options_data:
            options_dict = {
                "option1": options_data.option1,
                "option2": options_data.option2,
                "option3": options_data.option3,
                "option4": options_data.option4,
            }
            return options_dict
        else:
            return None
    except Options.DoesNotExist:
        return None


def get_question_set(exam):
    try:
        query_string = str(exam.question_set.all().query)
        import re
        question_ids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', query_string, re.IGNORECASE)
        if question_ids:
            unique_question_ids = list(set(question_ids))
            return unique_question_ids
        else:
            print("No question IDs found in the query string.")
            return None
    except Exception as e:
        print(e)
        return None


async def fetch_questions_from_database(exam_id, business_type):
    questions_list = []

    if business_type == 'competitive':
        exam = await get_competitive_exam(exam_id)
        question_ids = get_question_set(exam)

        for question_id in question_ids:
            question = await get_competitive_question(question_id)
            options = await get_options(question.options_id)
            if question:
                question_data = {
                    "question": question.question,
                    "options": options,
                    "answer": question.answer,
                    "marks": question.marks,
                    "time_duration": question.time_duration
                }
                questions_list.append(question_data)

    elif business_type == 'academic':
        exam = await get_academic_exam(exam_id)
        question_ids = get_question_set(exam)

        for question_id in question_ids:
            question = await get_academic_question(question_id)
            options = await get_options(question.options_id)
            if question:
                question_data = {
                    "question": question.question,
                    "options": options,
                    "answer": question.answer,
                    "marks": question.marks,
                    "time_duration": question.time_duration
                }
                questions_list.append(question_data)

    return questions_list

async def process_selected_answer(exam_id, user_info, selected_answer, current_question_id, student_id):
    exam = None
    question = None
    student_instance = None
    student_score = 0

    if user_info.batch_id:
        exam = await get_competitive_exam(exam_id)
    elif user_info.standard_id:
        exam = await get_academic_exam(exam_id)

    question_ids = get_question_set(exam)

    if 0 <= current_question_id < len(question_ids):
        if user_info.batch_id:
            question = await get_competitive_question(question_ids[current_question_id])
        elif user_info.standard_id:
            question = await get_academic_question(question_ids[current_question_id])

    if question and question.answer == selected_answer:
        student_score += question.marks

        student_instance = await get_student(student_id)

    await save_student_answer(
        question if user_info.standard_id else None,
        question if user_info.batch_id else None,
        selected_answer,
        student_instance,
        exam if user_info.batch_id else None,
        exam if user_info.standard_id else None
    )

    return student_score


owner_id = None

active_room = {}


@app.websocket("/ws/room_connection")
async def room_connection(
    websocket: WebSocket,
    token: str = Query(None),
    room_id: str = Query(None),
    user_type: str = Query(None),
    exam_id: str = Query(None)
):
    global owner_id

    user_info = await get_current_user(token, user_type)
    print(user_info)
    if not user_info:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    await manager.connect(websocket)
    if isinstance(user_info, BusinessOwners):
        print("info", user_info.business_type)
    if owner_id is None:
        owner_id = id(websocket)
        print(owner_id, "Student")

    if room_id:
        if room_id in active_room and active_room[room_id] == owner_id:
            await manager.join_room(websocket, room_id)
            await websocket.send_text(f"You are now connected to room {room_id}.")
            if isinstance(user_info, Students):
                print("info", user_info)
                student_id = user_info.id
                message = f"Student {user_info.first_name} {user_info.last_name} entered the room."
                await manager.send_personal_message(message, owner_id)
        else:
            await websocket.close(code=1008, reason="Invalid Room ID")
            return
    else:
        room_id = generate_unique_room_id()
        active_room[room_id] = owner_id
        await manager.join_room(websocket, room_id)
        await websocket.send_text(f"Room ID: {room_id}")
        await websocket.send_text("You are now connected to the room.")

    student_score = 0
    try:
        while True:
            message = await websocket.receive_text()

            if message.startswith("start"):
                question_id = int(message.split(" ")[1])
                questions = await fetch_questions_from_database(exam_id, user_info.business_type)
                if 0 <= question_id < len(questions):
                    question_json = json.dumps(questions[question_id])
                    await manager.broadcast_to_room(room_id, question_json)
                else:
                    await manager.broadcast_to_room(room_id, "Invalid question ID")

            

            elif message.startswith("next question"):
                question_id += 1
                questions = await fetch_questions_from_database(exam_id, user_info.business_type)
                if 0 <= question_id < len(questions):
                    question_json = json.dumps(questions[question_id])
                    await manager.broadcast_to_room(room_id, question_json)
                else:
                    await manager.broadcast_to_room(room_id, "No more questions.")
            
            elif message.startswith("selected_answer"):
                parts = message.split(" ")
                selected_answer = parts[1]
                current_question_id = int(parts[2])

                student_score += await process_selected_answer(exam_id, user_info, selected_answer, current_question_id, student_id)
                print(student_score, "SCORE")
                   
            elif message == "finish":
                
                pass
    except WebSocketDisconnect:
        await manager.disconnect(websocket)




if __name__ == '__main__':

    uvicorn.run("websocket:app", host="0.0.0.0", port=5000, log_level="info", reload=True)



