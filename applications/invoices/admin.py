from django.contrib import admin

from applications.invoices import models as invoices_models
from libs.admin import CustomModelAdmin


admin.site.register(invoices_models.Invoice, CustomModelAdmin)
admin.site.register(invoices_models.InvoiceItem, CustomModelAdmin)
admin.site.register(invoices_models.InvoiceItemTax, CustomModelAdmin)
