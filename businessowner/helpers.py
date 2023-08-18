from .models import *
from .schemas import *
from django.http import JsonResponse
from .authentication import JWTAuthentication 
from asgiref.sync import sync_to_async
from ninja import UploadedFile, File
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from ninja.errors import HttpError
from .utils import generate_token
import pandas as pd
from datetime import timedelta

def perform_login(data):
    try:
        user = BusinessOwners.objects.get(email=data.email)
        if user.password == data.password:
            token = generate_token(str(user.id))
       
            city = Cities.objects.get(id=user.city_id)
            state = States.objects.get(id=city.state_id)
            response_data = {
                "result": True,
                "data": {
                    "id": str(user.id),
                    "business_name": user.business_name,
                    "business_type": user.business_type,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "contact_no": user.contact_no,
                    "address": user.address,
                    "logo": user.logo.url if user.logo else None,
                    "tuition_tagline": user.tuition_tagline if user.tuition_tagline else None,
                    "status": user.status,
                    "is_reset":user.is_reset,
                    "city": {
                        "city_id": str(city.id),
                        "city_name": city.name,
                        "state_id": str(city.state_id),
                        "state_name": state.name,
                    },
                    "token": token
                    },
                "message": "Login successful",
        
            }
            return response_data
        else:
            response_data = {
            "result": False,
            "message": "Invalid Password"
        }
        
    
        return JsonResponse(response_data, status=401)
    except BusinessOwners.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Invalid Email"
        }
    
        return JsonResponse(response_data, status=401)



def perform_change_password(data, user):
    try:
        if data.old_password != user.password:
            response_data = {"result": False, "message": "Invalid old password"}
            return JsonResponse(response_data, status=400)
        
        if data.new_password == user.password:
            response_data = {"result": False, "message": "Please change password"}
            return JsonResponse(response_data, status=400)
        
        user.password = data.new_password
        user.is_reset = True
        user.save()

        response_data = {"result": True, "message": "Password changed successfully"}
        return JsonResponse(response_data, status=200)
    
    except BusinessOwners.DoesNotExist:
        response_data = {"result": False, "message": "Business owner not found"}
        return JsonResponse(response_data, status=400)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------PLAN PURCHASE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def get_plan_purchase_response():
    try:
        plans = Plans.objects.all()

        plan_schema_list = [
            {
            "plan_name":plan.plan_name,
            "description":plan.description,
            "price":plan.price,
            "validity":plan.validity,
            "image":plan.image.url if plan.image else None,
            "status":plan.status
        } for plan in plans]

        response_data = {
            "result": True,
            "data": plan_schema_list,
            "message": "Data found successfully"
        }

        return JsonResponse(response_data, status=200)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong"
        }
        return JsonResponse(response_data, status=400)


def get_purchase_history_response(user):
    try:
        purchase_history = PurchaseHistory.objects.filter(business_owner=user, status__in=[True])

        purchase_history_list = [
            {
                "plan_name": purchase.plan.plan_name,
                "order_id": purchase.order_id,
                "status": purchase.status,
         
            }
            for purchase in purchase_history
        ]

        response_data = {
            "result": True,
            "data": purchase_history_list,
            "message": "Purchase history retrieved successfully"
        }

        return JsonResponse(response_data, status=200)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=400)
    

#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------OWNER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def create_owner_response(user, is_valid, message):
    try:
        owner = BusinessOwners.objects.get(id=user.id)

        if owner:
            city = Cities.objects.get(id=owner.city_id)
            state = States.objects.get(id=city.state_id)
        
            owner_data = {
                    "id": str(owner.id),
                    "business_name": owner.business_name,
                    "business_type": owner.business_type,
                    "first_name": owner.first_name,
                    "last_name": owner.last_name,
                    "email": owner.email,
                    "contact_no": owner.contact_no,
                    "address": owner.address,
                    "logo": owner.logo.url if owner.logo else None,
                    "tuition_tagline": owner.tuition_tagline if owner.tuition_tagline else None,
                    "status": owner.status,
                    "created_at": owner.created_at,
                    "city": {
                        "city_id": str(city.id),
                        "city_name": city.name,
                        "state_id": str(city.state_id),
                        "state_name": state.name,
                    },
                }

            response_data = {
                "result": is_valid,
                "data": owner_data,
                "message": message
            }
        else:
            response_data = {
                "result": False,
                "message": message
            }
        
        return JsonResponse(response_data, status=200)
    

    except BusinessOwners.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Business owner does not exist"
        }
        return JsonResponse(response_data, status=400)


