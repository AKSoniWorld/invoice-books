"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url

from applications.taxes import (
    views as taxes_views
)


urlpatterns = [
    url(r'^$', taxes_views.TaxListView.as_view(), name='tax_list'),
    url(r'^create/$', taxes_views.TaxCreateView.as_view(), name='tax_create'),
    url(r'^(?P<tax_id>[0-9]+)/update/$', taxes_views.TaxUpdateView.as_view(), name='tax_update'),
]
