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
import time
import base64
from django.core.files.base import ContentFile  # Import ContentFile



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
                    "selected_language": first_student.selected_language,
                    "token": token,   
                },
                "message": "Login successful",
            }
            return response_data
        else:
            response_data = {
                "result": False,
                "message": "No students found with the provided contact number",
            }
            return JsonResponse(response_data, status=404)
        
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found"
        }
        return JsonResponse(response_data, status=400)
        
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
    

def select_lan(user, data):
    try:

        student = Students.objects.get(id = user.id)
        student.selected_language = data.language
        student.save()
        response_data = {
            "result": True,
            "data": {
                "id": str(student.id),
                "selected_language": student.selected_language
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


def get_profile(user, query):
    try:
        student = Students.objects.get(id=user.id)
        if not query.month:
            current_month = datetime.now().month
            print(current_month)
        else:
            print(query.month)
            current_month = query.month
        results = Results.objects.filter(student=user.id)
        # results = results.filter(created_at__month=current_month)
        total_exams = results.count()
        passed_result = results.filter(result="pass")
        passed_exams = passed_result.count()
        failed_result = results.filter(result="fail")
        failed_exams = failed_result.count()
        
        print(total_exams, passed_exams, failed_exams)
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        profile_data = Profile(
            id=str(student.id),
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            contact_no=student.contact_no,
            profile_image=student.profile_image.url if student.profile_image else None,
            selected_language=student.selected_language,
            months=months
        )
        response_data = {
            "result": True,
            "data": profile_data.dict(),
            "message": "Profile retrieved successfully"
        }
        return response_data
    
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found"
        }
        return JsonResponse(response_data, status=400)
    
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
                    elif field == "profile_image":
                        # Handle the image data here
                        image_data = base64.b64decode(value)
                        timestamp = int(time.time())
                        unique_filename = f"profile_image_{timestamp}.png"
                        
                        student.profile_image.save(unique_filename, ContentFile(image_data))
        
                    else:
                        setattr(student, field, value)
                
                student.save()

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
                        "selected_language": student.selected_language ,
                        "months": months
                         
                    },
                    "message": "Profile updated successfully"
                }
                return response_data  
            return None  
        
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found"
        }
        return JsonResponse(response_data, status=400)

    except Exception as e:
        print(e)
        response_data = {
            "result": False,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=400)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------DASHBOARD--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def dashboard(user):
    try:
        student = Students.objects.get(id=user.id)
        response_data ={
                    "result":True,
                    "data":{
                        "id": str(student.id),
                        "selected_institute_id": str(student.selected_institute.id) if student.selected_institute else None,
                        "selected_institute_name": str(student.selected_institute.business_name) if student.selected_institute else None,
                        "selected_language": student.selected_language,
                        "logo": student.selected_institute.logo.url if student.selected_institute.logo else None,
                
                    },
                    "message": "Profile updated successfully"
                }
        return response_data  

    except Exception as e:
        print(e)
        response_data = {
            "result": False,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=400)



#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------------NEWS----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def get_news(user):
    try:
        newses = BusinessNewses.objects.filter(
            Q(standard=user.standard, batch=None) | Q(standard=None, batch=user.batch) | Q(standard=None, batch=None),
            business_owner=user.selected_institute,
            status="active",
        ).order_by('-created_at')[:5]

        news_list = []

        for news in newses:
            news_list.append({
                "id": str(news.id),
                "image": news.image.url if news.image else None,
                "text": news.news if news.news else None,
                "status": news.status,
                "standard": str(news.standard.id) if news.standard else None,
                "batch": str(news.batch.id) if news.batch else None,
                "is_image": True if news.image else False,
                "created_at": str(news.created_at),
                "updated_at": str(news.updated_at)
            })

        return news_list
    
    except BusinessNewses.DoesNotExist:
        response_data = {
            "result": False,
            "message": "News not found"
        }
        return JsonResponse(response_data, status=400)
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found"
        }
        return JsonResponse(response_data, status=400)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong"
        }
        return JsonResponse(response_data, status=500)
    

#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------TERMS & CONDITION-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
   

def get_termsandcondtion(user):
    try:
        latest_terms = TermsandPolicy.objects.first()
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
        return {"result": False, "message": "Terms and conditions not found"}

    except Exception as e:
        return {"result": False, "message": "Something went wrong"}
    

#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------EXAM-----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

