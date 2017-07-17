from django import forms

from applications.taxes import models as taxes_models


class TaxCreateUpdateForm(forms.ModelForm):
    """ Form for creating/updating a tax """

    class Meta:
        model = taxes_models.Tax
        exclude = ("active", "created_at", "updated_at")
