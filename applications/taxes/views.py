from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView

from applications.taxes import (
    forms as taxes_forms,
    models as taxes_models
)

from libs import mixins as libs_mixins


class TaxListView(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin, ListView):
    """ View to list all taxes """

    model = taxes_models.Tax
    template_name = 'tax/tax_list.html'
    context_object_name = 'taxes_list'
    paginate_by = 20


class TaxProcessMixin(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin):

    model = taxes_models.Tax
    success_url = reverse_lazy('taxes:tax_list')
    form_class = taxes_forms.TaxCreateUpdateForm
    success_message = 'Tax [%s] processed successfully.'

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, _(self.success_message) % item.name)
        return super(TaxProcessMixin, self).form_valid(form)


class TaxUpdateView(TaxProcessMixin, UpdateView):

    template_name = 'tax/tax_update.html'
    pk_url_kwarg = 'tax_id'
    success_message = 'Tax [%s] updated successfully.'


class TaxCreateView(TaxProcessMixin, CreateView):
    """ View to create a new item """

    template_name = 'tax/tax_create.html'
    success_message = 'Tax [%s] updated successfully.'