def update_owner_data(data, user):
    try:
        owner = BusinessOwners.objects.get(id=user.id)
        if owner:
            update_data = {field: value for field, value in data.dict().items() if value is not None}
            city_id = update_data.pop('city', None)
            if city_id:
                city = Cities.objects.get(id=city_id)
                owner.city = city
            
            # Handle the logo update
            logo = update_data.pop('logo', None)
            if logo:
                owner.logo = logo
            if update_data:
                for field, value in update_data.items():
                    setattr(owner, field, value)
                owner.save()
                updated_owner_data = create_owner_response(owner, True, message="Owner updated successfully")
                return updated_owner_data
            else:
                response_data = {
                        "result": False,
                        "message": "updation not apply"
                    }
                return JsonResponse(response_data, status=400)      
        else:
            response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
            return JsonResponse(response_data, status=400)
        

    except BusinessOwners.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Business owner not found"
        }
        return JsonResponse(response_data, status=400)
    except Cities.DoesNotExist:
        response_data = {
            "result": False,
            "message": "City not found"
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=500)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_batch(data, user):
    try:
        batch_name = data.batch_name

        batch = CompetitiveBatches(batch_name=batch_name, business_owner=user)
        print(batch,"dsadsa")
        batch.save()
       
        business_owner = BusinessOwners.objects.get(id=batch.business_owner_id)
        batch_data = {
            "id": str(batch.id),
            "batch_name": batch.batch_name,
            "business_owner_id": str(batch.business_owner_id),
            "business_owner_name": business_owner.business_name,
            "status": batch.status,
            "created_at": batch.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "updated_at": batch.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            
        }
        response_data = {
            "result": True,
            "data": batch_data,
            "message": "Batch created successfully",
        }
        return response_data
    except Exception as e:
        print(e,"dsda")
        response_data = {
                "result": False,
                "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def get_batchlist(user, query):
    try:

        batches = CompetitiveBatches.objects.filter(business_owner=user)
        if query.status:
            batches = batches.filter(status=query.status)
        business_owner = BusinessOwners.objects.get(id=user.id)
        batches_list = [
            {
                "id": str(batch.id),
                "batch_name": batch.batch_name,
                "business_owner_id": str(batch.business_owner_id),
                "business_owner_name": business_owner.business_name,
                "status": batch.status,
                "created_at": batch.created_at,
                "updated_at": batch.updated_at,
            }
            for batch in batches
        ]

        response_data = {
            "result": True,
            "data": batches_list,
            "message": "Competitive batches retrieved successfully"
        }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def get_batch(batch_id, user):
    try:
        batch = CompetitiveBatches.objects.get(id=batch_id)
        business_owner = BusinessOwners.objects.get(id=user.id)
        batch_data = {
                "id": str(batch.id),
                "batch_name": batch.batch_name,
                "business_owner_id": str(batch.business_owner_id),
                "business_owner_name": business_owner.business_name,
                "status": batch.status,
                "created_at": batch.created_at,
                "updated_at": batch.updated_at,
            }
        response_data = {
            "result": True,
            "data": batch_data,
            "message": "Competitive batch retrieved successfully"
        }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def update_batch(batch_id, data):
    try:
        batch = CompetitiveBatches.objects.get(id=batch_id)
        if batch:
            update_data = {field: value for field, value in data.dict().items() if value is not None}
            if update_data:
                for field, value in update_data.items():
                    setattr(batch, field, value)
                batch.save()
                business_owner = BusinessOwners.objects.get(id=batch.business_owner_id)
                response_data = {
                    "result": True,
                    "data": {
                        "id": str(batch.id),
                        "batch_name": batch.batch_name,
                        "business_owner_id": str(batch.business_owner_id),
                        "business_owner_name": business_owner.business_name,
                        "status": batch.status,
                        "created_at": batch.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "updated_at": batch.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    },
                    "message": "Competitive batch updated successfully",
                }
                return response_data
            else:
                response_data = {
                    "result": False,
                    "message": "No fields to update"
                }
                return JsonResponse(response_data, status=400)
                
        else:
            response_data = {
                    "result": False,
                    "message": "Batch not found"
                }
            return JsonResponse(response_data, status=400)
           
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def delete_batch(batch_id):
    try:
        batch = CompetitiveBatches.objects.get(id=batch_id)
        batch.delete()

        response_data = {
            "result":True,
            "message":"Data Deleted Successfully"}
        return response_data
    
    except CompetitiveBatches.DoesNotExist:
        response_data = {
                    "result": False,
                    "message": "Btach not found"
                }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)  

