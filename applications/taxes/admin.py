from django.contrib import admin

from applications.taxes import models as taxes_models


admin.site.register(taxes_models.Tax)
