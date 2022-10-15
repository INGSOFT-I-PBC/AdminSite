from django.http import JsonResponse
from rest_framework import pagination
from rest_framework.response import Response


class ApiPagination(pagination.PageNumberPagination):
    page_size_query_param = "per_page"

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


err_codes = {404: "ERR_NOT_FOUND", 400: "ERR_BAD_REQUEST", 403: "ERR_UNAUTHORIZED"}


def error_response(err: str, code: str = None, status: int = 400):
    errres = {"error": True, "message": err}
    if code is not None:
        errres["code"] = code
    else:
        code = err_codes.get(status)
        if code is not None:
            errres["code"] = code

    return JsonResponse(errres, status=status)


def response(message: str, code: str = "SUCCESS", status: int = 200):
    return JsonResponse(
        {"message": message, "code": code, "error": False}, status=status
    )


def teapot(msg: str = "I'm a teapot"):
    return JsonResponse(
        {"error": None, "message": msg, "code": "IM_A_TEAPOT"}, status=418
    )
