from .models import *
from .schemas import *
from django.http import JsonResponse
from .authentication import JWTAuthentication 
from asgiref.sync import sync_to_async


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
            return {"result": False, "message": "Invalid old password"}

        if change_data.new_password != change_data.confirm_password:
            return {"result": False, "message": "New password and confirm password do not match"}

        user.password = change_data.new_password
        user.save()

        return {"result": True, "message": "Password changed successfully"}
    
    except BusinessOwners.DoesNotExist:
        return {"result": False, "message": "Business owner not found"}

def generate_change_password_response(result):
    if "result" in result and result["result"]:
        response = {
            "result": True,
            "message": "Password changed successfully"
        }
    else:
        response = {
            "result": False,
            "message": result["message"]  # Use the message from the result
        }
    return response

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

        return response_data
    
    except Exception as e:
        response_data = {
            "result": True,
            "message": "Something went wrong"
        }
        return response_data


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

        return response_data
    
    except Exception as e:
        response_data = {
            "result": True,
            "message": "Something went wrong"
        }
        return response_data
    

def create_owner_response(user, is_valid, message):
    try:
        owner = BusinessOwners.objects.get(id=user.id)

        if owner:
            city = Cities.objects.get(id=owner.city_id)
            state = States.objects.get(id=city.state_id)
        
            owner_data = BusinessOwnerOut(
                business_name=owner.business_name,
                business_type=owner.business_type,
                first_name=owner.first_name,
                last_name=owner.last_name,
                email=owner.email,
                contact_no=owner.contact_no,
                address=owner.address,
                logo=owner.logo.url if owner.logo else None,
                tuition_tagline=owner.tuition_tagline,
                status=owner.status,
                created_at=owner.created_at,
                city={
                    "city_id": city.id,
                    "city_name": city.name,
                    "state_id": city.state_id,
                    "state_name": state.name,
                },
            )

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
        
        return response_data
    except BusinessOwners.DoesNotExist:
        return None


def update_owner_data(owner, update_data):
    for field, value in update_data.items():
        setattr(owner, field, value)
    owner.save()