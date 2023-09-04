import calendar
from businessowner.models import *
from .schemas import *
from django.http import JsonResponse
from ninja import File
from django.db.models import Q
from ninja.errors import HttpError
from .utils import generate_token
import pandas as pd
from datetime import timedelta, timezone
import random
import time
import jwt
import razorpay
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
import base64
from urllib.request import urlopen
from django.core.files.base import ContentFile  # Import ContentFile
import os



def perform_login(data):
    try:
        students = Students.objects.filter(contact_no=data.contact_no)
        print(students)
        if students:
            first_student = students.first()
            token = generate_token(str(first_student.id))  
            response_data = {
                "result": True,
                "data": {
                    "first_name": first_student.first_name,
                    "last_name": first_student.last_name,
                    "email": first_student.email,
                    "contact_no": first_student.contact_no,
                    "address": first_student.address if first_student.address else None,
                    "profile_image": first_student.profile_image.url if first_student.profile_image else None,
                    "status": first_student.status,
                    "token": token,   
                },
                "message": "Login successful for multiple students",
            }
            return response_data
        else:
            response_data = {
                "result": False,
                "message": "No students found with the provided contact number",
            }
            return JsonResponse(response_data, status=404)
        
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=400)



def get_class_list(user):
    try:
        student = Students.objects.get(id=user.id)
        students = Students.objects.filter(contact_no=student.contact_no)
        business_owners = []
        for student in students:
            business_owner = student.business_owner
            business_owners.append({
                "id": business_owner.id,
                "name": business_owner.business_name,  
            })

        response_data = {
            "result": True,
            "data": {
                "Institutes": business_owners,
            },
            "message": "Institute list retrieved succesfully",
        }
        return JsonResponse(response_data)
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=400)
    

def select_class(user):
    try:
        pass
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e),
        }
        return JsonResponse(response_data, status=400)