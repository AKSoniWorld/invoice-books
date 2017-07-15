"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

from applications.accounts import (
    decorators as accounts_decorators,
    forms as accounts_forms
)


urlpatterns = [
    url(r'^login/$',
        accounts_decorators.anonymous_required(login, redirect_url=reverse_lazy('dashboard')),
        {'template_name': 'account/login.html', 'authentication_form': accounts_forms.LoginForm}, name='login'
        ),
    url(r'^logout/$', logout, name='logout', kwargs={'next_page': reverse_lazy('home')})
]