def get_exam_history(user, query):
    try:
        business_owner = BusinessOwners.objects.get(id=user.selected_institute.id)
        if business_owner.business_type == "competitive":        
            exams = CompetitiveExams.objects.filter(business_owner=business_owner, start_date__isnull=False).order_by('-created_at')
            exam_list = []
            
            if query.subject_id:
                exams = exams.filter(exam_data__subject=query.subject_id)
            
            if query.search:
                search_terms = query.search.strip().split()
                search_query = Q()

                for term in search_terms:
                    search_query |= (
                        Q(exam_title__icontains=term)
                        | Q(status__icontains=term)
                    )
            for exam in exams:
                try:
                    result = Results.objects.get(competitive_exam=exam)
                except Results.DoesNotExist:
                    result = None

                # If query.month is not provided or not valid, add all exams to the list
                if not query.month or (query.month and exam.start_date.month == int(query.month)):
                    # Add filtering by year
                    if not query.year or (query.year and exam.start_date.year == int(query.year)):
                        exam_data_list = []
                        for exam_data in exam.exam_data.all():
                            subject_name = exam_data.subject.subject_name
                            subject_id = exam_data.subject.id
                            exam_data_list.append({"subject_id": str(subject_id), "subject": subject_name})

                        exam_detail = {
                            "id": str(exam.id),
                            "exam_title": exam.exam_title,
                            "total_marks": exam.total_marks,
                            "start_date": str(exam.start_date),
                            "exam_datas": exam_data_list,
                            "result": result.result if result else None
                        }
                        exam_list.append(exam_detail)

            return exam_list

        if business_owner.business_type == "academic":
            exams = AcademicExams.objects.filter(business_owner=business_owner, start_date__isnull=False).order_by('-created_at')

        if query.subject:
            exams = exams.filter(exam_data__subject=query.subject)

        if query.search:
            search_terms = query.search.strip().split()
            search_query = Q()

            for exam in exams:
                # If query.month is not provided or not valid, add all exams to the list
                if not query.month or (query.month and exam.start_date.month == int(query.month)):
                    # Add filtering by year
                    if not query.year or (query.year and exam.start_date.year == int(query.year)):
                        exam_data_list = []
                        for exam_data in exam.exam_data.all():
                            subject_name = exam_data.subject.subject_name
                            subject_id = exam_data.subject.id
                            exam_data_list.append({"subject_id": str(subject_id),"subject": subject_name,})

                        result = None  # Assuming result is not defined in academic exams

                        exam_detail = {
                            "id": str(exam.id),
                            "exam_title": exam.exam_title,
                            "negative_marks": exam.negative_marks,
                            "total_marks": exam.total_marks,
                            "start_date": exam.start_date,
                            "exam_datas": exam_data_list,
                            "result": result.result if result else None
                        }
                        exam_list.append(exam_detail)

            return exam_list
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)
    

def get_exam_detail(user, exam_id):
    business_owner = BusinessOwners.objects.get(id=user.selected_institute.id)
    if business_owner.business_type == "competitive":
        exam = CompetitiveExams.objects.get(id=exam_id)
  
        try:
            result = Results.objects.get(competitive_exam=exam)
        except Results.DoesNotExist:
            result = None

        exam_data_list = []
        for exam_data in exam.exam_data.all():
            subject_name = exam_data.subject.subject_name

        
            chapters = []
            for chapter_id in exam_data.chapter.split(","):
                chapter_id = chapter_id.strip()  

                if chapter_id:  
                    try:
                        chapter = CompetitiveChapters.objects.get(id=chapter_id)
                        chapters.append(chapter.chapter_name)
                    except CompetitiveChapters.DoesNotExist:
                        pass  
            
            exam_data_list.append({"subject": subject_name, "chapters": chapters})

        exam_detail = {
            "id": str(exam.id),
            "exam_title": exam.exam_title,
            "batch": str(exam.batch.id),
            "batch_name": exam.batch.batch_name,
            "total_marks": exam.total_marks,
            "start_date": exam.start_date,
            "exam_datas": exam_data_list,
            "mark": result.score if result else None
        }
        return exam_detail

    elif business_owner.business_type == "academic":
        exam = AcademicExams.objects.get(id=exam_id)
        try:
            result = Results.objects.get(academic_exam=exam)
        except Results.DoesNotExist:
            result = None

        exam_data_list = []
        for exam_data in exam.exam_data.all():
            subject_name = exam_data.subject.subject_name

            chapters = []
            for chapter_id in exam_data.chapter.split(","):
                chapter_id = chapter_id.strip()  

                if chapter_id:  
                    try:
                        chapter = AcademicChapters.objects.get(id=chapter_id)
                        chapters.append(chapter.chapter_name)
                    except AcademicChapters.DoesNotExist:
                        pass
            
            exam_data_list.append({"subject": subject_name, "chapters": chapters})

        exam_detail = {
            "id": str(exam.id),
            "exam_title": exam.exam_title,
            "total_question": exam.total_questions,
            "time_duration": exam.time_duration,
            "negative_marks": exam.negative_marks,
            "total_marks": exam.total_marks,
            "start_date": exam.start_date,
            "exam_data": exam_data_list,
            "mark": result.score if result else None
        }
        return exam_detail