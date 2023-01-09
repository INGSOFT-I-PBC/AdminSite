from django.db import models

from api.models.users import Employee


class Role(models.Model):
    """
    Role Model:

    This model represents the hierarchy position of the given user
    into the business. This class is only contains organizational
    information doesn't represents anything important onto the
    authentication System.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=64, verbose_name="role name", null=False)
    codename = models.CharField(
        max_length=50, verbose_name="role identifier", default=None
    )
    role_class = models.CharField(
        max_length=128, db_column="class", verbose_name="role class", default=None
    )
    created_at = models.DateTimeField(auto_created=True, auto_now=True, null=False)

    def __str__(self):
        return f"{self.name} <{self.codename}>"

    class Meta:
        db_table = "roles"
        indexes = [models.Index(fields=["name"]), models.Index(fields=["role_class"])]
