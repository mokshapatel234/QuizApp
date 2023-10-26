import re
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
from asgiref.sync import sync_to_async
dotenv.load_dotenv()
import os
from django import setup
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quizapp.settings")  

setup()
from businessowner.models import Results, StudentAnswers, StudentMarks, BusinessOwners, Students, CompetitiveExams, AcademicExams, CompetitiveQuestions, AcademicQuestions, Options, WebsocketRooms

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
        try:
            await websocket.accept()  
            # self.active_connections.append(websocket)
        except Exception as e:
            print(e)

    async def disconnect(self, websocket: WebSocket, room_id):
        self.room_clients[room_id].remove(websocket)
        print(f"Client #{id(websocket)} left the chat")

    async def save_active_room(self, websocket: WebSocket, room_id):
        self.room_clients[room_id] = [websocket]
        print(self.room_clients)
    
    async def update_active_room(self, websocket: WebSocket, room_id):
        self.room_clients[room_id].append(websocket)
        print(self.room_clients)

    async def remove_active_room(self, websocket: WebSocket, room_id):
        self.room_clients[room_id].pop(websocket)
        print(self.room_clients)

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def send_personal_message(self, message: str, receiver_id: int, user_info, room_id):
        for connection in self.room_clients[room_id]:
            if id(connection) == receiver_id:
                image_url = user_info.profile_image.url if user_info.profile_image else None
                combined_message = f"{message} Image URL: {image_url}"
                await connection.send_text(combined_message)

    # async def join_room(self, websocket: WebSocket, room_id: str):
    #     self.room_clients[room_id] = self.active_connections
    #     print(self.room_clients)

    # async def leave_room(self, room_id: str):
    #     del self.room_clients[room_id]

    async def broadcast_to_room(self, room_id: str, message: str):
        for websocket in self.room_clients[room_id]:
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
    student_answer = StudentAnswers(
        academic_question=academic_question,
        competitive_question=competitive_question,
        selected_answer=selected_answer,
        student=student_instance,
        competitive_exam=competitive_exam,
        academic_exam=academic_exam,
    )
    student_answer.save()


# @sync_to_async
# def save_student_mark(student_instance, competitive_exam, academic_exam, academic_question, competitive_question, selected_answer):
#     try:
#         acadeemic_negative_marks = float(academic_exam.negative_marks) if student_instance.standard_id else None
#         competitive_negative_marks = float(competitive_exam.negative_marks) if student_instance.batch_id else None
#         student_mark = StudentMarks.objects.get(Students=student_instance, competitive=competitive_exam, academic=academic_exam)
#         if academic_question:
#             if academic_question.answer == selected_answer:
#                 student_mark.marks += academic_question.marks
#             elif acadeemic_negative_marks and academic_question.answer != selected_answer:
#                 student_mark.marks -= acadeemic_negative_marks
#         student_mark.save()
#         if competitive_question:
#             if competitive_question.answer == selected_answer:
#                 student_mark.marks += competitive_question.marks
#             elif competitive_negative_marks and competitive_question.answer != selected_answer:
#                 student_mark.marks -= competitive_negative_marks
#         student_mark.save()
#     except StudentMarks.DoesNotExist:
#         student_mark = StudentMarks.objects.create(
#             Students=student_instance,
#             competitive=competitive_exam,
#             academic=academic_exam,
#         )
#         if academic_question:
#             if academic_question.answer == selected_answer:
#                 student_mark.marks += academic_question.marks
#             elif acadeemic_negative_marks and academic_question.answer != selected_answer:
#                 student_mark.marks -= acadeemic_negative_marks
#         if competitive_question:
#             if competitive_question.answer == selected_answer:
#                 student_mark.marks += competitive_question.marks
#             elif competitive_negative_marks and competitive_question.answer != selected_answer:
#                 student_mark.marks -= competitive_negative_marks
#         student_mark.save()
#         return student_mark.marks


@sync_to_async
def save_student_result(academic_exam, competitive_exam, student, score, result):
    result_instance = Results(
        competitive_exam=competitive_exam,
        academic_exam=academic_exam ,
        student=student,
        score=score,
        result=result
    )
    result_instance.save()


@sync_to_async
def get_competitive_room(room_id):
    try:
        existing_room = WebsocketRooms.objects.get(room_id=room_id)
        if existing_room.competitive_exam:
            id = existing_room.competitive_exam.id
        return id
    except Exception as e:
        print(e)

@sync_to_async
def get_academic_room(room_id):
    try:
        existing_room = WebsocketRooms.objects.get(room_id=room_id)
        if existing_room.academic_exam:
            id = existing_room.academic_exam.id
        return id
    except Exception as e:
        print(e)

