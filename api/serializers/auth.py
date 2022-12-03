from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import Employee, Group, Permission, Role, User
from api.serializers.gender import GenderSerializer
from api.serializers.role import RoleSerializer


class UpdateUserSerializer(serializers.Serializer):
    """
    Serializer class
    ================

    This class show/validate the data that is available to modify externally
    by someone using the API
    """

    username = serializers.CharField(
        max_length=15, allow_blank=False, allow_null=False, required=False
    )
    email = serializers.EmailField(
        max_length=100, allow_blank=False, allow_null=False, required=False
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=False
    )
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=False
    )
    password = serializers.CharField(
        max_length=255, allow_blank=False, allow_null=False, required=False
    )

    def create(self, validated_data):
        if validated_data.get("password", None):
            validated_data["password"] = make_password(validated_data["password"])
        return User(**validated_data)

    def update(self, instance: User, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.group = validated_data.get("group", instance.group)
        instance.employee = validated_data.get("employee", instance.employee)
        password = validated_data.get("password", None)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance


class PublicUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    email = serializers.EmailField(max_length=100)
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        # TODO: Complete the update of the User
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "group", "employee"]


class UpdatableEmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=128, allow_blank=False, allow_null=False, required=False
    )
    lastname = serializers.CharField(
        max_length=128, allow_blank=False, allow_null=False, required=False
    )
    # TODO: add a validator to `cid` field
    cid = serializers.CharField(
        max_length=11, allow_blank=False, allow_null=False, required=False
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=False
    )

    def create(self, validated_data):
        return Employee(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.cid = validated_data.get("cid", instance.cid)
        instance.role = validated_data.get("role", instance.role)
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "lastname", "cid", "role"]


class ShowEmployeeSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    created_by = EmployeeSerializer()
    gender = GenderSerializer()
    address = serializers.CharField(allow_blank=True, allow_null=True, required=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "created_at",
            "created_by",
            "name",
            "lastname",
            "cid",
            "role",
            "phone_number",
            "gender",
            "is_active",
            "address",
        ]


class GetEmployeeSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    created_by = ShowEmployeeSerializer()
    gender = GenderSerializer()
    address = serializers.CharField(allow_blank=True, allow_null=True, required=True)

    class Meta:
        model = Employee
        fields = [
            "name",
            "lastname",
            "cid",
            "is_active",
            "role",
            "phone_number",
            "created_by",
            "gender",
            "address",
        ]


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    address = serializers.CharField(allow_blank=True, allow_null=True, required=True)

    class Meta:
        model = Employee
        fields = [
            "name",
            "lastname",
            "cid",
            "is_active",
            "created_by",
            "role",
            "phone_number",
            "gender",
            "address",
        ]


class PermissionSerializer(serializers.ModelSerializer):
    codename = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=128)

    class Meta:
        model = Permission
        fields = ["codename", "name"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