#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE SUBJECT----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_comp_subect(data, user):
    try:
        subject_name = data.subject_name
        
        subject = CompetitiveSubjects.objects.create(subject_name=subject_name, business_owner=user)
        business_owner = BusinessOwners.objects.get(id=subject.business_owner_id)
        subject_data = {
            "id": str(subject.id),
            "subject_name": subject.subject_name,
            "business_owner_id": str(subject.business_owner_id),
            "business_owner_name": business_owner.business_name,
            "status": subject.status,
            "created_at": subject.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "updated_at": subject.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        response_data = {
            "result": True,
            "data": subject_data,
            "message": "Subject created successfully",
        }
        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)
    

def get_comp_subjectlist(user, query):
    try:
        subjects = CompetitiveSubjects.objects.filter(business_owner=user)
        if query.status:
            subjects = subjects.filter(status=query.status)
        business_owner = BusinessOwners.objects.get(id=user.id)
        subject_list = [
            {
                "id": str(subject.id),
                "subject_name": subject.subject_name,
                "business_owner_id": str(subject.business_owner_id),
                "business_owner_name": business_owner.business_name,
                "status": subject.status,
                "created_at": subject.created_at,
                "updated_at": subject.updated_at,
            }
            for subject in subjects
        ]

        response_data = {
            "result": True,
            "data": subject_list,
            "message": "Competitive subjects retrieved successfully"
        }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def get_comp_subject(subject_id, user):
    try:
        subject = CompetitiveSubjects.objects.get(id=subject_id)
        business_owner = BusinessOwners.objects.get(id=user.id)
        subject_data = {
                "id": str(subject.id),
                "subject_name": subject.subject_name,
                "business_owner_id": str(subject.business_owner_id),
                "business_owner_name": business_owner.business_name,
                "status": subject.status,
                "created_at": subject.created_at,
                "updated_at": subject.updated_at,
            }
        response_data = {
            "result": True,
            "data": subject_data,
            "message": "Competitive subject retrieved successfully"
        }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def update_comp_subject(subject_id, data):
    try:
        subject = CompetitiveSubjects.objects.get(id=subject_id)
        if subject:
            update_data = {field: value for field, value in data.dict().items() if value is not None}
            if update_data:
                for field, value in update_data.items():
                    setattr(subject, field, value)
                subject.save()
                business_owner = BusinessOwners.objects.get(id=subject.business_owner_id)
                response_data = {
                    "result": True,
                    "data": {
                        "id": str(subject.id),
                        "subject_name": subject.subject_name,
                        "business_owner_id": str(subject.business_owner_id),
                        "business_owner_name": business_owner.business_name,
                        "status": subject.status,
                        "created_at": subject.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "updated_at": subject.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    },
                    "message": "Subject updated successfully",
                }
                return response_data
            else:
                response_data = {
                    "result": False,
                    "message": "No fields to update"
                }
                return JsonResponse(response_data, status=400)
        else:
            response_data = {
                    "result": False,
                    "message": "Subject not found"
                }
            return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def delete_comp_subject(subject_id):
    try:
        subject = CompetitiveSubjects.objects.get(id=subject_id)
        subject.delete()

        response_data = {
            "result":True,
             "message":"Data Deleted Successfully"}
        return response_data

    except CompetitiveSubjects.DoesNotExist:
        response_data = {
                    "result": False,
                    "message": "Subject not found"
                }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)
    

