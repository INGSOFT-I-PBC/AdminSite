from django.db import models


class Status(models.Model):
    """
    This model represent the status for some process that is used inside the system,
    this model is a generalization of all the statuses that are available to use into
    every model that needs it.

    Args:
        models (Model): Django's Model

    Attributes:
        id (AutoField):
            Identifier of the model

        name (CharField):
            Name of the Status (ex: Unknown, Available, Unavailable).

        description (CharField):
            The description of the status, only for help or verbosity.

        created_at (DateTimeField):
            This is a registry that saves when an `instance` of the model.

        created_by (Employee):
            This field represent the creator of the `instance`. Used for traceability.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = "status"
        indexes = [models.Index(fields=["name"])]


class TimestampModel(models.Model):
    """TimestampModel

    This abstract model hold the data from a model that holds the log when the
    'state' change.

    Attributes:
        created_at (DateTimeField):
            This field save the moment in which the `instance` is created on the
            database.

        updated_at (DateTimeField):
            This field save the moment in which the `instance` has a modification on
            any of its records.

        deleted_at (DateTimeField):
            This fields save the moment in which an `instance` is soft-delete from
            the database.
    """

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=[
                    "created_at",
                ],
                name="idx_filter_create_date",
            ),
            models.Index(
                fields=[
                    "updated_at",
                ],
                name="idx_filter_update_date",
            ),
        ]


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
        null=True,
        default=None,
        on_delete=models.RESTRICT,
        related_name="remover",
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=[
                    "created_by",
                ],
                name="idx_filter_create_actor",
            ),
            models.Index(
                fields=[
                    "updated_by",
                ],
                name="idx_filter_update_actor",
            ),
        ]
