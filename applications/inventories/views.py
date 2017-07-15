from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from applications.inventories import models as inventories_models


# class ItemCreateView(LoginRequiredMixin, CreateView):
#     """ View to create a new item """
#
#     model = inventories_models.Item
#     success_url = reverse_lazy('inventory:item_list')
#
#
class ItemListView(LoginRequiredMixin, ListView):
    """ View to list all items """

    model = inventories_models.Item
    template_name = 'inventory/items_list.html'
    context_object_name = 'items_list'
    paginate_by = 20


# class UpdateItemView(LoginRequiredMixin, UpdateView):
#     """ View to update an existing item """
#     # MIXIN will not work if dispatch is overridden
#     # add decorators manually to overridden dispatch for it to work.
#
#     model = Item
#     form_class = ItemUpdateForm
#     template_name = 'inventory/admin/item_update.html'
#     success_url = reverse_lazy('inventory:dashboard_admin')
#     pk_url_kwarg = 'item_id'
#
#     def form_valid(self, form):
#         item = form.save()
#         item_update_signal.send_robust(sender=UpdateItemView, item=item)
#         messages.success(self.request, _('Item [%s] updated successfully.') % item.name)
#         return super(UpdateItemView, self).form_valid(form)
#
#