#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE CHAPTER----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_comp_chapter(data):
    try:
        subject_instance = CompetitiveSubjects.objects.get(id=data.subject_id)
        batches_instances = CompetitiveBatches.objects.filter(id__in=data.batches)
        batches = list(batches_instances)
        
        # Create a new chapter instance
        chapter = CompetitiveChapters(
            subject_name=subject_instance,
            chapter_name=data.chapter_name,
        )

        for batch in batches:
            chapter.batches.add(batch)
        # chapter_instance.batches = list(batches_instances)
        chapter.save()
        print(chapter)
        subject_id = CompetitiveSubjects.objects.get(id=chapter.subject_name_id)
        batch_info = [{"id": str(batch.id), "batch_name": batch.batch_name} for batch in chapter.batches.all()]
        chapter_data = {
            "id": str(chapter.id),
            "chapter_name": chapter.chapter_name,
            "subject_id": str(subject_id.id),
            "subject_name": subject_id.subject_name,
            "batches":batch_info,
            "status": chapter.status,
            "created_at": chapter.created_at,
            "updated_at": chapter.updated_at,
        }
        response_data = {
            "result": True,
            "data": chapter_data,
            "message": "Chapter created successfully",
        }
        return response_data
    
    except CompetitiveSubjects.DoesNotExist:
        response_data = {
            "result": True,
            "message": "Subject not exist",
        }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        response_data = {
            "result": True,
            "message": "Something went wrong",
        }
        return JsonResponse(response_data, status=200)


def get_comp_chapterlist(user, query):
    try:
        chapters = CompetitiveChapters.objects.filter(subject_name__business_owner=user)

        if query.status:
            chapters = chapters.filter(status=query.status)
        if query.subject:
            chapters = chapters.filter(subject_name=query.subject)
        if query.batch:
            batch_id = query.batch
            chapters = [chapter for chapter in chapters if str(batch_id) in [str(batch.id) for batch in chapter.batches.all()]]


        chapters_list = []
        for chapter in chapters:
            subject_id = CompetitiveSubjects.objects.get(id=chapter.subject_name_id)
            batch_info = [{"id": str(batch.id), "batch_name": batch.batch_name} for batch in chapter.batches.all()]
            chapter_data = {
                "id": str(chapter.id),
                "chapter_name": chapter.chapter_name,
                "subject_id": str(subject_id.id),
                "subject_name": subject_id.subject_name,
                "batches":batch_info,
                "status": chapter.status,
                "created_at": chapter.created_at,
                "updated_at": chapter.updated_at,
            }
            chapters_list.append(chapter_data)
        response_data = {
            "result": True,
            "data": chapters_list,
            "message": "Competitive chapters retrieved successfully"
        }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)


def get_comp_chapter(user, chapter_id):
    try:
        chapter = CompetitiveChapters.objects.get(id=chapter_id)
        subject_id = CompetitiveSubjects.objects.get(id=chapter.subject_name_id)
        batch_info = [{"id": str(batch.id), "batch_name": batch.batch_name} for batch in chapter.batches.all()]
        chapter_data = {
            "id": str(chapter.id),
            "chapter_name": chapter.chapter_name,
            "subject_id": str(subject_id.id),
            "subject_name": subject_id.subject_name,
            "batches":batch_info,
            "status": chapter.status,
            "created_at": chapter.created_at,
            "updated_at": chapter.updated_at,
        }
        response_data = {
                "result": True,
                "data": chapter_data,
                "message": "Competitive chapter retrieved successfully"
            }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


