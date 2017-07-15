from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Prefetch
from django.views.generic import ListView, DetailView, CreateView

from applications.inventories import models as inventories_models
from applications.invoices import models as invoices_models

from libs import mixins as libs_mixins


class InvoiceListView(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin, ListView):
    """ View to list all invoices """

    model = invoices_models.Invoice
    template_name = 'invoice/invoice_list.html'
    context_object_name = 'invoices_list'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(company=self.user_company).annotate(
            discount=Sum('items__discount'), tax=Sum('items__taxes__amount'), amount=Sum('items__total_amount')
        )


class InvoiceDetailView(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin, DetailView):
    """ View to see detail of an invoice """

    model = invoices_models.Invoice
    template_name = 'invoice/invoice_detail.html'
    context_object_name = 'invoice'
    pk_url_kwarg = 'invoice_id'

    def get_queryset(self):
        return self.model.objects.filter(company=self.user_company).annotate(
            discount=Sum('items__discount'), tax=Sum('items__taxes__amount'), amount=Sum('items__total_amount')
        ).prefetch_related(Prefetch(
            'items',
            queryset=invoices_models.InvoiceItem.objects.annotate(tax=Sum('taxes__amount')),
        ))


# class InvoiceCreateView(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin, CreateView):
#     """ View to create an invoice """
#
#     model = invoices_models.Invoice
#     template_name = 'invoice/invoice_create.html'
#     form_class = inventories_forms.ItemCreateForm
#     template_name = 'inventory/item_create.html'
#     success_url = reverse_lazy('invoices:item_list')
