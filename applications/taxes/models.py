from __future__ import unicode_literals

from django.db import models

from libs import models as libs_models


class Tax(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores taxes and their info.
    """
    name = models.CharField(max_length=255, help_text='Name of the Tax.')
    description = models.TextField(help_text='Description of the Tax.')
    percentage = models.DecimalField(decimal_places=2, max_digits=6, help_text='Percentage that should be applied on total amount.')

    def __unicode__(self):
        return '{} - {}%'.format(self.name, self.percentage)
