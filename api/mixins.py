import logging

from django.db import models
from django.db.models import signals
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from api.middleware import RequestMiddleware

logger = logging.getLogger(__name__)

# This file contains helper Mixins that are used on models
# that wants to support the Mixin behavior, in order to implement
# the full mixin we need to ensure the order:
# TimestampMixin, SoftDeleteMixin, AuditMixin and last models.Model
# This last is required to create correctly a Django Model Class
# due the class inheritances


class TimestampMixin(models.Model):
    """
    A mixin that provides timestamps for when a model is created, updated, and deleted.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """SoftDeleteMixin
    This mixin is used to handle a model that can be/support soft-delete(ion)
    is supposed to auto-handle all the proccess to deactivate itself.

    Args:
        models (Model): The model class
    """

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class AuditMixin(models.Model):
    """
    Mixin for models that have created_by and updated_by fields.

    This mixin adds the following fields to the model:
        - created_by: The user who created the object.
        - updated_by: The user who last updated the object.
    """

    created_by = models.ForeignKey(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name=_("Created by"),
        editable=False,
    )
    updated_by = models.ForeignKey(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name=_("Updated by"),
        editable=False,
    )

    deleted_by = models.ForeignKey(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name=_("Deleted by"),
        editable=False,
    )

    class Meta:
        abstract = True


# Signal receivers


@receiver(pre_save)
def pre_save_handler(sender, instance, **kwargs):
    """
    Signal receiver that is called before a model instance is saved.
    This receiver sets the created_by and updated_by fields.
    """
    if isinstance(instance, AuditMixin):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        if not request:
            logger.warning("There was not a request, audit couldn't be set")
            return
        user = request.user
        if instance.pk:
            # Updating an existing object
            instance.updated_by = user.employee
        else:
            # Creating a new object
            instance.created_by = user.employee


@receiver(signals.post_delete, sender=AuditMixin)
def post_delete_audit(sender, instance, **kwargs):
    user = getattr(instance, "request", None) and instance.request.user
    instance.__class__.objects.filter(pk=instance.pk).update(deleted_by=user.employee)


@receiver(pre_save, sender=SoftDeleteMixin)
def pre_save_soft_delete_mixin(sender, instance, **kwargs):
    if instance.is_active is False:
        instance.__class__.objects.filter(pk=instance.pk).update(is_active=False)


@receiver(post_delete, sender=SoftDeleteMixin)
def post_delete_soft_delete_mixin(sender, instance, **kwargs):
    instance.__class__.objects.filter(pk=instance.pk).update(is_active=False)
