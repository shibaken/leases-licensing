from django.contrib import admin
from leaseslicensing.components.invoicing import models


@admin.register(models.ChargeMethod)
class ChargeMethodAdmin(admin.ModelAdmin):
    list_display = ['key', 'display_name',]
    # max_num = 0  # This removes 'Add another ...' button
    readonly_fields = ('key',)

    def has_add_permission(self, request, obj=None):
        # Remove 'Add ...' button
        return False

    def has_delete_permission(self, request, obj=None):
        # Remove 'Delete'
        return False