@sync_to_async
def get_existing_room(exam_id, business_type):
    try:
        if business_type == "competitive":
            existing_room = WebsocketRooms.objects.get(competitive_exam_id=exam_id)
        if business_type == "academic":
            existing_room = WebsocketRooms.objects.get(academic_exam_id=exam_id)
        return existing_room
    except WebsocketRooms.DoesNotExist:
        return None

@sync_to_async
def update_room(existing_room, new_room_id):
    try:
        existing_room.room_id = new_room_id
        existing_room.save()
        return existing_room
    except Exception as e:
        print(f"Error updating room: {e}")
        return None


@sync_to_async
def save_room(room_id, competitive_exam, academic_exam):
    try:
        room_save = WebsocketRooms(
            room_id = room_id,
            competitive_exam = competitive_exam,
            academic_exam = academic_exam
        )
        room_save.save()
    except Exception as e:
        print(e)
  

@sync_to_async
def get_selected_institute(id):
    try:
        return AcademicExams.objects.get(id=id)
    except:
        return CompetitiveExams.objects.get(id=id)


# @sync_to_async
# def student_verify(exam_id, institute):
#     try:
#         if institute.id == exam_id:
#             return True
#         return False
#     except Exception as e:
#         print()
        



@sync_to_async
def get_results(exam_id):
    try:
        results = Results.objects.filter(Q(competitive_exam=exam_id) | Q(academic_exam=exam_id))
        return list(results)
    except Results.DoesNotExist:
        return None
 

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
        question_ids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', query_string, re.IGNORECASE)
        if question_ids:
            unique_question_ids = list(set(question_ids))
            return unique_question_ids
        else:
            return None
    except Exception as e:
        return None


async def fetch_questions_from_database(room_id, business_type):
    questions_list = []
    
    if business_type == 'competitive':
        existing_id = await get_competitive_room(room_id)
        exam = await get_competitive_exam(existing_id)
        question_ids = get_question_set(exam)
        print(question_ids)

        for index, question_id in enumerate(question_ids):
            question = await get_competitive_question(question_id)
            options = await get_options(question.options_id)
            if question:
                question_data = {
                    "question": question.question,
                    "options": options,
                    "marks": question.marks,
                    "time_duration": question.time_duration*60,
                    "total_questions": exam.total_questions,
                    "question_index": index + 1 

                }
                questions_list.append(question_data)

    elif business_type == 'academic':
        existing_id = await get_academic_room(room_id)
        exam = await get_academic_exam(existing_id)
        question_ids = get_question_set(exam)
        print(question_ids)
        for index, question_id in enumerate(question_ids):
            question = await get_academic_question(question_id)
            options = await get_options(question.options_id)
            if question:
                question_data = {
                    "question": question.question,
                    "options": options,
                    "marks": question.marks,
                    "time_duration": question.time_duration*60,
                    "total_questions": exam.total_questions,
                    "question_index": index + 1 

                }
                questions_list.append(question_data)

    return questions_list

async def process_selected_answer(room_id, user_info, selected_answer, current_question_id, student_id):
    exam = None
    question = None
    student_instance = None
    student_score = 0

    if user_info.batch_id:
        existing_id = await get_competitive_room(room_id)
        exam = await get_competitive_exam(existing_id)
    elif user_info.standard_id:
        existing_id = await get_academic_room(room_id)
        exam = await get_academic_exam(existing_id)
    question_ids = get_question_set(exam)
    print(question_ids)
    if 0 <= current_question_id < len(question_ids):
        if user_info.batch_id:
            question = await get_competitive_question(question_ids[current_question_id])
        elif user_info.standard_id:
            question = await get_academic_question(question_ids[current_question_id])
            
    negative_marks = float(exam.negative_marks)
    if question:
        if question.answer == selected_answer:
            student_score += question.marks
        elif negative_marks and question.answer != selected_answer:
            student_score -= negative_marks

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


async def save_results(room_id, student_id, score, user_info):
    try:
        if user_info.batch_id:
            existing_id = await get_competitive_room(room_id)
            competitive_exam = await get_competitive_exam(existing_id)
            academic_exam = None
            if score >= competitive_exam.passing_marks:
                result = "pass"
            else:
                result = "fail"
        elif user_info.standard_id:
            existing_id = await get_academic_room(room_id)
            academic_exam = await get_academic_exam(existing_id)
            competitive_exam = None
            if score >= academic_exam.passing_marks:
                result = "pass"
            else:
                result = "fail"
        else:
            return

        student_instance = await get_student(student_id)
        if (competitive_exam or academic_exam) and student_instance:
            await save_student_result(academic_exam, competitive_exam, student_instance, score, result)
        
    except Exception as e:
        print(f"Error saving results: {e}")
   

