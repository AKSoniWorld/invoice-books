import datetime
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from applications.companies import models as companies_models
from applications.inventories import models as inventories_models
from applications.invoices import models as invoices_models


class InvoiceCreateForm(forms.ModelForm):
    """ Form for creating invoice """

    company = forms.ModelChoiceField(queryset=companies_models.Company.objects.all(), required=False)
    seq_number = forms.CharField(required=False)

    class Meta:
        model = invoices_models.Invoice
        fields = ('company', 'date', 'seq_number', 'customer', )

    def clean_company(self):
        return self.initial['company']

    def clean_seq_number(self):
        return invoices_models.Invoice._get_next_seq_number()


class InvoiceItemCreateForm(forms.ModelForm):
    """ Form for creating invoice-item """

    class Meta:
        model = invoices_models.InvoiceItem
        fields = ('item', 'quantity', 'discount')


InvoiceItemFormSet = inlineformset_factory(
    invoices_models.Invoice, invoices_models.InvoiceItem, form=InvoiceItemCreateForm, extra=0, min_num=1
)
