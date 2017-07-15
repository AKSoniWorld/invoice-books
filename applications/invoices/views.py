from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from applications.invoices import models as invoices_models


class InvoiceListView(LoginRequiredMixin, ListView):

    template_name = 'invoice/list.html'
    model = invoices_models.Invoice
    paginate_by = 20


class InvoiceCreateView(LoginRequiredMixin, CreateView):

    template_name = 'invoice/list.html'
    model = invoices_models.Invoice
    paginate_by = 20
