from django.contrib import admin

from applications.inventories import models as inventories_models
from libs.admin import CustomModelAdmin


admin.site.register(inventories_models.Item, CustomModelAdmin)
