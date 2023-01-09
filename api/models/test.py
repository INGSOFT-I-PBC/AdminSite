from django.db import models

from api.mixins import AuditMixin, SoftDeleteMixin, TimestampMixin


class TestModel(TimestampMixin, SoftDeleteMixin, AuditMixin, models.Model):

    charfield = models.CharField(max_length=128, null=True, blank=True)
    intfield = models.IntegerField(null=True)
    decimalfield = models.DecimalField(null=True, decimal_places=5, max_digits=65)
    floatfield = models.FloatField(null=True)
    boolfield = models.BooleanField(null=True, default=True)

    class Meta:
        db_table = "api_test_table"


class ChildTest(models.Model):
    parent = models.ForeignKey(
        TestModel, related_name="childs", on_delete=models.DO_NOTHING, null=True
    )

    field = models.CharField(
        max_length=128, default="field_value", null=True, blank=True
    )
