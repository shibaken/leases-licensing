from django.contrib import admin
from leaseslicensing.components.approvals import models


@admin.register(models.ApprovalSubType)
class ApprovalSubTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ApprovalType)
class ApprovalTypeAdmin(admin.ModelAdmin):
    pass
