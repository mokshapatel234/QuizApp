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
                "type":business_owner.business_type  
            })

        response_data = {
            "result": True,
            "data": {
                "Institutes": business_owners,
            },
            "message": "Institute list retrieved succesfully",
        }
        return JsonResponse(response_data)
    
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found",
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=400)
    

def select_class(user, data):
    try:
        selected_class = BusinessOwners.objects.get(id = data.id)
        student = Students.objects.get(id = user.id)
        student.selected_institute = selected_class
        student.save()
        response_data = {
            "result": True,
            "data": {
                "id": str(selected_class.id),
                "name": selected_class.business_name,
                "type": selected_class.business_type
            },
            "message": "Institute selected successfully"
        }
        return response_data
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found",
        }
        return JsonResponse(response_data, status=400)
    except BusinessOwners.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Institute not found",   
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=400)
    

#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------USER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def get_profile(user):
    try:
        student = Students.objects.get(id=user.id)

        # Get the current month
        # current_month = datetime.now().strftime('%B')

        # List of months with the current month first
        months = [
            # current_month,
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        # Create a Profile instance
        profile_data = Profile(
            id=str(student.id),
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            contact_no=student.contact_no,
            profile_image=student.profile_image.url if student.profile_image else None,
            months=months
        )

        response_data = {
            "result": True,
            "data": profile_data.dict(),
            "message": "Profile retrieved successfully"
        }
        return response_data
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e),
        }
        return JsonResponse(response_data, status=400)
    

def update_profile(user, data):
    try: 
        student = Students.objects.get(id=user.id)
        
        if student:
            update_data = {field: value for field, value in data.dict().items() if value is not None}
            if update_data:
                image_path = update_data.get('profile_image')
                for field, value in update_data.items():
                    
                    if field == "email":
                        existing_email = Students.objects.filter(business_owner=student.business_owner, email=data.email).first()

                        if existing_email:
                            response_data = {
                                "result": False,
                                "message": "A student with this email already exists for this institute."
                            }
                            return JsonResponse(response_data, status=400)
                        else:
                            student.email = value
                    else:
                        setattr(student, field, value)
                if image_path:
                    with open(image_path, 'rb') as image_file:
                        binary_data = image_file.read()
                        image_base64 = base64.b64encode(binary_data).decode('utf-8')
                    image_name = os.path.basename(image_path)
                    student.profile_image.save(image_name, ContentFile(base64.b64decode(image_base64)))
                    
                student.save()

                # Get the current month
                # current_month = datetime.now().strftime('%B')

                # List of months with the current month first
                months = [
                    # current_month,
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ]

                response_data ={
                    "result":True,
                    "data":{
                        "id": str(student.id),
                        "first_name": student.first_name,
                        "last_name": student.last_name,
                        "email": student.email,
                        "contact_no": student.contact_no,
                        "profile_image": student.profile_image.url if student.profile_image else None,
                        "months": months  # List of months with the current month first
                    },
                    "message": "Profile updated successfully"
                }
                return response_data  # Return response here
            return None  # Return None if update_data is empty

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e),
        }
        return JsonResponse(response_data, status=400)

    


def get_news(user):
    try:
        # Determine the user's role (standard or batch)
        is_standard_user = hasattr(user, 'standard')
        is_batch_user = hasattr(user, 'batch')
        print(is_standard_user)
        print(is_batch_user)
        if is_standard_user:
            # Filter news for standard user
            newses = BusinessNewses.objects.filter(business_owner=user.business_owner, status="active", standard=user.standard)
            
        elif is_batch_user:
            # Filter news for batch user
            newses = BusinessNewses.objects.filter(business_owner=user.business_owner, status="active", batch=user.batch)
        else:
            # Handle cases where the user doesn't have a specific role
            return JsonResponse({"result": False, "message": "User has no specific standard or batch."}, status=400)

        newses_list = [
            {
                "id": str(news.id),
                "image": news.image.url if news.image else None,
                "text": news.news if news.news else None,
                "status": news.status,
                "standard": str(news.standard.id) if news.standard else None,
                "batch": str(news.batch.id) if news.batch else None,
            }
            for news in newses
        ]
        return newses_list

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=500)
    


def get_termsandcondtion(user):
    try:
        # Fetch the latest terms and conditions from the database
        latest_terms = TermsandPolicy.objects.first()

        # Create a dictionary with the terms and conditions data
        data = {
            "terms_and_condition": latest_terms.terms_and_condition,
            "privacy_policy": latest_terms.privacy_policy,
        }

        response_data = {
            "result": True,
            "data": data,
            "message": "data retrieved successfully"
        }
        return response_data

    except TermsandPolicy.DoesNotExist:
        return {"result": False, "message": "No terms and conditions found"}

    except Exception as e:
        return {"result": False, "message": str(e)}