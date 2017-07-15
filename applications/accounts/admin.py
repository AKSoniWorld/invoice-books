from django.contrib import admin

from applications.accounts import models as accounts_models


admin.site.register(accounts_models.User)
