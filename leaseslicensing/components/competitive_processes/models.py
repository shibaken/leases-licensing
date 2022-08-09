from django.db import models
from ledger_api_client.ledger_models import EmailUserRO

from leaseslicensing.components.main.related_item import RelatedItem
from leaseslicensing.ledger_api_utils import retrieve_email_user


class CompetitiveProcess(models.Model):
    prefix = 'CP'
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DISCARDED = "discarded"
    STATUS_COMPLETED_APPLICATION = "completed_application"
    STATUS_COMPLETED_DECLINED = "completed_declined"
    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, "In Progress"), 
        (STATUS_DISCARDED, "Discarded"),
        (STATUS_COMPLETED_APPLICATION, "Completed (Application)"),
        (STATUS_COMPLETED_DECLINED, "Completed (Declined)"),
    )

    lodgement_number = models.CharField(max_length=9, blank=True, default="")
    status = models.CharField("Status", max_length=30, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0],)
    assigned_officer_id = models.IntegerField(null=True, blank=True)  # EmailUserRO
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = "leaseslicensing"
        verbose_name = "Competitive Process"
        verbose_name_plural = "Competitive Processes"

    @property
    def generated_from_registration_of_interest(self):
        if self.generating_proposal:
            return True
        return False

    @property
    def registration_of_interest(self):
        if self.generated_from_registration_of_interest:
            return self.generating_proposal
        return None

    @property
    def is_assigned(self):
        if self.assigned_officer_id:
            return True
        return False

    @property
    def assigned_officer(self):
        if self.is_assigned:
            return retrieve_email_user(self.assigned_officer_id)
        return None

    @property
    def next_lodgement_number(self):
        try:
            ids = [int(i) for i in CompetitiveProcess.objects.all().values_list('lodgement_number', flat=True) if i]
            return max(ids) + 1 if ids else 1
        except Exception as e:
            print(e)

    def save(self, *args, **kwargs):
        super(CompetitiveProcess, self).save(*args, **kwargs)
        if self.lodgement_number == '':
            self.lodgement_number = self.prefix + '{:07d}'.format(self.next_lodgement_number)
            self.save()

    @property
    def as_related_item(self):
        related_item = RelatedItem(
            identifier=self.related_item_identifier,
            model_name=self._meta.verbose_name,
            descriptor=self.related_item_descriptor,
            action_url='<a href=/internal/competitive_process/{} target="_blank">Open</a>'.format(self.id)
        )
        return related_item

    @property
    def related_item_identifier(self):
        return self.lodgement_number

    @property
    def related_item_descriptor(self):
        return '(return descriptor)'