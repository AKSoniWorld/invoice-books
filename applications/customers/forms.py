from django import forms

from applications.customers import models as customers_models


class CustomerCreateForm(forms.ModelForm):
    """ Form for creating a customer """

    class Meta:
        model = customers_models.Customer
        fields = ('name', 'address_line_1', 'address_line_2', 'state', 'phone', 'consumer_number')
