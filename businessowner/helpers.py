from .models import BusinessOwners
from django.http import JsonResponse
from asgiref.sync import sync_to_async
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