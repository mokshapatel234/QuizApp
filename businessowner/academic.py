# from .views import router
from .helpers import *
from uuid import UUID 
from django.http import JsonResponse
from ninja import Router,Query
from .authentication import verify_token
from typing import List
from.paginator import CustomPagination
from ninja.pagination import paginate, PaginationBase
from ninja.files import UploadedFile
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse
router = Router()


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------BOARD----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/academic/board", response={200:BoardsListResponse,401:dict, 400:dict})
@verify_token
def get_academic_boards(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_boards_list(request,filter_prompt)
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

@router.post("/import-data", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def upload_file(request, xl_file: UploadedFile = File(...),flag: str = Query(...),param_prompt: UploadData = Query(...)):
    if flag not in ["board", "medium","standard","subject","chapter","academic_question","batch","competitive_subject","competitive_chapter","competitive_question"]:
        return JSONResponse(content={"message": "Invalid flag."}, status_code=400)
    return upload_from_xl(xl_file, request.user,flag,param_prompt)


@router.post("/download-data-format", response={200: dict, 400: dict, 401: dict})
@verify_token
def download_file(request,flag: str = Query(...),related_id_name: DownloadData = Query(...)):
    if flag not in ["board", "medium","standard","competitve_subject","academic_subject","subject","chapter","question","batch","competitive_subject","competitive_chapter","competitive_question"]:
        return JSONResponse(content={"message": "Invalid flag."}, status_code=400)
    result = create_excel_with_column_names("output.xlsx",flag,related_id_name)
    return result
#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------MEDIUM----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/academic/medium", response={200:AcademicMediumResponse, 401:dict})
@verify_token
def get_academic_medium_list(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_mediums_list(request, filter_prompt)
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


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------STANDARD--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/academic/standard", response={200:AcademicStandardResponse, 401:dict, 400:dict})
@verify_token
def get_academic_standards(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_standard_list(request, filter_prompt)
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


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------SUBJECT--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/academic/subject", response={200:AcademicSubjectResponse, 401:dict, 400:dict})
@verify_token
def get_academic_subjects(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_subject_list(request, filter_prompt)
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


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------CHAPTER--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.get("/academic/chapter", response={200:AcademicChapterResponse, 401:dict, 400:dict})
@verify_token
def get_academic_chapter(request,filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_chapter_list(request, filter_prompt)
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


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------QUESTION--------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/academic/question", response={200: QuestionOut, 401: dict,400:dict})
@verify_token
def add_question(request,data: QuestionIn):
    result = add_question_data(request.user, data)  
    return result


@router.get("/academic/question", response={200:dict, 401:dict, 400:dict})
@verify_token
def get_academic_question(request, filter_prompt: AcademicFilter = Query(...)):
    result = get_academic_question_list(request, filter_prompt)
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


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------------EXAM----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#


@router.post("/academic/exam", response={200:dict, 401: dict, 400: dict})
@verify_token
def create_acad_exam(request, data: AcademicExamIn):
    return create_academic_exam(request.user, data)

@router.get("/academic/exam", response={200: AcadExamOutResponse, 400: dict, 401: dict})
@verify_token
def get_academic_examlist(request, query:AcadExamFilter = Query(...)):
    return get_acad_examlist(request, query)


@router.post("/academic/startExam", response={200: DeleteOut, 400: dict, 401: dict})
@verify_token
def start_academic_exam(request,data:AcadExamQuestion):
    return start_acad_exam(data)


@router.post("/academic/CreateExam", response={200: AcadeCreatestartExamOut, 400: dict, 401: dict})
@verify_token
def start_CSExam(request, data:AcadeCreatestartExam):
    return start_acad_CSExam(request.user,data)


@router.get("/result/{exam_id}", response={200:dict, 401:dict,400:dict})
@verify_token
def get_result(request,exam_id):
    result = get_exam_result(request.user,exam_id)
    return result