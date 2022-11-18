from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from api.models.common import TimestampModel as TModel
from api.models.users import Employee


class AuthManager(BaseUserManager):
    """
    Authentication Manager Class
    This class manages the creation of the users that can access to the user.
    """

    def create_user(self, username, email, password, employee: Employee):
        """
        This function create a new user with the given username, email,
        name, lastname and password.
        """
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("A password is needed to create a new user")
        print("the employee inserted is: ", employee)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            employee=employee,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, employee: Employee):
        """
        Create and save a new superuser with the given username, email, name,
        lastname and password
        """
        user = self.model(
            email=email,
            username=username,
            password=make_password(password),
            employee=employee,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Permission(models.Model):
    """Permission

    This class represents a permission that a user have.

    Attributes:
        name (CharField):
            This field holds the human-readable name of the current permission.

        codename (CharField):
            This field holds an system identifier for the permission, may contain
            extra information/flags.
    """

    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    name = models.CharField(null=False, max_length=50)
    codename = models.CharField(null=False, max_length=128)

    class Meta:
        db_table = "permission"
        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            )
        ]

    def __str__(self):
        return f"({self. name}, {self.codename})"


class Group(models.Model):
    """
    This Model represent a group of permission that a User has available/assigned.

    Args:
        models (Model): A Django's Model

    Attributes:
        name(CharField):
            This field represents a human-readable name for the current permission.

        codename(CharField):
            This field represent the system identifier of the `Group` that is used
            for internal logic
    """

    name = models.CharField(max_length=128, null=False)
    codename = models.CharField(max_length=128, null=False)

    class Meta:
        db_table = "group"


class GroupPermission(models.Model):
    """Role Permissions
    This class store the permission given by the user role
    """

    permission = models.ForeignKey("Permission", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)

    class Meta:
        db_table = "group_permission"


class UserPermission(models.Model):
    """
    UserPermission class

    This class store the permissions that a user has.
    """

    permission = models.ForeignKey("Permission", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_permissions"


class User(AbstractBaseUser, TModel):
    """
    User class

    This class represents a user into the system and is used to
    authentication and other logging things.
    """

    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, max_length=100, verbose_name="email address")
    password = models.CharField(max_length=255, null=False)
    group = models.ForeignKey(
        Group, on_delete=models.RESTRICT, null=False, related_name="permission_group"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=False, related_name="employee_info"
    )
    is_active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True, null=False)

    USERNAME_FIELD = "username"
    PASSWORD_FIELD = "password"

    REQUIRED_FIELDS = ["email", "employee"]

    objects = AuthManager()

    def __str__(self):
        return f"('{self.username}' '{self.email}')"

    def has_module_perms(self, app_label):
        """
        This function is not needed, so everyone can access to any module of the
        backend, but each permission would be managed individually
        """
        return True

    def has_perm(self, perm, obj=None):
        """Check if the user has the given permission"""
        permission = perm.split(".")[-1]
        if settings.DEBUG:
            print(
                f">> Requesting permission '{permission}' for user: '{self.username}'"
            )
        if self.is_admin:
            return True
        perms = GroupPermission.objects.filter(group=self.group)
        for perm in perms:
            if perm.permission.codename == permission:
                return True
        return False

    @property
    def is_admin(self):
        try:
            return self.group.name == "sys.admin"
        except Exception:
            return False

    @property
    def is_staff(self):
        """Checks if the user is a staff (Developer Team/Super User)"""
        return self.is_admin

    class Meta:
        db_table = "user"
        indexes = [
            models.Index(
                fields=[
                    "username",
                ],
                name="idx_username_search",
            ),
            models.Index(
                fields=[
                    "email",
                ],
                name="idx_email_find",
            ),
        ]
