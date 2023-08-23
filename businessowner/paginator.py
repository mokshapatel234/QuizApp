from ninja import Schema
from ninja.pagination import PaginationBase
from typing import List, Any
from .schemas import *


class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: int
        per_page: int 

    class Output(Schema):
        items: List[BatchOut]
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        return {
            'items': queryset[skip: skip + per_page],
            'total': queryset.count(),
            'per_page': per_page,
        }