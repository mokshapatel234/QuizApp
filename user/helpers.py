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
        
        # Filter results by month if query.month is available
        if query.month:
            results = [result for result in results if result.created_at.month == current_month]

        total_exams = len(results)
        passed_result = [result for result in results if result.result == "pass"]
        passed_exams = len(passed_result)
        failed_result = [result for result in results if result.result == "fail"]
        failed_exams = len(failed_result)
        
        print(total_exams, passed_exams, failed_exams)
    
        profile_data = Profile(
            id=str(student.id),
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            contact_no=student.contact_no,
            profile_image=student.profile_image.url if student.profile_image else None,
            selected_language=student.selected_language,
            total_exams=total_exams if total_exams else None,  # Added this line
            passed_exams=passed_exams if passed_exams else None,  # Added this line
            failed_exams=failed_exams if failed_exams else None 
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
                        try:
                            image_data = base64.b64decode(value)
                            timestamp = int(time.time())
                            unique_filename = f"profile_image_{timestamp}.png"
                            student.profile_image.save(unique_filename, ContentFile(image_data))
                        except Exception as e:
                            print(e)
        
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
            "message": str(e)
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

        if latest_terms is not None:
            data = {
                "terms_and_condition": latest_terms.terms_and_condition,
                "privacy_policy": latest_terms.privacy_policy,
            }

            response_data = {
                "result": True,
                "data": data,
                "message": "Data retrieved successfully"
            }
            return response_data
        else:
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
            print(exams)
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
                    result = Results.objects.get(competitive_exam=exam,student=user)
    
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
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
    

def get_exam_detail(user, exam_id):
    try:
        business_owner = BusinessOwners.objects.get(id=user.selected_institute.id)
        if business_owner.business_type == "competitive":
            exam = CompetitiveExams.objects.get(id=exam_id)
                
            try:
                result = Results.objects.get(competitive_exam=exam, student=user)
            except Results.DoesNotExist:
                result = None

            exam_data_list = []
            for exam_data in exam.exam_data.all():
                subject_name = exam_data.subject.subject_name
                subject_id = exam_data.subject.id
            
                chapters = []
                for chapter_id in exam_data.chapter.split(","):
                    chapter_id = chapter_id.strip()  

                    if chapter_id:  
                        try:
                            chapter = CompetitiveChapters.objects.get(id=chapter_id)
                            chapters.append(chapter.chapter_name)
                        except CompetitiveChapters.DoesNotExist:
                            pass  
                
                exam_data_list.append({"subject_id": subject_id, "subject": subject_name, "chapters": chapters})

            exam_detail = {
                "id": str(exam.id),
                "exam_title": exam.exam_title,
                "batch": str(exam.batch.id),
                "batch_name": exam.batch.batch_name,
                "total_marks": exam.total_marks,
                "passing_marks": exam.passing_marks,
                "start_date": exam.start_date,
                "exam_datas": exam_data_list,
                "mark": result.score if result else None
            }
            response = {
                "result": True,
                "data": exam_detail,
                "message": "Exam detail retrieved successfully."
            }
            return response

        elif business_owner.business_type == "academic":
            exam = AcademicExams.objects.get(id=exam_id)
            try:
                result = Results.objects.get(academic_exam=exam, student=user)
            except Results.DoesNotExist:
                result = None

            exam_data_list = []
            for exam_data in exam.exam_data.all():
                subject_name = exam_data.subject.subject_name
                subject_id = exam_data.subject.id
                chapters = []
                for chapter_id in exam_data.chapter.split(","):
                    chapter_id = chapter_id.strip()  

                    if chapter_id:  
                        try:
                            chapter = AcademicChapters.objects.get(id=chapter_id)
                            chapters.append(chapter.chapter_name)
                        except AcademicChapters.DoesNotExist:
                            pass
                
                exam_data_list.append({"subject_id": subject_id, "subject": subject_name, "chapters": chapters})

            exam_detail = {
                "id": str(exam.id),
                "exam_title": exam.exam_title,
                "total_question": exam.total_questions,
                "time_duration": exam.time_duration,
                "negative_marks": exam.negative_marks,
                "total_marks": exam.total_marks,
                "passing_marks": exam.passing_marks,
                "start_date": exam.start_date,
                "exam_data": exam_data_list,
                "mark": result.score if result else None
            }
            response = {
                "result": True,
                "data": exam_detail,
                "message": "Exam detail retrieved successfully."
            }
            return response

    except Exception as e:
        response = {
            "result": False,
            "message": str(e)
        }
        return response

    


def get_exam_detail_question(user, exam_id, subject_id):
    try:
        if not subject_id:
            return {"result": False, "message": "Subject ID not provided"}
        business_owner = BusinessOwners.objects.get(id=user.selected_institute.id)

        if business_owner.business_type == "competitive":
            try:
                exam = CompetitiveExams.objects.get(id=exam_id)
                questions = exam.question_set.filter(competitve_chapter__subject_name=subject_id)
                easy_questions = []
                medium_questions = []
                hard_questions = []

                for question in questions:
                    subject_name = str(question.competitve_chapter.subject_name)  # Convert to string
                    question_data = {
                        "question_text": question.question,
                        "question_image": question.competitive_question_image.url if question.competitive_question_image else None,
                        "subject_name": subject_name,
                        "right_answer": question.answer,
                        "options": {
                            "option1": question.options.option1,
                            "option2": question.options.option2,
                            "option3": question.options.option3,
                            "option4": question.options.option4,
                        }
                    }

                    if question.question_category == "easy":
                        easy_questions.append(question_data)
                    elif question.question_category == "medium":
                        medium_questions.append(question_data)
                    elif question.question_category == "hard":
                        hard_questions.append(question_data)

                    selected_answer = StudentAnswers.objects.filter(competitive_question=question, student=user).values_list('selected_answer', flat=True).first()
                    question_data["selected_answer"] = selected_answer if selected_answer else None
            except CompetitiveExams.DoesNotExist:
                return {"result": False, "message": "Competitive Exam not found"}

        elif business_owner.business_type == "academic":
            try:
                exam = AcademicExams.objects.get(id=exam_id)
                questions = exam.question_set.filter(academic_chapter__subject_name=subject_id)
                easy_questions = []
                medium_questions = []
                hard_questions = []

                for question in questions:
                    subject_name = str(question.academic_chapter.subject_name)  # Convert to string
                    question_data = {
                        "question_text": question.question,
                        "question_image": question.academic_question_image.url if question.academic_question_image else None,
                        "subject_name": subject_name,
                        "right_answer": question.answer,
                        "options": {
                            "option1": question.options.option1,
                            "option2": question.options.option2,
                            "option3": question.options.option3,
                            "option4": question.options.option4,
                        }
                    }

                    if question.question_category == "easy":
                        easy_questions.append(question_data)
                    elif question.question_category == "medium":
                        medium_questions.append(question_data)
                    elif question.question_category == "hard":
                        hard_questions.append(question_data)

                    selected_answer = StudentAnswers.objects.filter(academic_question=question, student=user).values_list('selected_answer', flat=True).first()
                    question_data["selected_answer"] = selected_answer if selected_answer else None

            except AcademicExams.DoesNotExist:
                return {"result": False, "message": "Academic Exam not found"}

        exam_detail = {
            "easy_questions": easy_questions,
            "medium_questions": medium_questions,
            "hard_questions": hard_questions
        }

        return {"result": True, "data": exam_detail, "message": "Exam detail retrieved successfully."}

    except Exception as e:
        return {"result": False, "message": str(e)}


def get_subject_list(user):
    try:
        business_owner = BusinessOwners.objects.get(id=user.selected_institute.id)
        if business_owner.business_type == "competitive":
            comp_subjects = CompetitiveSubjects.objects.filter(business_owner=business_owner)
            comp_subject_list = [
                {
                    "id": str(subject.id),
                    "subject_name": subject.subject_name,
                }
                for subject in comp_subjects
            ]
            return {
                "result": True,
                "data": comp_subject_list,
                "message": "Competitive subjects retrieved successfully."
            }
        elif business_owner.business_type == "academic":
            academic_subjects = AcademicSubjects.objects.filter(standard__medium_name__board_name__business_owner=business_owner)
            user_standard = user.standard
            print(user_standard)
            academic_subjects = academic_subjects.filter(standard=user_standard)
            academic_subject_list = [
                {
                    "id": str(subject.id),
                    "subject_name": subject.subject_name,
                }
                for subject in academic_subjects
            ]
            return {
                "result": True,
                "data": academic_subject_list,
                "message": "Competitive subjects retrieved successfully."
            }
        else:
            response_data = {
                "result": False,
                "message": "Invalid business type"
            }
            return JsonResponse(response_data, status=400)

    except BusinessOwners.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Business owner not found"
        }
        return JsonResponse(response_data, status=400)

    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong"
        }
        return JsonResponse(response_data, status=400)