def update_comp_chapter(chapter_id, data):
    try:
        chapter = CompetitiveChapters.objects.get(id=chapter_id)
        if chapter:
            update_data = {field: value for field, value in data.dict().items() if value is not None}
            if update_data:
                for field, value in update_data.items():

                    if field == "subject_id":  
                        subject = CompetitiveSubjects.objects.get(id=value)
                        chapter.subject_id = subject

                    elif field == "batches":  
                        new_batches_instances = CompetitiveBatches.objects.filter(id__in=value)
                        new_batches = list(new_batches_instances)
                        
                        # Get the existing batch IDs
                        existing_batch_ids = chapter.batches.all().values_list("id", flat=True)
                        
                        # Add new batches
                        for new_batch in new_batches:
                            if new_batch.id not in existing_batch_ids:
                                chapter.batches.add(new_batch)
                        
                        # Remove batches not in the updated list
                        for existing_batch_id in existing_batch_ids:
                            if existing_batch_id not in value:
                                batch_to_remove = CompetitiveBatches.objects.get(id=existing_batch_id)
                                chapter.batches.remove(batch_to_remove)

                    else:
                        setattr(chapter, field, value)

                chapter.save()

                subject_id = CompetitiveSubjects.objects.get(id=chapter.subject_name_id)
                batch_info = [{"id": str(batch.id), "batch_name": batch.batch_name} for batch in chapter.batches.all()]
                chapter_data = {
                    "id": str(chapter.id),
                    "chapter_name": chapter.chapter_name,
                    "subject_id": str(subject_id.id),
                    "subject_name": subject_id.subject_name,
                    "batches":batch_info,
                    "status": chapter.status,
                    "created_at": chapter.created_at,
                    "updated_at": chapter.updated_at,
                }
                response_data = {
                        "result": True,
                        "data": chapter_data,
                        "message": "Competitive chapter updated successfully"
                    }
                return response_data
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400) 


def delete_comp_chapter(chapter_id):
    try:
        chapter = CompetitiveChapters.objects.get(id=chapter_id)
        chapter.delete()

        response_data = {"result":True,
                         "message":"Data Deleted Successfully"}
        return response_data
    
    except CompetitiveChapters.DoesNotExist:
        response_data = {
                    "result": False,
                    "message": "Chapter not found"
                }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


