import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, CreateView

from applications.customers import (
    forms as customers_forms,
    models as customers_models
)

from libs import mixins as libs_mixins


class CustomerProcessMixin(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin):

    model = customers_models.Customer
    form_class = customers_forms.CustomerCreateForm
    success_message = 'Customer [%s] processed successfully.'

    def get_success_url(self):
        return reverse_lazy('invoices:invoice_create', kwargs={'customer_id': int(self.object.id)})

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, _(self.success_message) % item.name)
        return super(CustomerProcessMixin, self).form_valid(form)


class CustomerCreateView(CustomerProcessMixin, CreateView):
    """ View to create a new item """

    template_name = 'customer/customer_create.html'
    success_message = 'Customer [%s] updated successfully.'

    def get_context_data(self, **kwargs):
        context_data = super(CustomerCreateView, self).get_context_data(**kwargs)
        context_data.update({'for_invoice': True})
        return context_data


class CustomerAutoCompleteView(LoginRequiredMixin, View):
    """ View to serve customer names autocomplete request """

    def get(self, request, *args, **kwargs):
        if 'term' in self.request.GET:
            term = self.request.GET['term']
            customer_array = [
                {'id': customer.id, 'text': customer.name}
                for customer in customers_models.Customer.objects.filter(Q(name__icontains=term) | Q(consumer_number__icontains=term))
            ]
            return HttpResponse(json.dumps({'results': customer_array}), content_type='application/json')

        return HttpResponseRedirect(reverse_lazy('user:login'))
