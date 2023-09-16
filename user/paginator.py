from ninja import Schema
from ninja.pagination import PaginationBase
from typing import List, Any
from .schemas import *

class PaginatorSchema(Schema):
        page: int
        total_docs: int
        total_pages: int  # Add total_pages field
        per_page: int

class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: Optional[int] = 0
        per_page: Optional[int] 
        page: Optional[int] =1

    class Output(Schema):
        result: bool
        data: List[Any]
        pagination: PaginatorSchema
        message: str

    items_attribute = "data"
    
    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        page = pagination.page

        # If per_page is not provided, return the full queryset without pagination
        if per_page is None:
            queryset_list = list(queryset)
            total_docs = len(queryset_list)
            return {
                'result': True,
                'data': queryset_list,
                'pagination': {
                    'page': 1, 
                    'total_docs': total_docs,
                    'total_pages': 1, 
                    'per_page': total_docs, 
                },
                'message': 'Data retrieved successfully'
            }

        # Continue with pagination logic if per_page is provided
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        queryset_list = list(queryset)
        total_docs = len(queryset_list)
        total_pages = (total_docs + per_page - 1) // per_page

        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

        return {
            'result': True,
            'data': queryset_list[start_index:end_index],
            'pagination': {
                'page': page,
                'total_docs': total_docs,
                'total_pages': total_pages,
                'per_page': per_page, 
            },
            'message': 'Data retrieved successfully'
        }


