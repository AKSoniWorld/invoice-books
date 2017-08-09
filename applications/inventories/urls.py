"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url

from applications.inventories import (
    views as inventories_views
)


urlpatterns = [
    url(r'^$', inventories_views.ItemListView.as_view(), name='item_list'),
    url(r'^create/$', inventories_views.ItemCreateView.as_view(), name='item_create'),
    url(r'^(?P<item_id>[0-9]+)/update/$', inventories_views.ItemUpdateView.as_view(), name='item_update'),
    url(r'^autocomplete/$', inventories_views.ItemAutoCompleteView.as_view(), name='item_autocomplete'),
]
