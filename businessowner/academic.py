# from .views import router
from .helpers import *
from uuid import UUID 
from django.http import JsonResponse
from ninja import Router,Query
from .authentication import verify_token
from typing import List
router = Router()

@router.get("/academic/board", response={200:AcademicBoardListOut,401:dict, 400:dict})
@verify_token
def get_academic_boards(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_boards_list(request.user,filter_prompt)
    return result

@router.post("/academic/board", response={200: AcademicBoardOut, 401: dict, 400:dict})
@verify_token
def add_boards(request,data: BoardSchema):
    result = add_baord(request.user,data)
    return result

@router.get("/academic/board/{board_id}", response={200:AcademicBoardOut, 401:dict, 400:dict})
@verify_token
def get_academic_board(request,board_id):
    result = get_academic_board_data(request.user,board_id)
    return result


@router.patch("/academic/board/{board_id}", response={200: BoardUpdateSchemaOut, 401: dict, 400:dict})
@verify_token
def update_board(request, board_id: UUID, data: BoardUpdateSchema):
    result = update_board_data(request.user,data,board_id)
    return result
    

@router.delete("/academic/board/{board_id}",response={200: DeleteOut, 401: dict, 400:dict})
@verify_token
def delete_board(request, board_id):    
    result = delete_board_data(request.user,board_id)
    return result




@router.get("/academic/medium", response={200:AcademicMediumListOut, 401:dict})
@verify_token
def get_academic_medium_list(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_mediums_list(filter_prompt)
    return result

@router.get("/academic/medium/{medium_id}", response={200:AddAcademicMediumOut, 401:dict})
@verify_token
def get_academic_medium(request,medium_id):
    result = get_academic_medium_data(request.user,medium_id)
    return result

@router.post("/academic/medium", response={200: AddAcademicMediumOut, 401: dict})
@verify_token
def add_medium(request,data: AddAcademicMediumIn):
    result = add_medium_data(request.user, data.dict())  
    return result


@router.patch("/academic/medium/{medium_id}", response={200: UpdateAcademicMediumOut, 401: dict})
@verify_token
def update_medium(request, medium_id: UUID, data: updateMediumIn):
    result = update_medium_data(request.user,data,medium_id)
    return result


@router.delete("/academic/medium/{medium_id}",response={200: DeleteOut, 401: dict, 400:dict})
@verify_token
def delete_medium(request, medium_id):    
    result = delete_medium_data(request.user,medium_id)
    return result





@router.get("/academic/standard", response={200:AcademicStandardList, 401:dict, 400:dict})
@verify_token
def get_academic_standards(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_standard_list(filter_prompt)
    return result

@router.get("/academic/standard/{standard_id}", response={200:AcademicStandardOut, 401:dict,400:dict})
@verify_token
def get_academic_standard(request,standard_id):
    result = get_academic_standard_data(standard_id)
    return result

@router.post("/academic/standard", response={200: AcademicStandardOut, 401: dict,400:dict})
@verify_token
def add_standard(request,data: AcademicStandardIn):
    result = add_standard_data(request.user, data)  
    return result

@router.patch("/academic/standard/{standard_id}", response={200: AcademicStandardOut, 401: dict})
@verify_token
def update_standard(request, standard_id: UUID, data: updateStandardIn):
    result = update_standard_data(request.user,data,standard_id)
    return result

@router.delete("/academic/standard/{standard_id}",response={200: DeleteOut, 401: dict, 400:dict})
@verify_token
def delete_standard(request, standard_id):    
    result = delete_standard_data(request.user,standard_id)
    return result




@router.get("/academic/subject", response={200:AcademicSubjectList, 401:dict, 400:dict})
@verify_token
def get_academic_subjects(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_subject_list(filter_prompt)
    return result


@router.post("/academic/subject", response={200: AcademicSubjectOut, 401: dict,400:dict})
@verify_token
def add_subject(request,data: AcademicSubjectIn):
    result = add_subject_data(request.user, data)  
    return result


@router.get("/academic/subject/{subject_id}", response={200:AcademicSubjectOut, 401:dict,400:dict})
@verify_token
def get_academic_subject(request,subject_id):
    result = get_academic_subject_data(subject_id)
    return result


@router.delete("/academic/subject/{subject_id}",response={200: DeleteOut, 401: dict, 400:dict})
@verify_token
def delete_subject(request, subject_id):    
    result = delete_subject_data(request.user,subject_id)
    return result


@router.patch("/academic/subject/{subject_id}", response={200: AcademicSubjectOut, 401: dict})
@verify_token
def update_subject(request, subject_id: UUID, data: updateSubjectIn):
    result = update_subject_data(request.user,data,subject_id)
    return result





@router.get("/academic/chapter", response={200:AcademicChapterList, 401:dict, 400:dict})
@verify_token
def get_academic_chapter(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_chapter_list(filter_prompt)
    return result

@router.post("/academic/chapter", response={200: AcademicChapterOut, 401: dict,400:dict})
@verify_token
def add_chapter(request,data: AcademicChapterIn):
    result = add_chapter_data(request.user, data)  
    return result


@router.get("/academic/chapter/{chapter_id}", response={200:AcademicChapterOut, 401:dict,400:dict})
@verify_token
def get_academic_chapter(request,chapter_id):
    result = get_academic_chapter_data(chapter_id)
    return result

@router.delete("/academic/chapter/{chapter_id}",response={200: DeleteOut, 401: dict, 400:dict})
@verify_token
def delete_chapter(request, chapter_id):    
    result = delete_chapter_data(request.user,chapter_id)
    return result

@router.patch("/academic/chapter/{chapter_id}", response={200: AcademicChapterOut, 401: dict})
@verify_token
def update_chapter(request, chapter_id: UUID, data: updateChaptertIn):
    result = update_chapter_data(request.user,data,chapter_id)
    return result






@router.post("/academic/question", response={200: QuestionOut, 401: dict,400:dict})
@verify_token
def add_question(request,data: QuestionIn):
    result = add_question_data(request.user, data)  
    return result


@router.get("/academic/question", response={200:QuestionListOut, 401:dict, 400:dict})
@verify_token
def get_academic_question(request):
    result = get_academic_question_list(request.user)
    return result


@router.get("/academic/question/{question_id}", response={200:QuestionOut, 401:dict,400:dict})
@verify_token
def get_academic_chapter(request,question_id):
    result = get_academic_question_data(question_id)
    return result


@router.delete("/academic/question/{question_id}",response={200: DeleteOut, 401: dict, 400:dict})
@verify_token
def delete_question(request, question_id):    
    result = delete_question_data(request.user,question_id)
    return result


@router.patch("/academic/question/{question_id}", response={200: QuestionOut, 401: dict})
@verify_token
def update_question(request, question_id: UUID, data: UpdateQuestionIn):
    result = update_question_data(data,question_id)
    return result



@router.post("/academic/exam", response={200: List[AcademicExam], 401: dict,400:dict})
@verify_token
def add_exam(request,data: AcademicExamIn):
    result = create_academic_exam(request.user, data)  
    return result


