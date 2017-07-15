from django import forms
from django.utils.translation import ugettext_lazy as _

from applications.companies import models as companies_models
from applications.inventories import models as inventories_models


class ItemProcessFormMixin(object):
    """ Form for item create page """

    # def clean_name(self):
    #     return self.cleaned_data.get('name').strip().lower().title()

    def _validate_sku(self, sku, company):
        if inventories_models.Item.all_objects.exclude(
            id=self.instance.id
        ).filter(company=company, sku=sku).exists():
            raise forms.ValidationError(
                _('Item with same SKU [%(sku)s] already exists.'),
                code="invalid_sku", params={'sku': sku}
            )
        return sku


class ItemCreateForm(ItemProcessFormMixin, forms.ModelForm):
    """ Form for item create page """

    company = forms.ModelChoiceField(queryset=companies_models.Company.objects.all(), required=False)

    class Meta:
        model = inventories_models.Item
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
