from django.contrib import admin
from django import forms as django_forms
from leaseslicensing.components.approvals import models


@admin.register(models.ApprovalSubType)
class ApprovalSubTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ApprovalTypeDocumentType)
class ApprovalTypeDocumentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ApprovalType)
class ApprovalTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ["approval_type_document_types"]

    fieldsets = (
        ('Approval Type', {'fields': ('name','details_placeholder',)}),
        ('Approval Type Document Types', {'fields': ('approval_type_document_types',)}),
    )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        kwargs["queryset"] = models.ApprovalTypeDocumentType.objects.all()
        return super(ApprovalTypeAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


