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
    is_admin = models.BooleanField(null=False, default=False)

    USERNAME_FIELD = 'username'
    PASSWORD_FIELD = 'password'

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'({self.username}){{ {self.pk}, {self.name} {self.lastname} }}'


class Permission(models.Model):
    """
    Permission Class
    This class store a user permission for do an action or
    access to somewhere.
    """
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'permissions'


class UserPermission(models.Model):
    """
    UserPermission class

    This class store the permissions that a user has.
    """
    permission_id = models.ForeignKey(Permission, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'user_permissions'
