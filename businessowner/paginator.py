from ninja import Schema
from ninja.pagination import PaginationBase
from typing import List, Any
from .schemas import *


class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: Optional[int] = 0
        per_page: Optional[int] = 5
        page: Optional[int] = 1

    class Output(Schema):
        result: bool
        data: List[Any]
        page: int
        total_docs: int
        total_pages: int  # Add total_pages field
        per_page: int
        message: str

    items_attribute = "data"
    
    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        page = pagination.page

        queryset_list = list(queryset)  # Convert queryset to a list
        
        total_docs = len(queryset_list)
        total_pages = (total_docs + per_page - 1) // per_page  # Calculate total number of pages

        return {
            'result': True,
            'data': queryset_list[skip: skip + per_page],
            'page':page,
            'total_docs': total_docs,
            'total_pages': total_pages,
            'per_page': per_page,
            'message': 'Data retrieved successfully'
        }