#-----------------------------------------------------------------------------------------------------------#
#-----------------------------------------COMPETITIVE QUESTIONS---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_comp_question(user,data):
    try:
        options_data = data.options  # Extract options data dictionary from the main data
        print("AREYRDWFJWJJKEOQ")
        # Create an instance of Options using options_data dictionary
        options_instance = Options.objects.create(
            option1=options_data.option1,
            option2=options_data.option2,
            option3=options_data.option3,
            option4=options_data.option4
        )
        print(options_instance, "AFwewqt$")
        # Split the time str    ing into hours and minutes
        hours, minutes = map(int, data.time.split(":"))

        # Create a timedelta representing the provided time
        time_duration = timedelta(hours=hours, minutes=minutes)
        print(time_duration)
        competitive_chapter = CompetitiveChapters.objects.get(id= data.chapter)
        print(competitive_chapter)
        # Create the question
        question = CompetitiveQuestions.objects.create(
            competitve_chapter=competitive_chapter,
            question=data.question,
            options=options_instance,  # Pass the instance of Options
            answer=data.answer,
            question_category=data.question_category,
            marks=data.marks,
            time_duration=str(time_duration),
            business_owner=user
        )

        return {
            "id": str(question.id),
            "question": question.question,
            "answer": question.answer,
            "options": options_data,  # Return the options data as-is
            "chapter": question.competitve_chapter_id,
            "question_category": question.question_category,
            "marks": question.marks,
            "time": question.time_duration # Convert timedelta to minutes
        }
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
 


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------STUDENT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def create_student(data, user):
    try:
        existing_student = Students.objects.filter(business_owner=user, contact_no=data.contact_no).first()
        if existing_student:
            response_data = {
                        "result": False,
                        "message": "Student with this contact number and eamil already exist."
                    }
            return JsonResponse(response_data, status=400)
        
        if data.batch and data.standard:
            response_data = {
                "result": False,
                "message": "You can only specify either 'batch' or 'standard', not both."
            }
            return JsonResponse(response_data, status=400)

        student_data = {
            "business_owner": user,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
            "contact_no": data.contact_no,
            "parent_name": data.parent_name,
            "parent_contact_no": data.parent_contact_no,
            "profile_image": data.profile_image,
            "address": data.address,
        }
        
        if data.batch:
            batch_instance = CompetitiveBatches.objects.get(id=data.batch)
            student_data["batch"] = batch_instance
        
        if data.standard:
            standard_instance = AcademicStandards.objects.get(id=data.standard)
            student_data["standard"] = standard_instance

        student = Students.objects.create(**student_data)

        response_data = {
            "result": True,
            "data": {
                "id": str(student.id),
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "contact_no": student.contact_no,
                "parent_name": student.parent_name,
                "parent_contact_no": student.parent_contact_no,
                "profile_image": student.profile_image.url if student.profile_image else None,
                "address": student.address,
                "competitive": {
                        "batch": str(student.batch.id) if student.batch else None,
                        "batch_name":student.batch.batch_name if student.batch else None
                },
                "academic":{
                        "board": str(student.standard.medium_name.board_name.id) if student.standard else None,
                        "board_name": student.standard.medium_name.board_name.board_name if student.standard else None,
                        "medium": str(student.standard.medium_name.id) if student.standard else None,
                        "medium_name": student.standard.medium_name.medium_name if student.standard else None,
                        "standard": str(student.standard.id) if student.standard else None,
                        "standard_name": student.standard.standard if student.standard else None  
                }
            },
            "message": "Student created successfully."
        }
        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)
 

def upload_student(xl_file, user):
    try:
        xl_data = pd.read_excel(xl_file.file)
        created_students = []

        for _, row in xl_data.iterrows():
            student_info = {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "contact_no": row["contact_no"],
                "parent_name": row["parent_name"],
                "parent_contact_no": row["parent_contact_no"],
                "address": row["address"],
            }

            batch_name = row.get("batch")
            if batch_name:
                batch_instance, _ = CompetitiveBatches.objects.get_or_create(batch_name=batch_name)
                student_info["batch"] = batch_instance
            
            board_name = row.get("board")
            if board_name:
                board_instance = AcademicBoards.objects.get(board_name=board_name)  

                medium_name = row.get("medium")
                if medium_name:
                    medium_instance = AcademicMediums.objects.get(board_name=board_instance, medium_name=medium_name)
                 
                    standard_id = row.get("standard")
                    if standard_id:
                        standard_instance = AcademicStandards.objects.get(medium_name=medium_instance, standard=standard_id)
                        student_info["standard"] = standard_instance

            existing_student = Students.objects.filter(business_owner=user, contact_no=student_info["contact_no"]).first()
            if existing_student:
                return JsonResponse({
                    "result": False,
                    "message": "Student with this contact number and email already exists."
                }, status=400)

            student_info["business_owner"] = user
            student = Students.objects.create(**student_info)
            created_students.append(student)
            
        response_data = {
            "result": True,
            "message": "Students created successfully."
        }
        return response_data

    except Exception as e:
        return JsonResponse({
            "result": False,
            "message": str(e)
        }, status=400)



