from django import forms
from django.utils.translation import ugettext_lazy as _

from applications.companies import models as companies_models
from applications.inventories import models as inventories_models
from applications.taxes import models as taxes_models


class BaseItemProcessForm(forms.ModelForm):
    """ Base Form for item create/update page """

    tax_1 = forms.ModelChoiceField(
        label='Primary Tax', help_text='Primary tax to be applied on the item', queryset=taxes_models.Tax.objects.all(), required=False
    )
    tax_2 = forms.ModelChoiceField(
        label='Secondary Tax', help_text='Secondary tax to be applied on the item', queryset=taxes_models.Tax.objects.all(), required=False
    )

    class Meta:
        model = inventories_models.Item
        fields = ('sku', 'hsn', 'name', 'description', 'price', 'quantity', 'tax_1', 'tax_2', 'tax_notes')

    def clean(self):
        cleaned_data = super(BaseItemProcessForm, self).clean()
        tax_1 = cleaned_data.get('tax_1')
        tax_2 = cleaned_data.get('tax_2')
        if tax_1 and tax_2 and tax_1 == tax_2:
            raise forms.ValidationError(
                _('Same tax [%(tax)s] can not be applied twice.'),
                code="invalid_tax", params={'tax': tax_1}
            )
        return cleaned_data

    def _validate_sku(self, sku, company):
        if inventories_models.Item.all_objects.exclude(
            id=self.instance.id
        ).filter(company=company, sku=sku).exists():
            raise forms.ValidationError(
                _('Item with same SKU [%(sku)s] already exists.'),
                code="invalid_sku", params={'sku': sku}
            )
        return sku

    def save(self, *args, **kwargs):
        item = super(BaseItemProcessForm, self).save(*args, **kwargs)
        item.taxes.all().delete()
        tax_1 = self.cleaned_data.get('tax_1')
        tax_2 = self.cleaned_data.get('tax_2')
        if tax_1:
            taxes_models.ItemTax.all_objects.update_or_create(defaults={'active': True}, item=item, tax=tax_1)
        if tax_2:
            taxes_models.ItemTax.all_objects.update_or_create(defaults={'active': True}, item=item, tax=tax_2)
        return item


class ItemCreateForm(BaseItemProcessForm):
    """ Form for item create page """

    company = forms.ModelChoiceField(queryset=companies_models.Company.objects.all(), required=False)

    class Meta(BaseItemProcessForm.Meta):
        fields = BaseItemProcessForm.Meta.fields + ('company',)

    def clean_company(self):
        return self.initial['company']

    def clean_sku(self):
        return self._validate_sku(self.cleaned_data['sku'], self.initial['company'])


class ItemUpdateForm(BaseItemProcessForm):
    """ Form for item update page """

    def clean_sku(self):
        return self._validate_sku(self.cleaned_data['sku'], self.instance.company)
