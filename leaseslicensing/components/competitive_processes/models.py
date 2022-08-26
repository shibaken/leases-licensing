import uuid
from django.db import models
from django.db.models import Q
from django.contrib.gis.db.models.fields import PolygonField

from ledger_api_client.ledger_models import EmailUserRO
from leaseslicensing import settings
from leaseslicensing.components import competitive_processes
from leaseslicensing.components.main.models import CommunicationsLogEntry, Document, UserAction

from leaseslicensing.components.main.related_item import RelatedItem
from leaseslicensing.components.organisations.models import Organisation
from leaseslicensing.helpers import is_internal
from leaseslicensing.ledger_api_utils import retrieve_email_user


class CompetitiveProcessManager(models.Manager):

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                'originating_proposal',
            )
            .prefetch_related(
                'competitive_process_parties',
            )
        )


class CompetitiveProcess(models.Model):
    """A class to represent a competitive process"""

    objects = CompetitiveProcessManager()

    prefix = 'CP'

    # For status
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
    winner = models.ForeignKey("CompetitiveProcessParty", null=True, blank=True, on_delete=models.CASCADE)
    details = models.TextField(blank=True)
    generated_proposal = models.ForeignKey("Proposal", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = "leaseslicensing"
        verbose_name = "Competitive Process"
        verbose_name_plural = "Competitive Processes"

    @property
    def site(self):
        return 'site_name'

    @property
    def group(self):
        return 'group_name'

    @property
    def generated_from_registration_of_interest(self):
        if hasattr(self, 'originating_proposal'):
            if self.originating_proposal:
                return True
        return False

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
            ids = [int(i.lstrip(self.prefix)) for i in CompetitiveProcess.objects.all().values_list('lodgement_number', flat=True) if i]
            return max(ids) + 1 if ids else 1
        except Exception as e:
            print(e)

    def save(self, *args, **kwargs):
        super(CompetitiveProcess, self).save(*args, **kwargs)
        if self.lodgement_number == '':
            self.lodgement_number = self.prefix + '{:07d}'.format(self.next_lodgement_number)
            self.save()

    def get_related_items(self, **kwargs):
        return_list = []
        count = 0
        field_competitive_process = None
        field_names_to_display = ['originating_proposal', ]  # TODO: add   'originating_proposal', 'competitive_process', 'approval',
        all_fields = self._meta.get_fields()
        for a_field in all_fields:
            if a_field.name in field_names_to_display:
                field_objects = []
                if a_field.is_relation:
                    if a_field.many_to_many:
                        pass
                    elif a_field.many_to_one:  # foreign key
                        field_objects = [getattr(self, a_field.name),]
                    elif a_field.one_to_many:  # reverse foreign key
                        field_objects = a_field.related_model.objects.filter(**{a_field.remote_field.name: self})
                    elif a_field.one_to_one:
                        pass  # TODO: originating_proposal here..?
                for field_object in field_objects:
                    if field_object:
                        related_item = field_object.as_related_item
                        return_list.append(related_item)

        # serializer = RelatedItemsSerializer(return_list, many=True)
        # return serializer.data
        return return_list

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

    def can_user_view(self, user):
        if is_internal(user):  # TODO: confirm this condition
            return True
        return False

    def can_user_process(self, user):
        if self.assigned_officer == user:  # TODO: confirm this condition
            return True
        return False


class CompetitiveProcessGeometry(models.Model):
    competitive_process = models.ForeignKey(
        CompetitiveProcess, 
        on_delete=models.CASCADE, 
        related_name="competitive_process_geometries"
    )
    polygon = PolygonField(srid=4326, blank=True, null=True)
    # intersects = models.BooleanField(default=False)
    # copied_from = models.ForeignKey(
        # "self", on_delete=models.SET_NULL, blank=True, null=True
    # )

    class Meta:
        app_label = "leaseslicensing"


def update_competitive_process_doc_filename(instance, filename):
    return '{}/competitive_process/{}/{}'.format(
        settings.MEDIA_APP_DIR, 
        instance.competitive_process.id,
        filename,
    )


class CompetitiveProcessDocument(Document):
    competitive_process = models.ForeignKey(
        CompetitiveProcess, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='competitive_process_documents'
    )
    input_name = models.CharField(max_length=255, null=True, blank=True)
    _file = models.FileField(upload_to=update_competitive_process_doc_filename, max_length=512)
    
    class Meta:
        app_label = "leaseslicensing"


class CompetitiveProcessParty(models.Model):
    competitive_process = models.ForeignKey(
        CompetitiveProcess, 
        blank=True,
        null=True,
        on_delete=models.CASCADE, 
        related_name="competitive_process_parties"
    )
    person_id = models.IntegerField(null=True, blank=True)  # EmailUserRO
    organisation = models.ForeignKey(
        Organisation,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    invited_at = models.DateField(null=True, blank=True)
    removed_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = "leaseslicensing"
        ordering = ['invited_at']
        constraints = [
            models.CheckConstraint(
                # Either party_person or party_organisation must be None
                check=Q(person_id=None, organisation__isnull=False) | Q(person_id__isnull=False, organisation=None),
                name='either_one_null',
            )
        ]
    
    @property
    def is_person(self):
        if self.person_id:
            return True
        return False
    
    @property
    def person(self):
        if self.person_id:
            person = retrieve_email_user(self.person_id)
            return person
        return None

    @property
    def is_organisation(self):
        if self.organisation:
            return True
        return False


class PartyDetail(models.Model):
    competitive_processes_party = models.ForeignKey(
        CompetitiveProcessParty, 
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="party_details"
    )
    detail = models.TextField(blank=True)
    created_by = models.IntegerField(null=True, blank=True)  # EmailUserRO
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = "leaseslicensing"
        ordering = ['created_at']


def update_party_detail_doc_filename(instance, filename):
    return '{}/competitive_process/{}/party_detail/{}'.format(
        settings.MEDIA_APP_DIR, 
        instance.party_detail.competitive_process_party.competitive_process.id,
        uuid.uuid4()
    )
    # if instance.party_detail.competitive_process_party.is_person:
    #     party_folder_name = 'person'
    #     party_id = instance.party_detail.competitive_process_party.person
    # elif instance.party_detail.competitive_process_party.is_organisation:
    #     party_folder_name = 'organisation'
    #     party_id = instance.party_detail.competitive_process_party.organisation.id
    # else:
    #     party_folder_name = 'unsure_party'
    #     party_id = 'unsuer_id'
        
    # return "{}/competitive_process/{}/{}/{}/detail/{}/{}".format(
        # settings.MEDIA_APP_DIR, 
        # instance.party_detail.competitive_process_party.competitive_process.id,
        # party_folder_name,
        # party_id,
        # instance.party_detail.id,
        # filename,
    # )
# 

class PartyDetailDocument(Document):
    party_detail = models.ForeignKey(
        PartyDetail, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='party_detail_documents'
    )
    _file = models.FileField(upload_to=update_party_detail_doc_filename, max_length=512)
    
    class Meta:
        app_label = "leaseslicensing"


class CompetitiveProcessLogEntry(CommunicationsLogEntry):
    competitive_process = models.ForeignKey(
        CompetitiveProcess, related_name="comms_logs", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} - {}".format(self.reference, self.subject)

    class Meta:
        app_label = "leaseslicensing"

    def save(self, **kwargs):
        # save the competitive process id if the reference not provided
        if not self.reference:
            self.reference = self.competitive_process.id
        super().save(**kwargs)


class CompetitiveProcessUserAction(UserAction):
    ACTION_CREATE_CUSTOMER_ = "Create customer {}"
    ACTION_LINK_PARK = "Link park {} to application {}"

    competitive_process = models.ForeignKey(
        CompetitiveProcess, related_name="action_logs", on_delete=models.CASCADE
    )

    class Meta:
        app_label = "leaseslicensing"
        ordering = ("-when",)

    @classmethod
    def log_action(cls, competitive_process, action, user):
        return cls.objects.create(competitive_processes=competitive_process, who=user, what=str(action))

