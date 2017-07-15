from django.contrib import admin

from applications.taxes import models as taxes_models
from libs.admin import CustomModelAdmin


admin.site.register(taxes_models.Tax, CustomModelAdmin)
admin.site.register(taxes_models.ItemTax, CustomModelAdmin)
