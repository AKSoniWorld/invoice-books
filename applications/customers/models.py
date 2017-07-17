from __future__ import unicode_literals

from django.db import models
from libs import models as libs_models


class Customer(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores customers and their info.
    """
    name = models.CharField(max_length=255, help_text='Name of the customer.')
    address_line_1 = models.CharField(max_length=512, help_text='Address line 1 of the customer.')
    address_line_2 = models.CharField(max_length=512, blank=True, help_text='Address line 2 of the customer.')
    state = models.CharField(max_length=12, help_text='State of the customer.')
    phone = models.CharField(max_length=12, help_text='Contact number of the customer.')
    consumer_number = models.CharField(max_length=30, blank=True, help_text='Consumer number of the customer in the company.')

    def __unicode__(self):
        return '{} - {}'.format(self.name, self.consumer_number) if self.active else 'INACTIVE'


class CustomerExtraInfo(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores customers dynamically provided extra info.
    """
    customer = models.ForeignKey(Customer, related_name='extra_info')
    key = models.CharField(max_length=30, help_text='Key of the extra info.')
    value = models.CharField(max_length=127, help_text='Value of the extra info.')

    class Meta:
        unique_together = ('customer', 'key')

    def __unicode__(self):
        return '{} - ({} - {})'.format(self.customer, self.key, self.value) if self.active else 'INACTIVE'
