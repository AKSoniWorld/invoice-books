import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum, Prefetch
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView

from applications.invoices import (
    forms as invoices_forms,
    models as invoices_models
)

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
            discount=Sum("items__discount"), tax=Sum('items__tax_applied'), amount=Sum('items__total_amount')
        ).prefetch_related(Prefetch(
            'items',
            queryset=invoices_models.InvoiceItem.objects.annotate(
                tax=Sum('taxes__amount'), tax_percentage=Sum('taxes__percentage')
            ).extra(select={'total_amount_all_units': "quantity * total_amount"})
        ))


class InvoiceCreateView(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin, CreateView):
    """ View to create an invoice """

    model = invoices_models.Invoice
    template_name = 'invoice/invoice_create.html'
    form_class = invoices_forms.InvoiceCreateForm
    success_url = reverse_lazy('invoices:invoice_list')

    def get_initial(self, *args, **kwargs):
        initial_data = super(InvoiceCreateView, self).get_initial(*args, **kwargs)
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            initial_data.update({'customer': int(customer_id)})
        initial_data.update({
            'company': self.user_company,
            'date': datetime.date.today().strftime('%Y-%m-%d')
        })
        return initial_data

    def get_context_data(self, **kwargs):
        data = super(InvoiceCreateView, self).get_context_data(**kwargs)
        data['invoice_items_formset'] = invoices_forms.InvoiceItemFormSet(self.request.POST) if self.request.POST else invoices_forms.InvoiceItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_items_formset = context['invoice_items_formset']
        if invoice_items_formset.is_valid():
            self.object = form.save()
            invoice_items_formset.instance = self.object
            invoice_items_formset.save()
            messages.success(self.request, 'Invoice with sequence-no. [%s] created successfully.' % self.object.seq_number)
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(context)
