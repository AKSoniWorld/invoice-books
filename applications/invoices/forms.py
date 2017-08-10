import datetime
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
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

    def clean(self):
        item = self.cleaned_data.get('item')
        quantity = self.cleaned_data.get('quantity')
        if item and quantity and quantity > item.quantity:
            raise forms.ValidationError(
                _('Requested quantity %(quantity)s for "%(item)s" is more than available quantity %(item_quantity)s.'),
                code="invalid_quantity",
                params={'item': item.name, 'quantity': quantity, 'item_quantity': item.quantity}
            )
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.amount = self.instance.item.price
        self.instance.tax_applied = self.instance.amount * sum(self.instance.item.taxes.all().values_list('tax__percentage', flat=True)) / 100
        self.instance.total_amount = self.instance.amount - self.instance.discount + self.instance.tax_applied
        invoice_item = super(InvoiceItemCreateForm, self).save(commit)

        def save_m2m():
            for item_tax in self.instance.item.taxes.all():
                invoices_models.InvoiceItemTax.objects.create(
                    invoice_item=invoice_item, tax=item_tax.tax, percentage=item_tax.tax.percentage,
                    amount=item_tax.tax.percentage * self.instance.amount / 100
                )

        if not commit:
            self.save_m2m = save_m2m

        return invoice_item


class BaseInvoiceItemFormSet(BaseInlineFormSet):
    """ formset used for invoice-creation """

    def __init__(self, *args, **kwargs):
        """ overridden to force validation on empty(unchanged) forms in the formset """

        super(BaseInvoiceItemFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        """ Checks that an item is selected only once """

        for form in self.forms:
            if form not in self.deleted_forms:
                if form.errors:
                    return

        items_selected = set()
        for form in self.forms:
            if form not in self.deleted_forms:
                item = form.cleaned_data.get('item')
                if item.id in items_selected:
                    raise forms.ValidationError(
                        _('An item can be added only once in a single invoice. Duplicate item: %(item)s.'),
                        code="invalid_quantity",
                        params={'item': item.name}
                    )
                else:
                    items_selected.add(item.id)

        return self.cleaned_data


InvoiceItemFormSet = inlineformset_factory(
    invoices_models.Invoice, invoices_models.InvoiceItem, form=InvoiceItemCreateForm,
    formset=BaseInvoiceItemFormSet, extra=0, min_num=1, validate_min=2
)
