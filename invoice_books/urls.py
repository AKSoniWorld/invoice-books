"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url, include
from django.contrib import admin

from invoice_books import views as invoice_books_views

urlpatterns = [
    url(r'^$', invoice_books_views.IndexView.as_view(), name='home'),
    url(r'^account/', include('applications.accounts.urls', namespace='accounts')),
    url(r'^dashboard/$', invoice_books_views.DashboardView.as_view(), name='dashboard'),
    url('^inventory/', include('applications.inventories.urls', namespace='inventories')),
    url('^invoice/', include('applications.invoices.urls', namespace='invoices')),
    url(r'^test/$', invoice_books_views.TestView.as_view(), name='test'),
    url(r'^admin/', admin.site.urls),
]
