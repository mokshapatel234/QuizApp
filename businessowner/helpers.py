from .models import *
from .schemas import *
from django.http import JsonResponse
from .authentication import JWTAuthentication 
from asgiref.sync import sync_to_async
from ninja import UploadedFile, File
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from ninja.errors import HttpError


def authenticate_with_jwt_token(request):
    jwt_token = request.headers.get('Authorization', None)
    
    if not jwt_token:
        return None, {"result":False, "message": "Authorization token is required"}
    
    jwt_auth = JWTAuthentication()
    user, jwt_token = jwt_auth.authenticate(request)
    
    if not user:
        return None, {"result":False,"message": "Unauthorized"}
    
    return user, None


@sync_to_async
def verify_user_credentials(email, password):
    try:
        user = BusinessOwners.objects.get(email=email)
        if user.password == password:
            return True, "Login successful", str(user.id)
        else:
            return False, "Invalid password", None
    except BusinessOwners.DoesNotExist:
        return False, "Invalid email", None

def create_login_response(login_data, is_valid, message, token=None):
    if is_valid:
        response_data = {
            "result": is_valid,
            "data": login_data.dict(),
            "token": token,
            "message": message,
    
        }
        response_status = 200
    else:
        response_data = {
            "result": is_valid,
            "message": message
        }
        response_status = 401
    
    return JsonResponse(response_data, status=response_status)


def perform_change_password(change_data):
    try:
        user = BusinessOwners.objects.get(email=change_data.email)
    

        if change_data.old_password != user.password:
            return {"result": False, "message": "Invalid old password"},400

        if change_data.new_password != change_data.confirm_password:
            return {"result": False, "message": "New password and confirm password do not match"},400

        user.password = change_data.new_password
        user.save()

        return {"result": True, "message": "Password changed successfully"},200
    
    except BusinessOwners.DoesNotExist:
        return {"result": False, "message": "Business owner not found"},400
    

# def generate_change_password_response(result):
#     if "result" in result and result["result"]:
#         response_data = {
#             "result": True,
#             "message": "Password changed successfully"
#         }
        
#     else:
#         response_data = {
#             "result": False,
#             "message": result["message"]  # Use the message from the result
#         }
#     return JsonResponse(response_data)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------PLAN PURCHASE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def get_plan_purchase_response():
    try:
        plans = Plans.objects.all()

        plan_schema_list = [PlanSchemaIn(
            plan_name=plan.plan_name,
            description=plan.description,
            price=plan.price,
            validity=plan.validity,
            image=plan.image.url if plan.image else None,
            status=plan.status
        ) for plan in plans]

        response_data = {
            "result": True,
            "data": plan_schema_list,
            "message": "Data found successfully"
        }

        return JsonResponse(response_data)
    
    except Exception as e:
        response_data = {
            "result": True,
            "message": "Something went wrong"
        }
        return JsonResponse(response_data)


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

        return JsonResponse(response_data)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong"
        }
        return JsonResponse(response_data)
    

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
                        "city_id": city.id,
                        "city_name": city.name,
                        "state_id": city.state_id,
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
        
        return JsonResponse(response_data)
    

    except BusinessOwners.DoesNotExist:
        return None


