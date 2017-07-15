from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView

from applications.inventories import (
    forms as inventories_forms,
    models as inventories_models
)

from libs import utils as libs_utils


class ItemListView(LoginRequiredMixin, ListView):
    """ View to list all items """

    model = inventories_models.Item
    template_name = 'inventory/items_list.html'
    context_object_name = 'items_list'
    paginate_by = 20


class ItemUpdateView(LoginRequiredMixin, UpdateView):

    model = inventories_models.Item
    form_class = inventories_forms.ItemUpdateForm
    template_name = 'inventory/item_update.html'
    success_url = reverse_lazy('inventories:item_list')
    pk_url_kwarg = 'item_id'

    def get_initial(self):
        initial_data = super(ItemUpdateView, self).get_initial()
        initial_data['company'] = libs_utils.get_current_company(self.request.user)
        return initial_data

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, _('Item [%s] updated successfully.') % item.name)
        return super(ItemUpdateView, self).form_valid(form)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """ View to create a new item """

    model = inventories_models.Item
    form_class = inventories_forms.ItemUpdateForm
    template_name = 'inventory/item_update.html'
    success_url = reverse_lazy('inventory:item_list')

    def get_initial(self):
        initial_data = super(ItemCreateView, self).get_initial()
        initial_data['company'] = libs_utils.get_current_company(self.request.user)
        return initial_data

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, _('Item [%s] created successfully.') % item.name)
        return super(ItemCreateView, self).form_valid(form)