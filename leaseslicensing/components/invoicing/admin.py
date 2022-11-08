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


@admin.register(models.ReviewDateAnnually)
class ReviewDateAnnuallAdmin(admin.ModelAdmin):
    list_display = ['review_date', 'date_of_enforcement',]


@admin.register(models.ReviewDateQuarterly)
class ReviewDateQuarterlyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReviewDateMonthly)
class ReviewDateMonthlyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.InvoicingDateAnnually)
class InvoicingDateAnnuallyAdmin(admin.ModelAdmin):
    list_display = [
        # 'invoicing_date',
        'invoicing_date_display',
        'date_of_enforcement',
        'is_currently_activated',
    ]


@admin.register(models.InvoicingDateQuarterly)
class InvoicingDateQuarterlyAdmin(admin.ModelAdmin):
    list_display = [
        'invoicing_date_q1_display',
        'invoicing_date_q2_display',
        'invoicing_date_q3_display',
        'invoicing_date_q4_display',
        'date_of_enforcement',
        'is_currently_activated',
    ]


@admin.register(models.InvoicingDateMonthly)
class InvoicingDateMonthlyAdmin(admin.ModelAdmin):
    list_display = [
        'invoicing_date_display',
        'date_of_enforcement',
        'is_currently_activated',
    ]


@admin.register(models.ConsumerPriceIndex)
class ConsumerPriceIndexAdmin(admin.ModelAdmin):
    list_display = ['year', 'name', 'cpi_value_q1', 'cpi_value_q2', 'cpi_value_q3', 'cpi_value_q4']
    list_display_links = ['year', 'name',]
    exclude = ['year',]
