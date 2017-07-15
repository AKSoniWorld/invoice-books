from __future__ import unicode_literals

from django.db import models

from applications.accounts import models as accounts_models
from libs import models as libs_models


class Company(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores companies and their info.
    """
    name = models.CharField(max_length=255, help_text='Name of the company.')
    description = models.TextField(help_text='Description of the company.')
    address_line_1 = models.CharField(max_length=512, help_text='Address line 1 of the company.')
    address_line_2 = models.CharField(max_length=512, help_text='Address line 2 of the company.')
    state = models.CharField(max_length=12, help_text='State of the company.')
    phone = models.CharField(max_length=12, help_text='Contact number of the company.')
    gstin = models.CharField(unique=True, max_length=30, help_text='GSTIN of the company.')
    tin = models.CharField(max_length=30, blank=True, help_text='TIN of the company.')
    cin = models.CharField(max_length=30, blank=True, help_text='CIN of the company.')
    bank_account = models.CharField(max_length=60, blank=True, help_text='Details of bank account of the company.')
    invoice_terms_conditions = models.TextField(blank=True, help_text='Terms and Conditions that the company abide by.')
    logo_1 = models.ImageField(help_text='Primary logo of the company.')
    logo_2 = models.ImageField(null=True, blank=True, help_text='Secondary logo of the company.')

    def __unicode__(self):
        return '{} - {}'.format(self.name, self.gstin) if self.active else 'INACTIVE'


class UserCompany(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores relationship b/w users and companies.
    """
    user = models.ForeignKey(accounts_models.User, related_name='companies')
    company = models.ForeignKey(Company, related_name='users')

    class Meta:
        unique_together = ('user', 'company')

    def __unicode__(self):
        return '{} - ({})'.format(self.user, self.company) if self.active else 'INACTIVE'