def student_list(user, query):
    try:
        students = Students.objects.filter(business_owner=user)
        if query.status:
            students = students.filter(status=query.status)
        if query.batch:
            students = students.filter(batch=str(query.batch))
        if query.board:
            students = students.filter(standard__medium_name__board_name=str(query.board))
            print(query.board,"afh")
        if query.medium:
            students = students.filter(standard__medium_name=str(query.medium))
        if query.standard:
            students = students.filter(standard=str(query.standard))
        student_list = []
        for student in students:
            
            student_data = {
                "id": str(student.id),
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "contact_no": student.contact_no,
                "parent_name": student.parent_name,
                "parent_contact_no": student.parent_contact_no,
                "profile_image": student.profile_image.url if student.profile_image else None,
                "address": student.address,
                "competitive": {
                        "batch": str(student.batch.id) if student.batch else None,
                        "batch_name":student.batch.batch_name if student.batch else None
                },
                "academic":{
                        "board": str(student.standard.medium_name.board_name.id) if student.standard else None,
                        "board_name": student.standard.medium_name.board_name.board_name if student.standard else None,
                        "medium": str(student.standard.medium_name.id) if student.standard else None,
                        "medium_name": student.standard.medium_name.medium_name if student.standard else None,
                        "standard": str(student.standard.id) if student.standard else None,
                        "standard_name": student.standard.standard if student.standard else None  
                }
                
            }
            student_list.append(student_data)

        response_data = {
            "result": True,
            "data": student_list,
            "message": "Students retrieved successfully"
        }

        return response_data
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400) 


def student_detail(student_id):
    try:
        student = Students.objects.get(id=student_id)
        student_data = {
                "id": str(student.id),
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "contact_no": student.contact_no,
                "parent_name": student.parent_name,
                "parent_contact_no": student.parent_contact_no,
                "profile_image": student.profile_image.url if student.profile_image else None,
                "address": student.address,
                "competitive": {
                        "batch": str(student.batch.id) if student.batch else None,
                        "batch_name":student.batch.batch_name if student.batch else None
                },
                "academic":{
                        "board": str(student.standard.medium_name.board_name.id) if student.standard else None,
                        "board_name": student.standard.medium_name.board_name.board_name if student.standard else None,
                        "medium": str(student.standard.medium_name.id) if student.standard else None,
                        "medium_name": student.standard.medium_name.medium_name if student.standard else None,
                        "standard": str(student.standard.id) if student.standard else None,
                        "standard_name": student.standard.standard if student.standard else None  
                }  
        }
        response_data = {
            "result": True,
            "data": student_data,
            "message": "Student retrieved successfully"
        }

        return response_data
    
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)



