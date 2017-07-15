from django import forms
from django.utils.translation import ugettext_lazy as _

from applications.inventories import models as inventories_models


class ItemCreationForm(forms.ModelForm):
    """ Form for item creation page """

    class Meta:
        model = inventories_models.Item
        exclude = ("company", "active", "created_at", "updated_at")

    # def clean_name(self):
    #     return self.cleaned_data.get('name').strip().lower()


class ItemUpdateForm(forms.ModelForm):
    """ Form for item update page """

    class Meta:
        model = inventories_models.Item
        exclude = ("company", "active", "created_at", "updated_at")

    # def clean_name(self):
    #     return self.cleaned_data.get('name').strip().lower().title()

    def clean_sku(self):
        company = self.initial['company']
        sku = self.cleaned_data['sku']
        if inventories_models.Item.all_objects.exclude(
            id=self.instance.id
        ).filter(company=company, sku=sku).exists():
            raise forms.ValidationError(
                _('Item with same SKU [%(sku)s] already exists.'),
                code="invalid_sku", params={'sku': sku}
            )
        return self.cleaned_data
