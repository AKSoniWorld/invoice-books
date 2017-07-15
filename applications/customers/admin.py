from django.contrib import admin

from applications.customers import models as customers_models
from libs.admin import CustomModelAdmin


admin.site.register(customers_models.Customer, CustomModelAdmin)
admin.site.register(customers_models.CustomerExtraInfo, CustomModelAdmin)
