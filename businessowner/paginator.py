from ninja import Schema
from ninja.pagination import PaginationBase
from typing import List, Any
from .schemas import *


class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: int
        per_page: int 

    class Output(Schema):
        items: List[Any]
        total: int
        per_page: int
        

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page

        queryset_list = list(queryset)  # Convert queryset to a list
        return {
            'items': queryset_list[skip: skip + per_page],
            'total': len(queryset_list),
            'per_page': per_page,
        }
