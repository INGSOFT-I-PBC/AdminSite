from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from api.models import Employee, User
from api.serializers import PublicUserSerializer, UpdateUserSerializer, UserSerializer
from api.utils import error_response, response, teapot


class EmployeeView(APIView):
    """
    This class handle the request with a single element of the
    Employee model.
    """

    def get(self, request: Request):
        pass

    def put(self, request: Request):
        pass

    def delete(self, request: Request):
        pass


class UserView(APIView):
    """
    This class handle the request with a single element of the
    Employee model.
    """

    # id: int,

    def get(self, request: Request, *args, **kwargs):
        if not User.objects.filter(**kwargs, is_active=True).exists():
            return error_response("The given user was not found", status=404)

        target = User.objects.get(**kwargs, is_active=True)
        serializer = UserSerializer(target)
        return JsonResponse(data=serializer.data)

    def put(self, request: Request, *args, **kwargs):
        if not User.objects.filter(**kwargs, is_active=True).exists():
            return error_response("User not found", code="USR_NOT_FOUND", status=404)
        data = request.data
        if not data:
            return error_response("No data was provided")
        data["username"] = kwargs["username"]  # avoid the overwrite of username
        data.pop("id", None)
        target_user = User.objects.get(**kwargs)
        updated_user = UpdateUserSerializer(target_user, data=data)
        if updated_user.is_valid(raise_exception=True):
            updated_user.save()
            return response("user updated successfully")
        return error_response("Information provided is not valid")

    def delete(self, request: Request, *args, **kwargs):
        """
        Deactivate the given user from the system
        """
        if not User.objects.filter(**kwargs, is_active=True).exists():
            return error_response("The given user was not found", status=404)
        target = User.objects.get(**kwargs, is_active=True)
        target.is_active = False
        target.save()

        return JsonResponse(
            {
                "error": False,
                "message": "The user was deleted successfully",
                "code": "SUCC_USR_DEL",
            }
        )


@api_view(["POST"])
def create_user(request: Request, *args, **kwargs):
    if not request.data:
        return error_response("No data was provided")
    password = request.data.pop("password", None)
    pwd_confirm = request.data.pop("password_confirm", None)
    # security check password
    if not password or not pwd_confirm:
        return error_response("No password or password_confirm field was provided")
    if password != pwd_confirm:
        return error_response("The password and password_confirm doesn't match")

    username = request.data.get("username", None)
    # Now if username is provided, check the two cases
    if username:
        # If user already exists, then reactivate (if needed or send error)
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user_serializer = UserSerializer(user)  # used to overwrite internal data
            validated_data = PublicUserSerializer(data=request.data)
            validated_data.is_valid()
            if user.is_active:
                return error_response("The given user already exists")

            user.save()
            return JsonResponse(
                {
                    "error": False,
                    "message": "User activated succesffuly",
                    "code": "USR_ACT_SUCC",
                }
            )
    else:  # Create a new user
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.password = make_password(password)
        user.save()
        return JsonResponse(PublicUserSerializer(user))
    return error_response("No username was provided")


@api_view(["POST"])
def create_employee(request: Request, *args, **kwargs):
    return teapot()
