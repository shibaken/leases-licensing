from django.db import models
from datetime import datetime
import pytz
from ledger_api_client import settings_base


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class ChargeMethod(models.Model):
    """A class to represent a competitive process"""

    key = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200,)

    class Meta:
        app_label = "leaseslicensing"

    def __str__(self):
        return self.display_name


class ReviewDateAnnually(BaseModel):
    review_date = models.DateField(null=True, blank=True)
    date_of_enforcement = models.DateField()

    class Meta:
        app_label = "leaseslicensing"

    @staticmethod
    def get_review_date_annually_by_date(target_date=datetime.now(pytz.timezone(settings_base.TIME_ZONE)).date()):
        """
        Return an setting object which is enabled at the target_date
        """
        review_date_annually = ReviewDateAnnually.objects.filter(
            date_of_enforcement__lte=target_date,
        ).order_by('date_of_enforcement').last()
        return review_date_annually


class ReviewDateQuarterly(BaseModel):
    review_date_q1 = models.DateField()
    review_date_q2 = models.DateField()
    review_date_q3 = models.DateField()
    review_date_q4 = models.DateField()
    date_of_enforcement = models.DateField()

    class Meta:
        app_label = "leaseslicensing"

    @staticmethod
    def get_review_date_quarterly_by_date(target_date=datetime.now(pytz.timezone(settings_base.TIME_ZONE)).date()):
        """
        Return an setting object which is enabled at the target_date
        """
        review_date_quarterly = ReviewDateQuarterly.objects.filter(
            date_of_enforcement__lte=target_date,
        ).order_by('date_of_enforcement').last()
        return review_date_quarterly


class ReviewDateMonthly(BaseModel):
    review_date = models.PositiveSmallIntegerField(null=True, blank=True)
    date_of_enforcement = models.DateField()

    class Meta:
        app_label = "leaseslicensing"

    @staticmethod
    def get_review_date_monthly_by_date(target_date=datetime.now(pytz.timezone(settings_base.TIME_ZONE)).date()):
        """
        Return an setting object which is enabled at the target_date
        """
        review_date_monthly = ReviewDateMonthly.objects.filter(
            date_of_enforcement__lte=target_date,
        ).order_by('date_of_enforcement').last()
        return review_date_monthly


class InvoicingDateAnnually(BaseModel):
    invoicing_date = models.DateField(null=True, blank=True)
    date_of_enforcement = models.DateField()

    class Meta:
        app_label = "leaseslicensing"

    @staticmethod
    def get_invoicing_date_annually_by_date(target_date=datetime.now(pytz.timezone(settings_base.TIME_ZONE)).date()):
        """
        Return an setting object which is enabled at the target_date
        """
        invoicing_date_annually = InvoicingDateAnnually.objects.filter(
            date_of_enforcement__lte=target_date,
        ).order_by('date_of_enforcement').last()
        return invoicing_date_annually


class InvoicingDateQuarterly(BaseModel):
    invoicing_date_q1 = models.DateField()
    invoicing_date_q2 = models.DateField()
    invoicing_date_q3 = models.DateField()
    invoicing_date_q4 = models.DateField()
    date_of_enforcement = models.DateField()

    class Meta:
        app_label = "leaseslicensing"

    @staticmethod
    def get_invoicing_date_quarterly_by_date(target_date=datetime.now(pytz.timezone(settings_base.TIME_ZONE)).date()):
        """
        Return an setting object which is enabled at the target_date
        """
        invoicing_date_quarterly = InvoicingDateQuarterly.objects.filter(
            date_of_enforcement__lte=target_date,
        ).order_by('date_of_enforcement').last()
        return invoicing_date_quarterly


class InvoicingDateMonthly(BaseModel):
    invoicing_date = models.PositiveSmallIntegerField(null=True, blank=True)
    date_of_enforcement = models.DateField()

    class Meta:
        app_label = "leaseslicensing"

    @staticmethod
    def get_invoicing_date_monthly_by_date(target_date=datetime.now(pytz.timezone(settings_base.TIME_ZONE)).date()):
        """
        Return an setting object which is enabled at the target_date
        """
        invoicing_date_monthly = InvoicingDateMonthly.objects.filter(
            date_of_enforcement__lte=target_date,
        ).order_by('date_of_enforcement').last()
        return invoicing_date_monthly


class InvoicingDetails(BaseModel):
    """
    This is the main model to store invoicing details, generated by a proposal first (Proposal has a field: invoicing_details)
    then copied and/or edited as business run
    """
    charge_method = models.ForeignKey(ChargeMethod, null=True, blank=True, on_delete=models.SET_NULL)
    base_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    once_off_charge_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    review_once_every = models.PositiveSmallIntegerField(null=True, blank=True)
    invoicing_once_every = models.PositiveSmallIntegerField(null=True, blank=True)

    # Review dates
    # review_date_annually = models.ForeignKey(ReviewDateAnnually, null=True, blank=True, on_delete=models.SET_NULL)
    # review_date_quarterly = models.ForeignKey(ReviewDateQuarterly, null=True, blank=True, on_delete=models.SET_NULL)
    # review_date_monthly = models.ForeignKey(ReviewDateMonthly, null=True, blank=True, on_delete=models.SET_NULL)

    # Invoicing dates
    # invoicing_date_annually = models.ForeignKey(InvoicingDateAnnually, null=True, blank=True, on_delete=models.SET_NULL)
    # invoicing_date_quarterly = models.ForeignKey(InvoicingDateQuarterly, null=True, blank=True, on_delete=models.SET_NULL)
    # invoicing_date_monthly = models.ForeignKey(InvoicingDateMonthly, null=True, blank=True, on_delete=models.SET_NULL)

    approval = models.ForeignKey('Approval', null=True, blank=True, on_delete=models.SET_NULL)
    previous_invoicing_details = models.OneToOneField('self', null=True, blank=True, related_name='next_invoicing_details', on_delete=models.SET_NULL)

    class Meta:
        app_label = "leaseslicensing"

        # constraints = [
        #     models.CheckConstraint(
        #         check=Q(base_fee_amount=0) | Q(once_off_charge_amount=0),
        #         name='either_one_null',
        #     )
        # ]
