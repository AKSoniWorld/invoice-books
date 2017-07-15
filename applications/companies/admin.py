from django.contrib import admin

from applications.companies import models as companies_models


admin.site.register(companies_models.Company)
admin.site.register(companies_models.UserCompany)
