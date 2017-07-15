from __future__ import unicode_literals

from django.db import models, transaction
from django.db.models import manager, signals
from django.utils.translation import ugettext_lazy as _


class BaseDatesModel(models.Model):
    """
    Abstract model for basic required dates.
    """

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):

    @transaction.atomic
    def delete(self, *args, **kwargs):
        """
        Soft-deletes the records in the current QuerySet, i.e. marks it as inactive
        """
        for obj in self:
            # Soft Delete all objects one-by-one. .delete() will soft delete all other object referencing this one.
            obj.delete(*args, **kwargs)


class SoftDeleteManager(manager.BaseManager.from_queryset(SoftDeleteQuerySet)):
    """
    Object Manager to handle soft delete models.
    """
    use_for_related_fields = True

    def get_queryset(self):
        """
        Returns a new SoftDeleteQuerySet object.
        """
        return super(SoftDeleteManager, self).get_queryset().filter(active=True)


class BaseSoftDeleteModel(models.Model):
    """
    Abstract model to model tables having soft-deletable objects
    """
    soft_delete_model = True

    active = models.BooleanField(default=True)

    objects = SoftDeleteManager()
    # Default manager, see: https://docs.djangoproject.com/en/1.5/topics/db/managers/#modifying-initial-manager-querysets
    all_objects = models.Manager()
    _base_manager = models.Manager()

    @transaction.atomic
    def delete(self, *args, **kwargs):
        signals.pre_delete.send(sender=self.__class__, instance=self)
        self.active = False
        # Super class .save() otherwise it will call post_delete twice
        super(BaseSoftDeleteModel, self).save()
        # Since we are soft deleting the object so have to send signal
        models.signals.post_delete.send(sender=self.__class__, instance=self)

    def undelete(self):
        self.active = True
        self.save()

    def save(self, *args, **kwargs):
        # Since we are soft deleted(active=False) the object so have to send signal
        if not self.active:
            # Pre Delete listener must be send update_locked_pre_member key
            signals.pre_delete.send(sender=self.__class__, instance=self)
        # Save Model object
        super(BaseSoftDeleteModel, self).save(*args, **kwargs)
        # Since we are soft deleted(active=False) the object so have to send signal
        if not self.active:
            # Post Delete listener must be send update_locked_pre_member key
            models.signals.post_delete.send(sender=self.__class__, instance=self)

    def permanent_delete(self, *args, **kwargs):
        super(BaseSoftDeleteModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class BaseSoftDeleteDatesModel(BaseSoftDeleteModel, BaseDatesModel):
    """
    Base model of BaseSoftDeleteModel and BaseDatesModel
    """
    class Meta:
        abstract = True
