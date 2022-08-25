from django.db import models


class StatusModel(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.ForeignKey("Employee", on_delete=models.RESTRICT)

    class Meta:
        db_table = "status"


class TimestampModel(models.Model):
    """TimestampModel

    This abstract model hold the data from a model that holds
    the log when the 'state' change.
    """

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True


class TraceableModel(models.Model):
    """TraceableModel

    This models contains the registry of the user that change its
    state.
    """

    created_by = models.ForeignKey(
        "Employee",
        db_column="created_by",
        null=True,
        on_delete=models.RESTRICT,
        related_name="creator",
    )
    updated_by = models.ForeignKey(
        "Employee",
        db_column="updated_by",
        null=True,
        default=None,
        on_delete=models.RESTRICT,
        related_name="updater",
    )
    deleted_by = models.ForeignKey(
        "Employee",
        db_column="deleted_by",
        null=False,
        default=None,
        on_delete=models.RESTRICT,
        related_name="remover",
    )

    class Meta:
        abstract = True
