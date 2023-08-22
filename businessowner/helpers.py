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
#----------------------------------------------CITY & STATE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def get_citylist():
    city_list = [] 
    cities = Cities.objects.all()
    for city in cities:
        city_dict = {
            "city_id": str(city.id),
            "city_name": city.name,
            "state_id": str(city.state.id),
            "state_name": city.state.name
        }
        city_list.append(city_dict)  
        response_data = {
            "result":True,
            "data":city_list,
            "message":"List of cities retrived successfully"
        }
    return response_data

def get_statelist():
    state_list =[]
    states = States.objects.all()
    for state in states:
        state_dict = {
            "state_id": str(state.id),
            "state_name": state.name
        }
        state_list.append(state_dict)
        response_data = {
            "result":True,
            "data":state_list,
            "message":"List of states retrived successfully"
        }
    return response_data


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
                "message": "Owner not found"
            }
        
        return response_data
    

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
            
            if update_data:
                for field, value in update_data.items():
                    if field == "city":
                        city = Cities.objects.get(id=value)
                        owner.city = city
                    elif field == "logo":
                        owner.logo = value
                    else:    
                        setattr(owner, field, value)
                owner.save()
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
                        "city_id": str(owner.city.id),
                        "city_name": owner.city.name,
                        "state_id": str(owner.city.state_id),
                        "state_name": owner.city.state.name,
                    },
                }

                response_data = {
                    "result": True,
                    "data": owner_data,
                    "message": "Profile updated successfully"
                }
            
                return response_data
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
                    "message": str(e)
                }
        return JsonResponse(response_data, status=500)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_batch(data, user):
    try:
        existing_batch = CompetitiveBatches.objects.filter(business_owner=user, batch_name=data.batch_name).first()
        if existing_batch:
            response_data = {
                        "result": False,
                        "message": "A batch with the same name already exists for this owner."
                    }
            return JsonResponse(response_data, status=400)
        
        batch = CompetitiveBatches(batch_name=data.batch_name, business_owner=user)
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
        if query.search:
            search_terms = query.search.strip().split()  
            search_query = Q()  
            for term in search_terms:
                search_query |= Q(batch_name__icontains=term)  

            batches = batches.filter(search_query)
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


def update_batch(batch_id, data, user):
    try:
        batch = CompetitiveBatches.objects.get(id=batch_id)
        if batch:
            existing_batch = CompetitiveBatches.objects.filter(business_owner=user, batch_name=data.batch_name).first()
            if existing_batch:
                response_data = {
                            "result": False,
                            "message": "A batch with the same name already exists for this owner."
                        }
                return JsonResponse(response_data, status=400)
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
        existing_subject = CompetitiveSubjects.objects.filter(business_owner=user, subject_name=data.subject_name).first()
        if existing_subject:
            response_data = {
                        "result": False,
                        "message": "A subject with the same name already exists for this owner."
                    }
            return JsonResponse(response_data, status=400)
        
        subject = CompetitiveSubjects.objects.create(subject_name=data.subject_name, business_owner=user)
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
        if query.search:
            search_terms = query.search.strip().split()  
            search_query = Q()  
            for term in search_terms:
                search_query |= Q(subject_name__icontains=term)  

            subjects = subjects.filter(search_query)
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

def update_comp_subject(subject_id, data, user):
    try:
        subject = CompetitiveSubjects.objects.get(id=subject_id)
        if subject:
            existing_subject = CompetitiveSubjects.objects.filter(business_owner=user, subject_name=data.subject_name).first()
            if existing_subject:
                response_data = {
                            "result": False,
                            "message": "A subject with the same name already exists for this owner."
                        }
                return JsonResponse(response_data, status=400)
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


def add_comp_chapter(data, user):
    try:
        existing_chapter = CompetitiveChapters.objects.filter(subject_name__business_owner=user, chapter_name=data.chapter_name).first()
        if existing_chapter:
            response_data = {
                        "result": False,
                        "message": "A chapter with the same name already exists for this owner."
                    }
            return JsonResponse(response_data, status=400)

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
        if query.search:
            search_terms = query.search.strip().split()  
            search_query = Q()  
            for term in search_terms:
                search_query |= Q(chapter_name__icontains=term) | Q(subject_name__subject_name__icontains=term) | Q(batches__batch_name__icontains=term)

            chapters = chapters.filter(search_query)

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
    except CompetitiveChapters.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Chapter not found"
        }
        return JsonResponse(response_data, status=400)
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
    
    except CompetitiveChapters.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Chapter not found"
        }
        return JsonResponse(response_data, status=400)
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


def update_comp_chapter(chapter_id, data, user):
    try:
        chapter = CompetitiveChapters.objects.get(id=chapter_id)
        if chapter:
            existing_chapter = CompetitiveChapters.objects.filter(subject_name__business_owner=user, chapter_name=data.chapter_name).first()
            if existing_chapter:
                response_data = {
                            "result": False,
                            "message": "A chapter with the same name already exists for this owner."
                        }
                return JsonResponse(response_data, status=400)
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
    except CompetitiveChapters.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Chapter not found"
        }
        return JsonResponse(response_data, status=400)
    except CompetitiveSubjects.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Subject not found"
        }
        return JsonResponse(response_data, status=400)
    except CompetitiveBatches.DoesNotExist:
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
        options_data = data.options  

        options_instance = Options.objects.create(
            option1=options_data.option1,
            option2=options_data.option2,
            option3=options_data.option3,
            option4=options_data.option4
        )

        

        competitive_chapter = CompetitiveChapters.objects.get(id= data.chapter)
        question = CompetitiveQuestions.objects.create(
            competitve_chapter=competitive_chapter,
            question=data.question,
            options=options_instance,  
            answer=data.answer,
            question_category=data.question_category,
            marks=data.marks,
            time_duration=data.time,
            business_owner=user
        )

        chapter = CompetitiveChapters.objects.get(id=question.competitve_chapter_id)
        subject = CompetitiveSubjects.objects.get(id=chapter.subject_name.id)
        question_data = {
            "id": str(question.id),
            "question": question.question,
            "answer": question.answer,
            "options": options_data,  
            "chapter_id": str(question.competitve_chapter.id),
            "chapter_name": question.competitve_chapter.chapter_name,
            "subject_id": str(question.competitve_chapter.subject_name.id),
            "subject_name": question.competitve_chapter.subject_name.subject_name,
            "question_category": question.question_category,
            "marks": question.marks,
            "time": str(question.time_duration),
            "status": question.status,
            "created_at":question.created_at,
            "updated_at":question.updated_at
        }

        response_data = {
            "result": True,
            "data": question_data,
            "message":"Question added successfully"
        }
        return response_data

    except Options.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Options not found"
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
 

