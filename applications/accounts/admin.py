from django.contrib import admin

from applications.accounts import models as accounts_models
from libs.admin import CustomModelAdmin


admin.site.register(accounts_models.User, CustomModelAdmin)
