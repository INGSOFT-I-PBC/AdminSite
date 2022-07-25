from pyexpat import model
from django.db import models

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
    """ TraceableModel

    This models contains the registry of the user that change its
    state.
    """
    created_by = models.ForeignKey('User', db_column='created_by', null=True, on_delete=models.RESTRICT)
    updated_by = models.ForeignKey('User', db_column='updated_by', null=True, default=None, on_delete=models.RESTRICT)
    deleted_by = models.ForeignKey('User', db_column='created_by', null=False, default=None, on_delete=models.RESTRICT)