def get_comp_questionlist(user, query):
    try:
        questions = CompetitiveQuestions.objects.filter(business_owner=user)
        if query.status:
            questions = questions.filter(status=query.status)
        if query.chapter:
            questions = questions.filter(competitve_chapter=query.chapter)
        if query.subject:
            questions = questions.filter(competitve_chapter__subject_name=query.subject)
        if query.batch:
            batch_id = query.batch
            questions = [question for question in questions if str(batch_id) in [str(batch.id) for batch in question.competitve_chapter.batches.all()]]

        if query.question_category:
            questions = questions.filter(question_category=query.question_category)

        if query.search:
            search_terms = query.search.strip().split()
            search_query = Q()

            for term in search_terms:
                search_query |= (
                    Q(question__icontains=term)
                    | Q(answer__icontains=term)
                    | Q(competitve_chapter__chapter_name__icontains=term)
                    | Q(competitve_chapter__subject_name__subject_name__icontains=term)
                    | Q(competitve_chapter__batches__batch_name__icontains=term)
                    | Q(question_category__icontains=term)
                    | Q(marks__icontains=term)
                    | Q(time_duration__icontains=term)
                    | Q(status__icontains=term)
                )

            questions = questions.filter(search_query)

        question_list = []
        for question in questions:
            try:
                options_data = Options.objects.get(id=question.options_id)
            except Options.DoesNotExist:
                options_data = None  
            
            options_dict = {
                "option1": options_data.option1 if options_data else None,
                "option2": options_data.option2 if options_data else None,
                "option3": options_data.option3 if options_data else None,
                "option4": options_data.option4 if options_data else None,
            }
            question_data = {
                    "id": str(question.id),
                    "question": question.question,
                    "answer": question.answer,
                    "options": options_dict,  
                    "chapter_id": str(question.competitve_chapter.id),
                    "chapter_name": question.competitve_chapter.chapter_name,
                    "subject_id": str(question.competitve_chapter.subject_name.id),
                    "subject_name": question.competitve_chapter.subject_name.subject_name, 
                    "question_category": question.question_category,
                    "marks": question.marks,
                    "time": str(question.time_duration),
                    "status": question.status,
                    "created_at":question.created_at,
                    "updated_at":question.updated_at
                }
            question_list.append(question_data)
            
        response_data = {
            "result": True,
            "data": question_list,
            "message":"Question retrieved successfully"
        }
        return response_data

    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)


def get_comp_question(user, question_id):
    try:
        question = CompetitiveQuestions.objects.get(id=question_id)
        try:
            options_data = Options.objects.get(id=question.options_id)
        except Options.DoesNotExist:
            options_data = None 
        
        options_dict = {
            "option1": options_data.option1 if options_data else None,
            "option2": options_data.option2 if options_data else None,
            "option3": options_data.option3 if options_data else None,
            "option4": options_data.option4 if options_data else None,
        }
        question_data = {
                "id": str(question.id),
                "question": question.question,
                "answer": question.answer,
                "options": options_dict, 
                "chapter_id": str(question.competitve_chapter.id),
                "chapter_name": question.competitve_chapter.chapter_name,
                "subject_id": str(question.competitve_chapter.subject_name.id),
                "subject_name": question.competitve_chapter.subject_name.subject_name, 
                "question_category": question.question_category,
                "marks": question.marks,
                "time": str(question.time_duration),
                "status": question.status,
                "created_at":question.created_at,
                "updated_at":question.updated_at
            }
        
        response_data = {
            "result": True,
            "data": question_data,
            "message":"Question retrieved successfully"
        }
        return response_data
    except CompetitiveQuestions.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Question not found"
        }
        return JsonResponse(response_data, status=400)
    except Options.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Options not found"
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)
    

def update_comp_question(question_id, data):
    try:
        question = CompetitiveQuestions.objects.get(id=question_id)
        try:
            options_data = Options.objects.get(id=question.options_id)
        except Options.DoesNotExist:
            options_data = None  
    
        update_data = {field: value for field, value in data.dict().items() if value is not None}
        
        if update_data:
            if "options" in update_data and options_data:
                new_options = update_data.pop("options")
                for field, value in new_options.items():
                    if hasattr(options_data, field) and value is not None:
                        setattr(options_data, field, value)
                options_data.save()

            for field, value in update_data.items():
                if field == "chapter":
                    chapter = CompetitiveChapters.objects.get(id=value)
                    question.competitve_chapter = chapter
                elif field == "time":
                    hours, minutes = map(int, data.time.split(":"))
                    time_duration = timedelta(hours=hours, minutes=minutes)
                    question.time_duration = str(time_duration)

                else:
                    setattr(question, field, value)
            question.save()
            question_data = {
                "id": str(question.id),
                "question": question.question,
                "answer": question.answer,
                "chapter_id": str(question.competitve_chapter.id),
                "chapter_name": question.competitve_chapter.chapter_name,
                "subject_id": str(question.competitve_chapter.subject_name.id),
                "subject_name": question.competitve_chapter.subject_name.subject_name, 
                "question_category": question.question_category,
                "marks": question.marks,
                "time": str(question.time_duration),
                "status": question.status,
                "created_at":question.created_at,
                "updated_at":question.updated_at
            }
            if options_data:
                options_dict = {
                    "option1": options_data.option1,
                    "option2": options_data.option2,
                    "option3": options_data.option3,
                    "option4": options_data.option4,
                }
                question_data["options"] = options_dict
            else:
                options_dict = {
                    "option1": question_data.options_data.option1,
                    "option2": question_data.options_data.option2,
                    "option3": question_data.options_data.option3,
                    "option4": question_data.options_data.option4,
                }
                question_data["options"] = options_dict
        
            response_data = {
                "result": True,
                "data": question_data,
                "message":"Question retrieved successfully"
            }
            return response_data

    except CompetitiveQuestions.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Question not found"
        }
        return JsonResponse(response_data, status=400)
    except Options.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Options not found"
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
    

