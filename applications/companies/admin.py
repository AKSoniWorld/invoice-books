from django.contrib import admin

from applications.companies import models as companies_models
from libs.admin import CustomModelAdmin


admin.site.register(companies_models.Company, CustomModelAdmin)
admin.site.register(companies_models.UserCompany, CustomModelAdmin)
