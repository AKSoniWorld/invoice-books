from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _

from applications.accounts import models as accounts_models


class LoginForm(AuthenticationForm):
    """ Extending AuthenticationForm to add 'remember-me' functionality """

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not accounts_models.User.objects.filter(email=username).exists():
            raise forms.ValidationError(
                _('No user with email-id ["%(username)s"]'),
                code="invalid", params={'username': username}
            )
        return username

    def clean_remember_me(self):
        remember_me = self.cleaned_data.get('remember_me')
        self.request.session.set_expiry(60 * 30 if remember_me else 0)
        return remember_me