async def get_exam_results(exam_id):
    try:
        results = await get_results(exam_id)         
        results_data = []
        for result in results:
            student = await get_student(result.student_id)
            print(student)
            if student:
                result_data = {
                    "rank": None,
                    "first_name": student.first_name if student.first_name else "N/A",
                    "last_name": student.last_name if student.last_name else "N/A",
                    "score": result.score,
                    "result": result.result,
                    "profile_image": student.profile_image.url if student.profile_image else None
                }
                results_data.append(result_data)
        sorted_results_data = sorted(results_data, key=lambda x: x['score'], reverse=True)
        for i, result in enumerate(sorted_results_data, start=1):
            result['rank'] = i
        return sorted_results_data
    except Exception as e:
        print(f"Error fetching results: {e}")
        return None


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
    global owner_id,business_owner_id

    user_info = await get_current_user(token, user_type)
    if not user_info:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    
    
    if isinstance(user_info, BusinessOwners):
        owner_id = id(websocket)
        business_owner_id = user_info.id
        await manager.connect(websocket)
        
    if room_id:
        if room_id in active_room and active_room[room_id] == owner_id:
            if isinstance(user_info, Students):
                if user_info.selected_institute_id==business_owner_id:
                    await manager.connect(websocket)
                    try:
                # await manager.join_room(websocket, room_id)
                            await manager.update_active_room(websocket, room_id)
                            await websocket.send_text(f"You are now connected to room {room_id}.")
                    except Exception as e:
                        print("this is error")
            
                    student_id = user_info.id
                    message = f"Student {user_info.first_name} {user_info.last_name} entered the room."
                    await manager.send_personal_message(message, owner_id, user_info, room_id)
        else:
            await websocket.close(code=1008, reason="Invalid Room ID")
            return
    else:
        room_id = generate_unique_room_id()
        await manager.save_active_room(websocket, room_id)
        existing_record = await get_existing_room(exam_id, user_info.business_type)
        if existing_record:
            await update_room(existing_record, room_id)
        else:
            if user_info.business_type == "competitive":
                competitive_exam = await get_competitive_exam(exam_id)
                academic_exam = None
            elif user_info.business_type == "academic":
                academic_exam = await get_academic_exam(exam_id)
                competitive_exam = None
            await save_room(room_id, competitive_exam, academic_exam)

        active_room[room_id] = owner_id
        # await manager.join_room(websocket, room_id)
        await websocket.send_text(f"Room ID: {room_id}")
        await websocket.send_text("You are now connected to the room.")

    student_score = 0
    try:
        while True:
            message = await websocket.receive_text()

            if message.startswith("start"):
                question_id = int(message.split(" ")[1])
                questions = await fetch_questions_from_database(room_id, user_info.business_type)
                if 0 <= question_id < len(questions):
                    question_data = questions[question_id]
                    await manager.broadcast_to_room(room_id, question_data)
                else:
                    await manager.broadcast_to_room(room_id, "Invalid question ID")


            elif message.startswith("next"):
                question_id += 1
                questions = await fetch_questions_from_database(room_id, user_info.business_type)
                if 0 <= question_id < len(questions):
                    question_data = questions[question_id]
                    await manager.broadcast_to_room(room_id, question_data)
                else:
                    await manager.broadcast_to_room(room_id, "No more questions.")
            
            elif message.startswith("selected_answer"):
                try:
                    parts = message.split(" ")
                    if len(parts) >= 3:
                        selected_answer = parts[1]
                        current_question_id = int(parts[2])

                        student_score += await process_selected_answer(room_id, user_info, selected_answer, current_question_id, student_id)
                        print(student_score, "SCORE")
                except Exception as e:
                    print(f"Error processing selected answer: {e}")
                   
            elif message == "finish":
                await save_results(room_id, student_id, student_score, user_info)
                break

            elif message.startswith("get_result"):
                if user_info.business_type == "competitive":
                    exam = await get_competitive_exam(exam_id)
                elif user_info.business_type == 'academic':
                    exam = await get_academic_exam(exam_id)
                exam_data = {
                    "title": exam.exam_title,
                    "passing_marks": exam.passing_marks,
                    "total_marks": exam.total_marks,
                    "time_duration": exam.time_duration,
                    "total_questions": exam.total_questions
                }
                exam_results = await get_exam_results(exam_id)
                if exam_results:
                    result_data = {
                        "exam_data": exam_data,
                        "exam_results": exam_results
                    }
                    await manager.broadcast_to_room(room_id, result_data)
                else:
                    await manager.broadcast_to_room(room_id, "Failed to fetch exam results.")
                # await manager.remove_active_room(websocket, room_id)


    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)


if __name__ == '__main__':
    uvicorn.run("websocket:app", host="0.0.0.0", port=7000, log_level="info", reload=True)