def update_owner_data(user, data):
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
                raise HttpError(400, "No fields to update")
        else:
            raise HttpError(404, "Owner not found")
        

    except BusinessOwners.DoesNotExist:
        return JsonResponse({"error": "Owner not found"}, status=404)
    except Cities.DoesNotExist:
        return JsonResponse({"error": "City not found"}, status=404)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": "An error occurred"}, status=500)


    


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_batch(data, user):
    try:
        batch_name = data.batch_name

        if CompetitiveBatches.objects.filter(batch_name=batch_name, business_owner=user).exists():
            response_data = {
                "result": False,
                "message": "Batch name already exists",
            }
            return JsonResponse(response_data, status=400)

        batch = CompetitiveBatches.objects.create(batch_name=batch_name, business_owner=user)
        business_owner = BusinessOwners.objects.get(id=batch.business_owner_id)
        saved_batch = {
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
            "data": saved_batch,
            "message": "Batch created successfully",
        }
        return JsonResponse(response_data, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_batches_response(user):
    try:
        batches = CompetitiveBatches.objects.filter(business_owner=user, status="active")
        business_owner = BusinessOwners.objects.get(id=user.id)
        batches_list = [
            {
                "id": batch.id,
                "batch_name": batch.batch_name,
                "business_owner_id": batch.business_owner_id,
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
            "message": "Purchase history retrieved successfully"
        }

        return JsonResponse(response_data)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data)


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
                    "message": "Batch updated successfully",
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({"result": False, "message": "No fields to update"}, status=400)
        else:
            return JsonResponse({"result": False, "message": "Batch not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, "error": str(e)}, status=500)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE SUBJECT----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


def add_comp_sub(data, user):
    try:
        subject_name = data.subject_name

        if CompetitiveSubjects.objects.filter(subject_name=subject_name, business_owner=user).exists():
            response_data = {
                "result": False,
                "message": "Subject name already exists",
            }
            return JsonResponse(response_data, status=400)
        
        subject = CompetitiveSubjects.objects.create(subject_name=subject_name, business_owner=user)
        business_owner = BusinessOwners.objects.get(id=subject.business_owner_id)
        saved_subject = {
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
            "data": saved_subject,
            "message": "Subject created successfully",
        }
        return JsonResponse(response_data, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_subjects_response(user):
    try:
        subjects = CompetitiveSubjects.objects.select_related('business_owner').filter(
            Q(business_owner=user) & Q(status="active")
        )
        business_owner = BusinessOwners.objects.get(id=user.id)
        subjects_list = [
            {
                "id": subject.id,
                "subject_name": subject.subject_name,
                "business_owner_id": subject.business_owner_id,
                "business_owner_name": business_owner.business_name,
                "status": subject.status,
                "created_at": subject.created_at,
                "updated_at": subject.updated_at,
            }
            for subject in subjects
        ]

        response_data = {
            "result": True,
            "data": subjects_list,
            "message": "Purchase history retrieved successfully"
        }

        return JsonResponse(response_data)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": str(e)
        }
        return JsonResponse(response_data)


def update_comp_sub(subject_id, data):
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
                        "batch_name": subject.subject_name,
                        "business_owner_id": str(subject.business_owner_id),
                        "business_owner_name": business_owner.business_name,
                        "status": subject.status,
                        "created_at": subject.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "updated_at": subject.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    },
                    "message": "Batch updated successfully",
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({"result": False, "message": "No fields to update"}, status=400)
        else:
            return JsonResponse({"result": False, "message": "Batch not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, "error": str(e)}, status=500)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE CHAPTER----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#












































































































































































































































































































































































































































































































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

        return JsonResponse(response_data,status=200)
    
    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong."
        }
        return JsonResponse(response_data,status=200)
    


def add_baord(user, data):
    try:
        # Create a new AcademicBoard instance
        board = AcademicBoards.objects.create(
            board_name=data.board_name,
            business_owner=user,
        )
        
        # Return the saved board data as a response
        saved_board = {
            "id": board.id,
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

        return JsonResponse(response_data, status=201)

    except Exception as e:
        return JsonResponse(print(e), status=500)
    


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
            "id": academic_board.id,
            "board_name": academic_board.board_name,
            "business_owner_name": academic_board.business_owner.business_name,
            "status": academic_board.status,
            "created_at": academic_board.created_at,
            "updated_at": academic_board.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_board,
            "message": "Academic board updated successfully."
        }

        return JsonResponse(response_data, status=200)

    except AcademicBoards.DoesNotExist:
        return JsonResponse({"error": "Academic board not found."}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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

        return JsonResponse(response_data, status=200)

    except AcademicBoards.DoesNotExist:
        response_data = {
            "result": False,
            "message": "Academic board not found."
        }
        return JsonResponse(response_data, status=404)
    
    except Exception as e:
        response_data = {
            "error": str(e)
        }
        return JsonResponse(response_data, status=500)
    

def get_academic_mediums():
    try:
        academic_mediums = AcademicMediums.objects.all()

        academic_medium_list = [
            {
                "id": medium.id,
                "medium_name": medium.medium_name,
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

        return JsonResponse(response_data, status=200)

    except Exception as e:
        response_data = {
            "result": False,
            "message": "Something went wrong."
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
            "id": medium.id,
            "medium_name": medium.medium_name,
            "board_name": medium.board_name.board_name,
            "business_owner": user.business_name,
            "status": medium.status,
            "created_at": medium.created_at,
            "updated_at": medium.updated_at,
        }

        response_data = {
            "result": True,
            "data": saved_medium,
            "message": "Medium added successfully."
        }

        return JsonResponse(response_data, status=201)

    except Exception as e:
        error_response = {
            "result": False,
            "error": str(e),
            "message": "An error occurred while adding the medium."
        }
        return JsonResponse(error_response, status=500, safe=False)



def update_medium_data(user,data,medium_id):
    try:
        # Check if the academic board exists
        academic_medium = AcademicMediums.objects.get(id=medium_id)
        board_id=data.board_name

        academic_board = AcademicBoards.objects.get(id=board_id)
       
        update_data = {field: value for field, value in data.dict().items() if field != "board_name" and value is not None}
        
        # Update the board_name and status
        for field, value in update_data.items():
            setattr(academic_medium, field, value)

        academic_medium.board_name = academic_board
        
        academic_medium.save()

        updated_board = {
            "id": academic_medium.id,
            "medium_name":academic_medium.medium_name,
            "board_name": academic_medium.board_name.board_name,
            # "business_owner_name": academic_medium.business_owner.business_name,
            "status": academic_medium.status,
            "created_at": academic_medium.created_at,
            "updated_at": academic_medium.updated_at,
        }

        response_data = {
            "result": True,
            "data": updated_board,
            "message": "Academic board updated successfully."
        }

        return JsonResponse(response_data, status=200)

    except AcademicBoards.DoesNotExist:
        return JsonResponse({"error": "Academic medium not found."}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)