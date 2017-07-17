"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url

from applications.customers import (
    views as customers_views
)


urlpatterns = [
    # url(r'^$', customers_views.customerListView.as_view(), name='customer_list'),
    url(r'^create/$', customers_views.CustomerCreateView.as_view(), name='customer_create'),
    # url(r'^(?P<customer_id>[0-9]+)/update/$', customers_views.customerUpdateView.as_view(), name='customer_update'),
]
