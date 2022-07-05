from django.db import models


class User(models.Model):
    """
    User class

    This class represents a user into the system and is used to
    authentication and other logging things.
    """
    name = models.CharField(max_length=15, null=False)
    lastname = models.CharField(max_length=25, null=False)
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'users'


class Permission(models.Model):
    """
    Permission Class
    This class store a user permission for do an action or
    access to somewhere.
    """
    name = models.CharField(max_length=25, null=False, unique=True)

    class Meta:
        db_table = 'permissions'


class UserPermission(models.Model):
    """
    UserPermission class

    This class store the permissions that a user has.
    """
    permission_id = models.ForeignKey('Permission', on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey('User', on_delete=models.DO_NOTHING)
