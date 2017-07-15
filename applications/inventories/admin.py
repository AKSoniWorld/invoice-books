from django.contrib import admin

from applications.inventories import models as inventories_models


admin.site.register(inventories_models.Item)
