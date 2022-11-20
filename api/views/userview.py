from django.contrib.auth.hashers import make_password
from django.db.models import Model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from api.models import Employee, User
from api.serializers.auth import *
from api.utils import error_response, response


class EmployeeView(APIView):
    """
    This class handle the request with a single element of the
    Employee model.
    """

    def get(self, request: Request, *args, **kwargs):
        if not Employee.objects.filter(**kwargs).exists():
            return error_response("the given employee doesn't exists")
        employee = Employee.objects.get(**kwargs)
        return JsonResponse(data=GetEmployeeSerializer(employee).data)

    def put(self, request: Request, *args, **kwargs):
        if not Employee.objects.filter(**kwargs).exists():
            return error_response("The given employee doesn't exists")
        if not request.data:
            return error_response("No data provided")
        employee = Employee.objects.get(**kwargs)
        updated_model = UpdateEmployeeSerializer(employee, data=request.data)
        updated_model.is_valid(raise_exception=True)
        updated_model.save()
        return response("The employee was updated successfully")

    def delete(self, request: Request, *args, **kwargs):
        if not Employee.objects.filter(**kwargs).exists():
            return error_response("The given employee doesn't exists")
        employee = Employee.objects.get(**kwargs)
        employee.delete()
        return response("Employee deleted successfully")


class UserView(APIView):
    """
    This class handle the request with a single element of the
    Employee model.
    """

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
        if kwargs.get("username", None):
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
                    "message": "User activated successfully",
                    "code": "USR_ACT_SUCC",
                }
            )
        # else:  # Create a new user
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.password = make_password(password)
        user = user.save()
        return JsonResponse(PublicUserSerializer(user).data)
    print("Wtf")
    return error_response("No username was provided")


@api_view(["POST"])
def create_employee(request: Request, *args, **kwargs):
    if not request.data:
        return error_response("No data was provided")
    if not request.data:
        return error_response("No data was provided")

    cid = request.data.get("cid", None)
    # Now if cid is provided, check the two cases
    if cid:
        # If employee already exists, then reactivate (if needed or send error)
        if Employee.objects.filter(cid=cid).exists():
            return error_response("Empleado con número de cédula existente")
        # else:  # Create a new employee
        employee = UpdateEmployeeSerializer(data=request.data)
        employee.is_valid(raise_exception=True)
        employee = employee.save()
        return JsonResponse(ShowEmployeeSerializer(employee).data)
    return error_response("No cid was provided")


@api_view(["POST"])
def activate_user(request: Request, *args, **kwargs):
    """
    This endpoint activate a given user from the request
    if, and only if it's inactive, else return an error
    message to the consumer.
    """
    return __activate_entity(User, "user", **kwargs)


@api_view(["POST"])
def activate_employee(request: Request, *args, **kwargs):
    """
    This endpoint activate a given employee from the request
    if, and only if it's inactive, else return an error
    message to the consumer.
    """
    return __activate_entity(Employee, "employee", **kwargs)


@api_view(["POST"])
def inactivate_employee(request: Request, *args, **kwargs):
    """
    This endpoint inactivate a given employee from the request
    if, and only if it's active, else return an error
    message to the consumer.
    """
    return __inactivate_entity(Employee, "employee", **kwargs)


def __activate_entity(entity_class: Model, entity_name: str, **kwargs):
    """
    This function activate the given model and return a message
    of completion that can be used as response
    """
    entity = entity_class.objects.filter(**kwargs)
    if not entity.exists():
        return error_response(f"The given {entity_name} doesn't exists")
    target = entity.first()
    if target.is_active:
        return error_response(f"The given {entity_name} is already active")
    target.is_active = True
    target.save()
    return response(f"The {entity_name} was successfully re-activated")


def __inactivate_entity(entity_class: Model, entity_name: str, **kwargs):
    """
    This function inactivate the given model and return a message
    of completion that can be used as response
    """
    entity = entity_class.objects.filter(**kwargs)
    if not entity.exists():
        return error_response(f"The given {entity_name} doesn't exists")
    target = entity.first()
    if not target.is_active:
        return error_response(f"The given {entity_name} is already inactive")
    target.is_active = False
    target.save()
    return response(f"The {entity_name} was successfully inactivated")