def delete_comp_question(question_id):
    try:
        question = CompetitiveQuestions.objects.get(id=question_id)
        options = Options.objects.get(id=question.options_id)
        options.delete()
        question.delete()
        

        response_data = {"result":True,
                         "message":"Data Deleted Successfully"}
        return response_data
    
    except CompetitiveQuestions.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Question not found"
        }
        return JsonResponse(response_data, status=400)
    except Options.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Options not found"
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
                    "result": False,
                    "message": "Something went wrong"
                }
        return JsonResponse(response_data, status=400)


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------COMPETITIVE EXAM-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def create_comp_exam(user, data):
    try:
        batch_instance = CompetitiveBatches.objects.get(id=data.batch)

        total_weightage = data.total_questions

        exam_data_calculated = []

        for subject_data in data.exam_data:
            subject_weightage = sum(
                qtype for qtype in [subject_data.easy_question, subject_data.medium_question, subject_data.hard_question]
            )
            subject_percentage = subject_weightage / total_weightage
            subject_time = float(data.time_duration * subject_percentage)
            subject_marks = int(data.total_marks * subject_percentage)

            subject_instance = CompetitiveSubjects.objects.get(id=subject_data.subject)
            
            chapter_instance = CompetitiveChapters.objects.filter(id__in=subject_data.chapter)
            chapters = list(chapter_instance)
            chapter_ids = [f"{item.id}," for item in chapters]
            chapters = " ".join(chapter_ids)
            print(chapters, "AJDJDIEWQIWQ")
            question_data = CompetitiveQuestions.objects.filter(competitve_chapter__subject_name=subject_instance)
            question_data = question_data.filter(competitve_chapter__id__in=subject_data.chapter)
            selected_questions = []
            selected_time = 0
            selected_marks = 0
            remaining_easy_questions = subject_data.easy_question
            remaining_medium_questions = subject_data.medium_question
            remaining_hard_questions = subject_data.hard_question
            selected_comp_questions = []
        
            for question in question_data:
                if remaining_easy_questions > 0:
                    if question.question_category == "easy":
                        if selected_time + question.time_duration <= subject_time and selected_marks + question.marks <= subject_marks:
                            selected_questions.append(question)
                            selected_time += question.time_duration
                            selected_marks += question.marks
                            remaining_easy_questions -= 1
                elif remaining_medium_questions > 0:
                    if question.question_category == "medium":
                        if selected_time + question.time_duration <= subject_time and selected_marks + question.marks <= subject_marks:
                            selected_questions.append(question)
                            selected_time += question.time_duration
                            selected_marks += question.marks
                            remaining_medium_questions -= 1
                elif remaining_hard_questions > 0:
                    if question.question_category == "hard":
                        if selected_time + question.time_duration <= subject_time and selected_marks + question.marks <= subject_marks:
                            selected_questions.append(question)
                            selected_time += question.time_duration
                            selected_marks += question.marks
                            remaining_hard_questions -= 1
                else:
                    break  
            
            
            
            for question in selected_questions:
                comp_exam_instance = CompExam(
                    question=question.question,    
                )
                selected_comp_questions.append(comp_exam_instance)
            print(selected_comp_questions)
            
            exam_data_instance = CompetitiveExamData(
                subject=subject_instance,
                easy_question=subject_data.easy_question,
                chapter=chapters,
                medium_question=subject_data.medium_question,
                hard_question=subject_data.hard_question,
                time_per_subject=subject_time,
                marks_per_subject=subject_marks,
            )
            exam_data_instance.save() 
    
            exam_data_calculated.append(exam_data_instance) 
            
        
        exam_instance = CompetitiveExams(
            exam_title=data.exam_title,
            batch=batch_instance,
            total_questions=data.total_questions,
            time_duration=data.time_duration,
            passing_marks=data.passing_marks,
            total_marks=data.total_marks,
            negative_marks=data.negative_marks,
            option_e=data.option_e
        )
        exam_instance.save()
        for exam in exam_data_calculated:
            exam_instance.exam_data.add(exam) 
       
        return selected_comp_questions

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return response_data



