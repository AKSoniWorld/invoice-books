import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from applications.companies import models as companies_models
from applications.inventories import models as inventories_models
from applications.invoices import models as invoices_models


class InvoiceItemCreateForm(forms.ModelForm):
    """ Form for creating invoice item """

    company = forms.ModelChoiceField(queryset=companies_models.Company.objects.all(), required=False)

    class Meta:
        model = inventories_models.Item
        exclude = ("active", "created_at", "updated_at")

    def clean_company(self):
        return self.initial['company']

    def clean_sku(self):
        return self._validate_sku(self.cleaned_data['sku'], self.initial['company'])



class InvoiceCreateForm(forms.ModelForm):
    """ Form for creating invoice """

    company = forms.ModelChoiceField(queryset=companies_models.Company.objects.all(), required=False)
    customer = forms.ModelChoiceField(queryset=companies_models.Company.objects.all(), required=False)
    date = forms.DateField(required=False)

    class Meta:
        model = invoices_models.Invoice
        exclude = ("is_paid", "pdf", "active", "created_at", "updated_at")

    def clean_company(self):
        return self.initial['company']

    def clean_date(self):
        return datetime.date.today()

    def clean_seq_number(self):
        return invoices_models.Invoice._get_next_seq_number()
