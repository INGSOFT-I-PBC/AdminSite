from rest_framework import pagination
from rest_framework.response import Response


class ApiPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "page": self.page.number,
                "lastPage": self.page.paginator.num_pages,
                "total": self.page.paginator.count,
            }
        )


class ParamNotFoundError(Exception):
    pass


class ParamTypeMatchError(TypeError):
    pass


class Validator:
    """
    Builds a new Validator for an HTTP requests.
    """

    def add_field(self, field_name: str, field_type=str):

        pass
