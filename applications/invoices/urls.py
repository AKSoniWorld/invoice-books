"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url

from applications.invoices import views as invoices_views

urlpatterns = [
    url(r'^$', invoices_views.InvoiceListView.as_view(), name='invoice_list'),
    url(r'^(?P<invoice_id>[0-9]+)/$', invoices_views.InvoiceDetailView.as_view(), name='invoice_detail'),
    url(r'^create/$', invoices_views.InvoiceCreateView.as_view(), name='invoice_create'),
    url(r'^create/(?P<customer_id>[0-9]+)/$', invoices_views.InvoiceCreateView.as_view(), name='invoice_create'),
]