def student_updation(student_id, data):
    try:
        student = Students.objects.get(id=student_id)
        if student:
            existing_student = Students.objects.filter(
                business_owner=student.business_owner,
                contact_no=data.contact_no,
            ).first()
            if existing_student:
                response_data = {
                    "result": False,
                    "message": "Student with this contact number already exists for the same business owner."
                }
                return JsonResponse(response_data, status=400)
            
            if data.batch and student.standard:
                response_data = {
                    "result": False,
                    "message": "You cannot update 'batch' when 'standard' is already assigned."
                }
                return JsonResponse(response_data, status=400)

            if data.standard and student.batch:
                response_data = {
                    "result": False,
                    "message": "You cannot update 'standard' when 'batch' is already assigned."
                }
                return JsonResponse(response_data, status=400)

            update_data = {field: value for field, value in data.dict().items() if value is not None}
            if update_data:
                for field, value in update_data.items():
                    if field == "standard":
                        try:
                            standard_instance = AcademicStandards.objects.get(id=value)
                            student.standard = standard_instance
                        except AcademicStandards.DoesNotExist:
                            response_data = {
                                "result": False,
                                "message": "Invalid standard UUID provided."
                            }
                            return JsonResponse(response_data, status=400)

                    elif field == "batch":
                        try:
                            batch_instance = CompetitiveBatches.objects.get(id=value)
                            student.batch = batch_instance
                        except CompetitiveBatches.DoesNotExist:
                            response_data = {
                                "result": False,
                                "message": "Invalid batch UUID provided."
                            }
                            return JsonResponse(response_data, status=400)

                    else:
                        setattr(student, field, value)
                
                student.save()

                student_data = {
                    "id": str(student.id),
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "email": student.email,
                    "contact_no": student.contact_no,
                    "parent_name": student.parent_name,
                    "parent_contact_no": student.parent_contact_no,
                    "profile_image": student.profile_image.url if student.profile_image else None,
                    "address": student.address,
                    "competitive": {
                        "batch": str(student.batch.id) if student.batch else None,
                        "batch_name":student.batch.batch_name if student.batch else None
                    },
                    "academic":{
                            "board": str(student.standard.medium_name.board_name.id) if student.standard else None,
                            "board_name": student.standard.medium_name.board_name.board_name if student.standard else None,
                            "medium": str(student.standard.medium_name.id) if student.standard else None,
                            "medium_name": student.standard.medium_name.medium_name if student.standard else None,
                            "standard": str(student.standard.id) if student.standard else None,
                            "standard_name": student.standard.standard if student.standard else None  
                    }  
                }
                response_data = {
                    "result": True,
                    "data": student_data,
                    "message": "Student updated successfully."
                }

                return response_data
    
    except Students.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Student not found."
        }
        return JsonResponse(response_data, status=404)
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=400)



def student_file_updation(xl_file, user):
    try:
        print(xl_file)
        xl_data = pd.read_excel(xl_file.file)
        print(xl_data)
        updated_students = []

        for _, row in xl_data.iterrows():
            student_info = {
                "contact_no": row["contact_no"]
            }
            print(student_info["contact_no"])
        
            student = Students.objects.filter(business_owner=user, contact_no=student_info["contact_no"]).first()
            print(student)
            batch_name = row.get("batch")
            if batch_name:
                batch_instance, _ = CompetitiveBatches.objects.get(batch_name=batch_name)
                student.batch = batch_instance
            
            board_name = row.get("board")
            if board_name:
                board_instance = AcademicBoards.objects.get(board_name=board_name)  

                medium_name = row.get("medium")
                if medium_name:
                    medium_instance = AcademicMediums.objects.get(board_name=board_instance, medium_name=medium_name)
                 
                    standard_id = row.get("standard")
                    if standard_id:
                        standard_instance = AcademicStandards.objects.get(medium_name=medium_instance, standard=standard_id)
                        student.standard = standard_instance


            student.save()
            updated_students.append(student)
        
        response_data = {
            "result": True,
            "message": "Students updated successfully."
        }
        return response_data

    except Exception as e:
        return JsonResponse({
            "result": False,
            "message": str(e)
        }, status=400)



def remove_student(student_id):
    try:
        student = Students.objects.get(id=student_id)
        student.delete()

        response_data = {"result":True,
                         "message":"Data Deleted Successfully"}
        return response_data
    
    except CompetitiveChapters.DoesNotExist:
        response_data = {
                    "result": False,
                    "message": "Chapter not found"
                }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)















































































































































































































































































































































































































































































####################################################################################
####--------------------------------ACADEMIC------------------------------------####
####################################################################################


def get_boards(user):
    try:
        academic_boards = AcademicBoards.objects.all()

        academic_list = [
            {
                "id": board.id,
                "board_name": board.board_name,
                "business_owner_id": board.business_owner_id,
                "status": board.status,
                "created_at": board.created_at,
                "updated_at": board.updated_at,
            }
            for board in academic_boards
        ]
        response_data = {
            "result": True,
            "data": academic_list,
            "message": "Academic boards retrieved successfully."
        }

        return JsonResponse(response_data,status=200)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong."
        }
        return JsonResponse(response_data,status=200)