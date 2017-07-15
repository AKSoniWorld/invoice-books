from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView

from applications.inventories import (
    forms as inventories_forms,
    models as inventories_models
)

from libs import mixins as libs_mixins


class ItemListView(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin, ListView):
    """ View to list all items """

    model = inventories_models.Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items_list'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(company=self.user_company)


class ItemProcessMixin(LoginRequiredMixin, libs_mixins.CompanyRequiredMixin):

    model = inventories_models.Item
    success_url = reverse_lazy('inventories:item_list')
    success_message = 'Item [%s] processed successfully.'

    def get_initial(self):
        initial_data = super(ItemProcessMixin, self).get_initial()
        initial_data['company'] = self.user_company
        return initial_data

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, _(self.success_message) % item.name)
        return super(ItemProcessMixin, self).form_valid(form)


class ItemUpdateView(ItemProcessMixin, UpdateView):

    template_name = 'inventory/item_update.html'
    form_class = inventories_forms.ItemUpdateForm
    pk_url_kwarg = 'item_id'
    success_message = 'Item [%s] updated successfully.'


class ItemCreateView(ItemProcessMixin, CreateView):
    """ View to create a new item """

    form_class = inventories_forms.ItemCreateForm
    template_name = 'inventory/item_create.html'
    success_message = 'Item [%s] created successfully.'
