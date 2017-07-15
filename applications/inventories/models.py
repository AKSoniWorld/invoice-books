from __future__ import unicode_literals

from django.db import models

from applications.companies import models as companies_models
from libs import models as libs_models


class Item(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores items and their info.
    """
    company = models.ForeignKey(companies_models.Company, help_text='Company to which item belongs')
    sku = models.CharField(max_length=30, help_text='\'Stock Keeping Unit\' code of the item.')
    hsn = models.CharField(max_length=60, blank=True, help_text='\'Harmonized System of Nomenclature\' code of the item.')
    name = models.CharField(max_length=255, help_text='Name of the item.')
    description = models.TextField(help_text='Description of the item.')
    quantity = models.PositiveIntegerField(default=0, help_text='Current stock of the item.')
    tax_notes = models.CharField(max_length=60, blank=True, help_text='Notes about the tax applied on the item.')

    class Meta:
        unique_together = ('company', 'sku')

    def __unicode__(self):
        return '{} - {} - {}'.format(self.company, self.sku, self.quantity) if self.active else 'INACTIVE'