#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------STUDENT----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def create_student(data, user):
    try:
        existing_student = Students.objects.filter(business_owner=user, contact_no=data.contact_no).first()

        if existing_student:
            response_data = {
                "result": False,
                "message": "A student with this contact number already exists for this business owner."
            }
            return JsonResponse(response_data, status=400)

        existing_email = Students.objects.filter(business_owner=user, email=data.email).first()

        if existing_email:
            response_data = {
                "result": False,
                "message": "A student with this email already exists for this business owner."
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
            "message": "Something went wrong"
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
        if query.search:
            search_terms = query.search.strip().split()
            search_query = Q()

            for term in search_terms:
                search_query |= (
                    Q(first_name__icontains=term)
                    | Q(last_name__icontains=term)
                    | Q(email__icontains=term)
                    | Q(parent_name__icontains=term)
                    | Q(address__icontains=term)
                    | Q(batch__batch_name__icontains=term)
                    | Q(standard__standard__icontains=term)
                    | Q(standard__medium_name__medium_name__icontains=term)
                    | Q(standard__medium_name__board_name__board_name__icontains=term)
                    | Q(status__icontains=term)
                )

            students = students.filter(search_query)
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
                    "message": "Something went wrong"
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
            existing_student = Students.objects.filter(business_owner=student.business_owner, contact_no=data.contact_no).first()

            if existing_student:
                response_data = {
                    "result": False,
                    "message": "A student with this contact number already exists for this business owner."
                }
                return JsonResponse(response_data, status=400)

            existing_email = Students.objects.filter(business_owner=student.business_owner, email=data.email).first()

            if existing_email:
                response_data = {
                    "result": False,
                    "message": "A student with this email already exists for this business owner."
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
            "message": "Something went wrong"
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
            "message": "Something went wrong"
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


def get_boards_list(user,filter_prompt):
    print(filter_prompt)
    try:
        academic_boards = AcademicBoards.objects.all()

        if filter_prompt.search:
            q_objects = Q(board_name__icontains=filter_prompt.search) | Q(business_owner__business_name__icontains=filter_prompt.search)
            academic_boards = academic_boards.filter(q_objects)
            
        elif filter_prompt.status:
            print(filter_prompt)
            academic_boards = academic_boards.filter(status=filter_prompt.status)
        print(academic_boards)
        # else:
        #     academic_boards = AcademicBoards.objects.all()

        academic_list = [
            {
                "id": str(board.id),
                "board_name": board.board_name,
                "business_owner": board.business_owner.business_name,
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

        return response_data
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong."
        }
        return JsonResponse(response_data,status=200)
    
def get_academic_board_data(user,board_id):
    try:
        academic_boards = AcademicBoards.objects.get(id=board_id)

        academic_board = {
                "id": str(academic_boards.id),
                "board_name": academic_boards.board_name,
                "business_owner": academic_boards.business_owner.business_name,
                "status": academic_boards.status,
                "created_at": academic_boards.created_at,
                "updated_at": academic_boards.updated_at,
            }

        response_data = {
            "result": True,
            "data": academic_board,
            "message": "Academic board retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong."
        }
        return JsonResponse(response_data, status=500)

def add_baord(user, data):
    try:
        # Create a new AcademicBoard instance
        board = AcademicBoards.objects.create(
            board_name=data.board_name,
            business_owner=user,
        )
        # Return the saved board data as a response
        saved_board = {
            "id": str(board.id),
            "board_name": board.board_name,
            "business_owner": user.business_name,  # Use the business owner's name from the token
            "status": board.status,
            "created_at": board.created_at,
            "updated_at": board.updated_at,
        }

        response_data = {
            "result": True,
            "data": saved_board,
            "message": "board added successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": "somthing went wrong."
        }

        return JsonResponse(response_data,status=400)


def update_board_data(user,data,board_id):
    try:
        # Check if the academic board exists
        academic_board = AcademicBoards.objects.get(id=board_id, business_owner=user)

        update_data = {field: value for field, value in data.dict().items() if value is not None}
        
        # Update the board_name and status
        for field, value in update_data.items():
            setattr(academic_board, field, value)
        
        academic_board.save()

        updated_board = {
            "id": str(academic_board.id),
            "board_name": academic_board.board_name,
            "business_owner": academic_board.business_owner.business_name,
            "status": academic_board.status,
            "created_at": academic_board.created_at,
            "updated_at": academic_board.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_board,
            "message": "Academic board updated successfully."
        }

        return response_data 

    except Exception as e:
        response_data = {
            "result": False,
            "message": "somthing went wrong."
        }

        return JsonResponse(response_data,status=400)


def delete_board_data(user,board_id):
    try:
        # Check if the academic board exists
        academic_board = AcademicBoards.objects.get(id=board_id, business_owner=user)
        
        # Delete the academic board
        academic_board.delete()

        response_data = {
            "result": True,
            "message": "Academic board deleted successfully."
        }

        return response_data

    except AcademicBoards.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Academic board not found."
        }
        return JsonResponse(response_data, status=404)
    
    except Exception as e:
        response_data = {
            "error": "Something went wrong"
        }
        return JsonResponse(response_data, status=500)
    

def get_academic_mediums_list(filter_prompt):
    try:
        academic_mediums = AcademicMediums.objects.all()

        if filter_prompt.search:
            q_objects = Q(medium_name__icontains=filter_prompt.search) | Q(board_name__board_name__icontains=filter_prompt.search)
            academic_mediums = academic_mediums.filter(q_objects)

        elif filter_prompt.status and filter_prompt.board_id and filter_prompt.medium_id:
            academic_mediums = academic_mediums.filter(
                status=filter_prompt.status,
                board_name__id=filter_prompt.board_id,
                id=filter_prompt.medium_id
            )
        elif filter_prompt.status and filter_prompt.board_id:
            academic_mediums = academic_mediums.filter(
                status=filter_prompt.status,
                board_name__id=filter_prompt.board_id
            )
        elif filter_prompt.status and filter_prompt.medium_id:
            academic_mediums = academic_mediums.filter(
                status=filter_prompt.status,
                id=filter_prompt.medium_id
            )
        elif filter_prompt.board_id and filter_prompt.medium_id:
            academic_mediums = academic_mediums.filter(
                board_name__id=filter_prompt.board_id,
                id=filter_prompt.medium_id
            )
        elif filter_prompt.status:
            academic_mediums = academic_mediums.filter(status=filter_prompt.status)
        elif filter_prompt.board_id:
            academic_mediums = academic_mediums.filter(board_name__id=filter_prompt.board_id)
        elif filter_prompt.medium_id:
            academic_mediums = academic_mediums.filter(id=filter_prompt.medium_id)
        academic_medium_list = [
            {
                "id": str(medium.id),
                "medium_name": medium.medium_name,
                "board_id": str(medium.board_name.id),
                "board_name": medium.board_name.board_name,
                "status": medium.status,
                "created_at": medium.created_at,
                "updated_at": medium.updated_at,
            }
            for medium in academic_mediums
        ]
        
        response_data = {
            "result": True,
            "data": academic_medium_list,
            "message": "Academic mediums retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong."
        }
        return JsonResponse(response_data, status=500)

def get_academic_medium_data(user,medium_id):
    try:
        academic_mediums = AcademicMediums.objects.get(id=medium_id)

        academic_medium_list = {
                "id": str(academic_mediums.id),
                "medium_name": academic_mediums.medium_name,
                "board_id": str(academic_mediums.board_name.id),
                "board_name": academic_mediums.board_name.board_name,
                "status": academic_mediums.status,
                "created_at": academic_mediums.created_at,
                "updated_at": academic_mediums.updated_at,
            }
    
        response_data = {
            "result": True,
            "data": academic_medium_list,
            "message": "Academic mediums retrieved successfully."
        }
        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": print(e)
        }
        return JsonResponse(response_data, status=500)

from django.http import JsonResponse
import uuid

def add_medium_data(user, data):
    try:
        board_id = data.get('board_id')  # Fetch board_id (UUID) from the request data
        board_instance = AcademicBoards.objects.get(id=board_id) 
        print(board_instance) # Convert to UUID and fetch the corresponding board instance
        
        medium = AcademicMediums.objects.create(
            medium_name=data.get('medium_name'),
            board_name=board_instance,  # Use the fetched board instance
        )
    
        
        saved_medium = {
            "id": str(medium.id),
            "medium_name": medium.medium_name,
            "board_id": str(medium.board_name.id),
            "board_name": medium.board_name.board_name,
            "status": medium.status,
            "created_at": medium.created_at,
            "updated_at": medium.updated_at,
        }

        response_data = {
            "result": True,
            "data": saved_medium,
            "message": "Medium added successfully."
        }

        return response_data

    except Exception as e:
        error_response = {
            "result": False,
            "message": "An error occurred while adding the medium."
        }
        return JsonResponse(error_response, status=500, safe=False)



def update_medium_data(user,data,medium_id):
    try:
        # Check if the academic board exists
        print(data,"DATA")
        academic_medium = AcademicMediums.objects.get(id=medium_id)
        print(academic_medium)
        try:
            data.board_name = AcademicBoards.objects.get(id=data.board_name)
            print(data.board_name)
        except:
            data.board_name = academic_medium.board_name
        update_data = {field: value for field, value in data.dict().items() if value!= None}
        print(update_data,"fsdfsdf")
        
        # Update the board_name and status
        for field, value in update_data.items():
            setattr(academic_medium, field, value)

        # academic_medium.board_name = academic_board
       
        academic_medium.save()
        print(academic_medium,"hgjhj")
        updated_board = {
            "id": str(academic_medium.id),
            "medium_name":academic_medium.medium_name,
            "board_id": str(academic_medium.board_name.id),
            "board_name": academic_medium.board_name.board_name,
            "status": academic_medium.status,
            "created_at": academic_medium.created_at,
            "updated_at": academic_medium.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_board,
            "message": "Academic board updated successfully."
        }

        return response_data

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def delete_medium_data(user,medium_id):
    try:
        # Check if the academic board exists
        academic_medium = AcademicMediums.objects.get(id=medium_id)
        
        # Delete the academic board
        academic_medium.delete()

        response_data = {
            "result": True,
            "message": "Academic medium deleted successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=404)



    

def get_academic_standard_list(filter_prompt):
    try:
        academic_standards = AcademicStandards.objects.all()

        if filter_prompt.search:
            q_objects = (
                Q(medium_name__medium_name__icontains=filter_prompt.search) |
                Q(standard__icontains=filter_prompt.search)
            )
            academic_standards = academic_standards.filter(q_objects)

        elif filter_prompt.status and filter_prompt.medium_id and filter_prompt.board_id and filter_prompt.standard:
            academic_standards = academic_standards.filter(
                status=filter_prompt.status,
                medium_name__id=filter_prompt.medium_id,
                medium_name__board_name__id=filter_prompt.board_id,
                id=filter_prompt.standard
            )
        elif filter_prompt.status and filter_prompt.medium_id and filter_prompt.board_id:
            academic_standards = academic_standards.filter(
                status=filter_prompt.status,
                medium_name__id=filter_prompt.medium_id,
                medium_name__board_name__id=filter_prompt.board_id
            )
        elif filter_prompt.status and filter_prompt.medium_id:
            academic_standards = academic_standards.filter(
                status=filter_prompt.status,
                medium_name__id=filter_prompt.medium_id
            )
        elif filter_prompt.status and filter_prompt.board_id:
            academic_standards = academic_standards.filter(
                status=filter_prompt.status,
                medium_name__board_name__id=filter_prompt.board_id
            )
        elif filter_prompt.medium_id and filter_prompt.board_id:
            academic_standards = academic_standards.filter(
                medium_name__id=filter_prompt.medium_id,
                medium_name__board_name__id=filter_prompt.board_id
            )
        elif filter_prompt.status:
            academic_standards = academic_standards.filter(status=filter_prompt.status)
        elif filter_prompt.medium_id:
            academic_standards = academic_standards.filter(medium_name__id=filter_prompt.medium_id)
        elif filter_prompt.board_id:
            academic_standards = academic_standards.filter(medium_name__board_name__id=filter_prompt.board_id)
        elif filter_prompt.standard:
            academic_standards = academic_standards.filter(id=filter_prompt.standard)
        academic_standard_list = [
            {
                "id": str(standards.id),
                "standard": standards.standard,
                "medium_id": str(standards.medium_name.id),
                "medium_name": standards.medium_name.medium_name,
                "status": standards.status,
                "created_at": standards.created_at,
                "updated_at": standards.updated_at,
            }
            for standards in academic_standards
        ]
        
        response_data = {
            "result": True,
            "data": academic_standard_list,
            "message": "Academic standard retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=500)
    

def add_standard_data(user, data):

    try:

        medium_id = data.medium_id 
    
        medium_instance = AcademicMediums.objects.get(id=medium_id) 
     # Convert to UUID and fetch the corresponding board instance
        print(medium_instance)
        standards = AcademicStandards.objects.create(
            standard=data.standard,
            medium_name=medium_instance,  # Use the fetched board instance
        )
        print(standards)
    
        
        saved_standard = {
            "id": str(standards.id),
            "standard":standards.standard,
            "medium_id":str(standards.medium_name.id),
            "medium_name": standards.medium_name.medium_name,
            "status": standards.status,
            "created_at": standards.created_at,
            "updated_at": standards.updated_at,
        }
     
        response_data = {
            "result": True,
            "data": saved_standard,
            "message": "standard added successfully."
        }

        return response_data 

    except Exception as e:
        error_response = {
            "result": False,
            "message": str(e),
        }
        return JsonResponse(error_response, status=500, safe=False)
    

def delete_standard_data(user,standard_id):
    try:
        # Check if the academic board exists
        academic_standard = AcademicStandards.objects.get(id=standard_id)
        
        # Delete the academic board
        academic_standard.delete()

        response_data = {
            "result": True,
            "message": "Academic standard deleted successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=404)
    

def get_academic_standard_data(standard_id):
    try:
        academic_standards = AcademicStandards.objects.get(id=standard_id)

        academic_standard_list = {
                "id": str(academic_standards.id),
                "standard":academic_standards.standard,
                "medium_id":str(academic_standards.medium_name.id),
                "medium_name": academic_standards.medium_name.medium_name,
                "status": academic_standards.status,
                "created_at": academic_standards.created_at,
                "updated_at": academic_standards.updated_at,
            }

        response_data = {
            "result": True,
            "data": academic_standard_list,
            "message": "Academic mediums retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": print(e)
        }
        return JsonResponse(response_data, status=500)
    

def update_standard_data(user,data,standard_id):
    try:
        # Check if the academic board exists
        print(data,"DATA")
        academic_standard = AcademicStandards.objects.get(id=standard_id)
        print(academic_standard)
        try:
            data.medium_name = AcademicMediums.objects.get(id=data.medium_name)
            print(data.medium_name)
        except:
            data.medium_name = academic_standard.medium_name
        update_data = {field: value for field, value in data.dict().items() if value!= None}
        print(update_data,"fsdfsdf")
        
        # Update the board_name and status
        for field, value in update_data.items():
            setattr(academic_standard, field, value)

        # academic_medium.board_name = academic_board
       
        academic_standard.save()
        print(academic_standard,"hgjhj")
        updated_standard = {
            "id": str(academic_standard.id),
            "standard":academic_standard.standard,
            "medium_id": str(academic_standard.medium_name.id),
            "medium_name": academic_standard.medium_name.medium_name,
            "status": academic_standard.status,
            "created_at": academic_standard.created_at,
            "updated_at": academic_standard.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_standard,
            "message": "Academic stnadard updated successfully."
        }

        return response_data

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def get_academic_subject_list(filter_prompt):
    try:
        academic_subjects = AcademicSubjects.objects.all()

        # if filter_prompt:
        #     print(filter_prompt)
        #     academic_subjects = academic_subjects.filter(**filter_prompt)

        q_objects = Q()

        if filter_prompt.status:
            q_objects &= Q(status=filter_prompt.status)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        if filter_prompt.medium_id and filter_prompt.board_id and filter_prompt.standard:
            q_objects &= (
                Q(standard__medium_name__id=filter_prompt.medium_id) &
                Q(standard__medium_name__board_name__id=filter_prompt.board_id) &
                Q(standard__id=filter_prompt.standard)
            )
        elif filter_prompt.medium_id and filter_prompt.board_id:
            q_objects &= (
                Q(standard__medium_name__id=filter_prompt.medium_id) &
                Q(standard__medium_name__board_name__id=filter_prompt.board_id)
            )
        elif filter_prompt.medium_id:
            q_objects &= Q(standard__medium_name__id=filter_prompt.medium_id)
        elif filter_prompt.board_id:
            q_objects &= Q(standard__medium_name__board_name__id=filter_prompt.board_id)
        elif filter_prompt.standard:
            q_objects &= Q(standard__id=filter_prompt.standard)

        elif filter_prompt.subject_id:
            print(filter_prompt.subject_id)
            q_objects &= Q(id=filter_prompt.subject_id)

        academic_subjects = academic_subjects.filter(q_objects)

        academic_subject_list = [
            {
                "id": str(subject.id),
                "subject_name": subject.subject_name,
                "standard_id": str(subject.standard.id),
                "standard": subject.standard.standard,
                "status": subject.status,
                "created_at": subject.created_at,
                "updated_at": subject.updated_at,
            }
            for subject in academic_subjects
        ]
        
        response_data = {
            "result": True,
            "data": academic_subject_list,
            "message": "Academic subject retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=500)
    

def add_subject_data(user, data):

    try:

        standard_id = data.standard_id 
    
        standard_instance = AcademicStandards.objects.get(id=standard_id) 
     # Convert to UUID and fetch the corresponding board instance
        print(standard_instance)
        subjects = AcademicSubjects.objects.create(
            subject_name=data.subject_name,
            standard=standard_instance,  # Use the fetched board instance
        )
        print(subjects)
    
        
        saved_subject = {
            "id": str(subjects.id),
            "subject_name":subjects.subject_name,
            "standard_id":str(subjects.standard.id),
            "standard": subjects.standard.standard,
            "status": subjects.status,
            "created_at": subjects.created_at,
            "updated_at": subjects.updated_at,
        }
     
        response_data = {
            "result": True,
            "data": saved_subject,
            "message": "subject added successfully."
        }

        return response_data 

    except Exception as e:
        error_response = {
            "result": False,
            "message": str(e),
        }
        return JsonResponse(error_response, status=500, safe=False)


def get_academic_subject_data(subject_id):
    try:
        academic_subjects = AcademicSubjects.objects.get(id=subject_id)

        academic_standard_list = {
                "id": str(academic_subjects.id),
                "subject_name":academic_subjects.subject_name,
                "standard_id":str(academic_subjects.standard.id),
                "standard": academic_subjects.standard.standard,
                "status": academic_subjects.status,
                "created_at": academic_subjects.created_at,
                "updated_at": academic_subjects.updated_at,
            }

        response_data = {
            "result": True,
            "data": academic_standard_list,
            "message": "Academic subject retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": print(e)
        }
        return JsonResponse(response_data, status=500)
    

def delete_subject_data(user,subject_id):
    try:
        # Check if the academic board exists
        academic_subject = AcademicSubjects.objects.get(id=subject_id)
        
        # Delete the academic board
        academic_subject.delete()

        response_data = {
            "result": True,
            "message": "Academic subject deleted successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=404)
    

def update_subject_data(user,data,subject_id):
    try:
        # Check if the academic board exists
        print(data,"DATA")
        academic_subjects = AcademicSubjects.objects.get(id=subject_id)
        print(academic_subjects)
        try:
            data.standard = AcademicStandards.objects.get(id=data.standard)
        except:
            data.standard = academic_subjects.standard
        update_data = {field: value for field, value in data.dict().items() if value!= None}
        print(update_data,"fsdfsdf")
        
        # Update the board_name and status
        for field, value in update_data.items():
            setattr(academic_subjects, field, value)

        # academic_medium.board_name = academic_board
       
        academic_subjects.save()
        print(academic_subjects,"hgjhj")
        updated_subject = {
            "id": str(academic_subjects.id),
            "subject_name":academic_subjects.subject_name,
            "standard_id": str(academic_subjects.standard.id),
            "standard": academic_subjects.standard.standard,
            "status": academic_subjects.status,
            "created_at": academic_subjects.created_at,
            "updated_at": academic_subjects.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_subject,
            "message": "Academic subject updated successfully."
        }

        return response_data

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    




def get_academic_chapter_list(filter_prompt):
    try:
        academic_chapters = AcademicChapters.objects.all()

        if filter_prompt.status:
            print(filter_prompt)
            academic_chapters = academic_chapters.filter(status=filter_prompt.status)

        elif filter_prompt.subject_id:
            academic_chapters = academic_chapters.filter(subject_name__id=filter_prompt.subject_id)

        elif filter_prompt.chapter_id:
            academic_chapters = academic_chapters.filter(id=filter_prompt.chapter_id)

        academic_chapters_list = [
            {
                "id": str(chapter.id),
                "chapter_name": chapter.chapter_name,
                "subject_id": str(chapter.subject_name.id),
                "subject_name": chapter.subject_name.subject_name,
                "status": chapter.status,
                "created_at": chapter.created_at,
                "updated_at": chapter.updated_at,
            }
            for chapter in academic_chapters
        ]
        
        response_data = {
            "result": True,
            "data": academic_chapters_list,
            "message": "Academic chapter retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=500)
    

def add_chapter_data(user, data):

    try:

        subject_id = data.subject_id 
    
        subject_instance = AcademicSubjects.objects.get(id=subject_id) 
     # Convert to UUID and fetch the corresponding board instance
        print(subject_instance)
        chapter = AcademicChapters.objects.create(
            chapter_name=data.chapter_name,
            subject_name=subject_instance,  # Use the fetched board instance
        )
        print(chapter)
    
        
        saved_chapter = {
            "id": str(chapter.id),
            "chapter_name":chapter.chapter_name,
            "subject_id":str(chapter.subject_name.id),
            "subject_name": chapter.subject_name.subject_name,
            "status": chapter.status,
            "created_at": chapter.created_at,
            "updated_at": chapter.updated_at,
        }
     
        response_data = {
            "result": True,
            "data": saved_chapter,
            "message": "chapter added successfully."
        }

        return response_data 

    except Exception as e:
        error_response = {
            "result": False,
            "message": str(e),
        }
        return JsonResponse(error_response, status=500, safe=False)
    

def get_academic_chapter_data(chapter_id):
    try:
        academic_chapters = AcademicChapters.objects.get(id=chapter_id)

        

        academic_chapter_list = {
                "id": str(academic_chapters.id),
                "chapter_name":academic_chapters.chapter_name,
                "subject_id":str(academic_chapters.subject_name.id),
                "subject_name": academic_chapters.subject_name.subject_name,
                "status": academic_chapters.status,
                "created_at": academic_chapters.created_at,
                "updated_at": academic_chapters.updated_at,
            }

        response_data = {
            "result": True,
            "data": academic_chapter_list,
            "message": "Academic subject retrieved successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": print(e)
        }
        return JsonResponse(response_data, status=500)
    


def delete_chapter_data(user,chapter_id):
    try:
        # Check if the academic board exists
        academic_chapter = AcademicChapters.objects.get(id=chapter_id)
        
        # Delete the academic board
        academic_chapter.delete()

        response_data = {
            "result": True,
            "message": "Academic chapter deleted successfully."
        }

        return response_data

    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=404)
    


def update_chapter_data(user,data,chapter_id):
    try:
        # Check if the academic board exists
        academic_chapters = AcademicChapters.objects.get(id=chapter_id)
        try:
            data.subject_name = AcademicSubjects.objects.get(id=data.subject_name)
        except:
            data.standard = academic_chapters.subject_name
        update_data = {field: value for field, value in data.dict().items() if value!= None}

        # Update the board_name and status
        for field, value in update_data.items():
            setattr(academic_chapters, field, value)

        # academic_medium.board_name = academic_board
       
        academic_chapters.save()
      
        updated_chapter = {
            "id": str(academic_chapters.id),
            "chapter_name":academic_chapters.chapter_name,
            "subject_id": str(academic_chapters.subject_name.id),
            "subject_name": academic_chapters.subject_name.subject_name,
            "status": academic_chapters.status,
            "created_at": academic_chapters.created_at,
            "updated_at": academic_chapters.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_chapter,
            "message": "Academic chapter updated successfully."
        }

        return response_data

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

from datetime import timedelta
def add_question_data(user,data):
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
        academic_chapter = AcademicChapters.objects.get(id=data.chapter)
        print(academic_chapter)
        # Create the question
        question = AcademicQuestions.objects.create(
            academic_chapter=academic_chapter,
            question=data.question,
            options=options_instance,  # Pass the instance of Options
            answer=data.answer,
            question_category=data.question_category,
            marks=data.marks,
            time_duration=str(time_duration),
            business_owner=user
        )

        question_data = {
            "id": str(question.id),
            "question": question.question,
            "answer": question.answer,
            "options": options_data,  # Return the options data as-is
            "chapter_id": str(question.academic_chapter.id),
            "chapter_name": question.academic_chapter.chapter_name,
            "subject_id": str(question.academic_chapter.subject_name.id),
            "subject_name": question.academic_chapter.subject_name.subject_name,
            "question_category": question.question_category,
            "marks": question.marks,
            "time": question.time_duration,
            "status": question.status,
            "created_at":question.created_at,
            "updated_at":question.updated_at
        }

        response_data = {
            "result": True,
            "data": question_data,
            "message":"Question added successfully"
        }
        return response_data

    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
    


def get_academic_question_list(user):
    try:
        questions = AcademicQuestions.objects.filter(business_owner=user)
        question_list = []
        for question in questions:
            try:
                options_data = Options.objects.get(id=question.options_id)
            except Options.DoesNotExist:
                options_data = None  # Handle the case where options are not found
            
            options_dict = {
                "option1": options_data.option1 if options_data else None,
                "option2": options_data.option2 if options_data else None,
                "option3": options_data.option3 if options_data else None,
                "option4": options_data.option4 if options_data else None,
            }
            question_data = {
                    "id": str(question.id),
                    "question": question.question,
                    "answer": question.answer,
                    "options": options_dict,  # Return the options data as-is
                    "chapter_id": str(question.academic_chapter.id),
                    "chapter_name": question.academic_chapter.chapter_name,
                    "subject_id": str(question.academic_chapter.subject_name.id),
                    "subject_name": question.academic_chapter.subject_name.subject_name, 
                    "question_category": question.question_category,
                    "marks": question.marks,
                    "time": str(question.time_duration),
                    "status": question.status,
                    "created_at":question.created_at,
                    "updated_at":question.updated_at
                }
            question_list.append(question_data)
            
        response_data = {
            "result": True,
            "data": question_list,
            "message":"Questions retrived successfully"
        }
        return response_data

    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
    


def get_academic_question_data(question_id):
    try:
        question = AcademicQuestions.objects.get(id=question_id)
        options_data = Options.objects.get(id=question.options_id)
        options_dict = {
                "option1": options_data.option1 if options_data else None,
                "option2": options_data.option2 if options_data else None,
                "option3": options_data.option3 if options_data else None,
                "option4": options_data.option4 if options_data else None,
            }
        
        question_data = {
                "id": str(question.id),
                "question": question.question,
                "answer": question.answer,
                "options": options_dict,  # Return the options data as-is
                "chapter_id": str(question.academic_chapter.id),
                "chapter_name": question.academic_chapter.chapter_name,
                "subject_id": str(question.academic_chapter.subject_name.id),
                "subject_name": question.academic_chapter.subject_name.subject_name, 
                "question_category": question.question_category,
                "marks": question.marks,
                "time": str(question.time_duration),
                "status": question.status,
                "created_at":question.created_at,
                "updated_at":question.updated_at
            }
         
            
        response_data = {
            "result": True,
            "data": question_data,
            "message":"Questions retrived successfully"
        }
        return response_data

    except Exception as e:
        response_data = {
                    "result": False,
                    "message": str(e)
                }
        return JsonResponse(response_data, status=400)
    


def delete_question_data(user, question_id):
    try:
        # Check if the academic question exists
        academic_question = AcademicQuestions.objects.get(id=question_id)
        
        # Get the options associated with the question
        options_data = Options.objects.filter(id=academic_question.options_id)
        
        # Delete the academic question
        academic_question.delete()
        
        # Delete the associated options
        options_data.delete()

        response_data = {
            "result": True,
            "message": "Academic question and associated options deleted successfully."
        }

        return response_data

    except AcademicQuestions.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Academic question not found."
        }
        return JsonResponse(response_data, status=404)
    
    except Options.DoesNotExist:
        # Handle the case where options are not found
        response_data = {
            "result": False,
            "message": "Options not found."
        }
        return JsonResponse(response_data, status=404)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data, status=500)
    




def parse_time_duration(time_str):
    try:
        time_parts = time_str.split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        return timedelta(hours=hours, minutes=minutes)
    except ValueError:
        raise HttpError(400, "Invalid time duration format")


def update_question_data(data, question_id):
    try:
        question = AcademicQuestions.objects.get(id=question_id)
        options = None  # Initialize options variable

        # Update question fields if data is provided
        if data.question is not None:
            question.question = data.question
        if data.answer is not None:
            question.answer = data.answer
        if data.question_category is not None:
            question.question_category = data.question_category
        if data.marks is not None:
            question.marks = data.marks
        if data.time is not None:
            question.time_duration = str(parse_time_duration(data.time))
        
        question.save()

        # Update options if data is provided
        if data.options is not None:
            options = Options.objects.get(id=question.options_id)
            if data.options.option1 is not None:
                options.option1 = data.options.option1
            if data.options.option2 is not None:
                options.option2 = data.options.option2
            if data.options.option3 is not None:
                options.option3 = data.options.option3
            if data.options.option4 is not None:
                options.option4 = data.options.option4
            options.save()

        # Construct response options_dict based on updated or existing options
        if options:
            options_dict = {
                "option1": options.option1,
                "option2": options.option2,
                "option3": options.option3,
                "option4": options.option4,
            }
        else:
            options_dict = {
                "option1": question.options.option1,
                "option2": question.options.option2,
                "option3": question.options.option3,
                "option4": question.options.option4,
            }

        question_data = {
            "id": str(question.id),
            "question": question.question,
            "answer": question.answer,
            "options": options_dict,
            "chapter_id": str(question.academic_chapter.id),
            "chapter_name": question.academic_chapter.chapter_name,
            "subject_id": str(question.academic_chapter.subject_name.id),
            "subject_name": question.academic_chapter.subject_name.subject_name,
            "question_category": question.question_category,
            "marks": question.marks,
            "time": str(question.time_duration),
            "status": question.status,
            "created_at": question.created_at,
            "updated_at": question.updated_at
        }

        response_data = {
            "result": True,
            "data": question_data,
            "message": "Question updated successfully"
        }
        return response_data

    except AcademicQuestions.DoesNotExist:
        raise HttpError(404, "Question not found")

    except Options.DoesNotExist:
        raise HttpError(404, "Options not found")

    except Exception as e:
        raise HttpError(500, str(e))