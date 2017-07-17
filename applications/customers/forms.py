from django import forms
from django.utils.translation import ugettext_lazy as _

from applications.companies import models as companies_models
from applications.customers import models as customers_models


class CustomerCreateForm(forms.ModelForm):
    """ Form for creating a customer """


    class Meta:
        model = customers_models.Customer
        exclude = ("active", "created_at", "updated_at")

    def clean_company(self):
        return self.initial['company']

    def clean_sku(self):
        return self._validate_sku(self.cleaned_data['sku'], self.initial['company'])


class ItemUpdateForm(ItemProcessFormMixin, forms.ModelForm):
    """ Form for item update page """

    class Meta:
        model = inventories_models.Item
        exclude = ("company", "active", "created_at", "updated_at")

    def clean_sku(self):
        return self._validate_sku(self.cleaned_data['sku'], self.instance.company)
