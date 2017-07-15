from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import ListView

from applications.invoices import models as invoices_models


class InvoiceListView(LoginRequiredMixin, ListView):
    """ View to list all items """

    model = invoices_models.Invoice
    template_name = 'invoice/invoice_list.html'
    context_object_name = 'invoices_list'
    paginate_by = 20
    queryset = model.objects.annotate(
        discount=Sum('items__discount'), tax=Sum('items__taxes__amount'), amount=Sum('items__total_amount')
    )
