from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models, transaction
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from libs import models as libs_models


class SoftDeleteBaseUserQuerySet(QuerySet):

    @transaction.atomic
    def delete(self):
        """
        Deletes(soft delete) the records in the current QuerySet.
        """
        # Since we are soft deleting the objects so have to send signals
        for obj in self:
            # Soft Delete all objects one-by-one. .delete() will soft delete all other object referencing this one.
            obj.delete()


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(u'The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, active=True, is_superuser=is_superuser, last_login=datetime.datetime.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class SoftDeleteFilterUserManager(CustomUserManager):
    def get_queryset(self):
        qs = super(SoftDeleteFilterUserManager, self).get_queryset().filter(active=True)
        qs.__class__ = SoftDeleteBaseUserQuerySet
        return qs


class SoftDeleteFilterAdminManager(CustomUserManager):
    def get_queryset(self):
        qs = super(SoftDeleteFilterAdminManager, self).get_queryset()
        qs.__class__ = SoftDeleteBaseUserQuerySet
        return qs


class User(AbstractBaseUser, PermissionsMixin, libs_models.BaseSoftDeleteDatesModel):
    """
    Stores users and their info.
    """

    REQUIRED_FIELDS = ('first_name', 'last_name', 'phone', )

    email = models.EmailField(unique=True, help_text='Email of the user')
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    phone = models.CharField(max_length=10)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into the admin site.')
    )

    USERNAME_FIELD = 'email'

    # select only active users
    objects = SoftDeleteFilterUserManager()
    # select all users, This manage user by auth system to fetch user
    _default_manager = CustomUserManager()
    # select all users, such that we can also remove inactive users from DB
    all_objects = CustomUserManager()
    # select all users. On delete it only soft deletes
    admin_objects = SoftDeleteFilterAdminManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        return self.get_short_name()

    def get_short_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.get_full_name()
