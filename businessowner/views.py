from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from businessowner.schemas import *
from .utils import generate_token
from .helpers import *
from .models import *
from .authentication import JWTAuthentication
from ninja import Router
from ninja.errors import HttpError
from .authentication import verify_token
router = Router()



@router.post("/login", response={200: LoginOut, 401: dict})
async def login(request, login_data: LoginIn):
    is_valid, message, user_id = await verify_user_credentials(login_data.email, login_data.password)
    
    if is_valid:
        token = generate_token(user_id)  # Generate the token here
        return create_login_response(login_data, is_valid, message, token)
    else:
        return create_login_response(login_data, is_valid, message)


@router.post("/changePassword", response={200: ChangePasswordOut, 400: dict, 401: dict})
@verify_token
def change_password(request, change_data: ChangePasswordIn):
    
    result,status = perform_change_password(change_data) 
    
    return JsonResponse(result,status=status)


@router.post("/forgotPassword", response={400: dict, 401: dict})
def forgot_password(request):
    pass


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------PLAN PURCHASE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/planPurchase", response={200: dict, 400: dict, 401: dict})
def plan_purchase(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    print(user)
    return get_plan_purchase_response()


@router.get("/purchaseHistory", response={200: dict, 400: dict, 401: dict})
def purchase_history(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return get_purchase_history_response(user)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------OWNER PROFILE-------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/ownerProfile", response={200: dict})
def get_business_owner(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)

    return create_owner_response(user, True, "Owner retrieved successfully")


@router.patch("/ownerProfile", response={200: dict})
def update_business_owner(request, data: BusinessOwnerIn):

    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    return update_owner_data(user, data)
    
    

#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------COMPETITIVE BATCH-----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/batch", response={200: dict})
def add_competitive_batch(request, data: BatchIn):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    return add_batch(data, user)


@router.get("/competitive/batch",  response={200: dict, 400: dict, 401: dict})
def get_competitive_batch(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    return get_batches_response(user)


@router.put("/competitive/batch/{batch_id}",  response={200: dict, 400: dict, 401: dict})
def update_competitive_batch(request, batch_id, data: BatchUpdate):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    return update_batch(batch_id, data)


@router.delete("/competitive/batch/{batch_id}",  response={200: dict, 400: dict, 401: dict})
def delete_competitive_batch(request, batch_id):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    batch = get_object_or_404(CompetitiveBatches, id=batch_id)
    batch.delete()

    return JsonResponse({"status":True,
                         "message":"Data Deleted Successfully"})


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE SUBJECT----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/subject", response={200: dict})
def add_competitive_subject(request, data: SubjectIn):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    return add_comp_sub(data, user)


@router.get("/competitive/subject",  response={200: dict, 400: dict, 401: dict})
def get_competitive_subject(request):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    return get_subjects_response(user)


@router.put("/competitive/subject/{subject_id}",  response={200: dict, 400: dict, 401: dict})
def update_competitive_subject(request, subject_id, data: SubjectUpdate):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    return update_comp_sub(subject_id, data)


@router.delete("/competitive/subject/{subject_id}",  response={200: dict, 400: dict, 401: dict})
def delete_competitive_subject(request, subject_id):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    subject = get_object_or_404(CompetitiveSubjects, id=subject_id)
    subject.delete()

    return JsonResponse({"status":True,
                         "message":"Data Deleted Successfully"})


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------COMPETITIVE CHAPTER----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/competitive/chapter", response={200: str})
def add_competitive_chapter(request, data: ChapterIn):
    user, error_response = authenticate_with_jwt_token(request)
    if error_response:
        return JsonResponse(error_response, status=401)
    
    try:
        try:
            subject_instance = CompetitiveSubjects.objects.get(id=data.subject_name)
        except CompetitiveSubjects.DoesNotExist:
            return JsonResponse({"error": "Subject does not exist"}, status=400)
        
        batches_instances = CompetitiveBatches.objects.filter(id__in=data.batches)
        batches = list(batches_instances)
        
        # Create a new chapter instance
        chapter_instance = CompetitiveChapters(
            subject_name=subject_instance,
            chapter_name=data.chapter_name,
        )

        for batch in batches:
            chapter_instance.batches.add(batch)
        # chapter_instance.batches = list(batches_instances)
        chapter_instance.save()
        return JsonResponse({"message": "Chapter added successfully!"}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)