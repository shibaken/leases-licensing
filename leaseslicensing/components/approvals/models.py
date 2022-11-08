from __future__ import unicode_literals

import logging
import re

import json
import datetime
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError

# from django.contrib.postgres.fields.jsonb import JSONField
from django.db.models import JSONField
from django.utils import timezone
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models import Q

# from ledger.accounts.models import Organisation as ledger_organisation
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from leaseslicensing.components.main.models import RevisionedMixin
from leaseslicensing import exceptions
from leaseslicensing.components.main.related_item import RelatedItem
from leaseslicensing.components.organisations.models import Organisation
from leaseslicensing.components.proposals.models import (
    Proposal,
    ProposalUserAction,
    RequirementDocument,
    ProposalType,
)
from leaseslicensing.components.main.models import (
    CommunicationsLogEntry,
    UserAction,
    Document,
    ApplicationType,
)
from leaseslicensing.components.approvals.email import (
    send_approval_expire_email_notification,
    send_approval_cancel_email_notification,
    send_approval_suspend_email_notification,
    send_approval_reinstate_email_notification,
    send_approval_surrender_email_notification,
)
from leaseslicensing.settings import PROPOSAL_TYPE_AMENDMENT, PROPOSAL_TYPE_RENEWAL
from leaseslicensing.utils import search_keys, search_multiple_keys
from leaseslicensing.helpers import is_customer

# from leaseslicensing.components.approvals.email import send_referral_email_notification

logger = logging.getLogger(__name__)


def update_approval_doc_filename(instance, filename):
    return "{}/proposals/{}/approvals/{}".format(
        settings.MEDIA_APP_DIR, instance.approval.current_proposal.id, filename
    )


def update_approval_comms_log_filename(instance, filename):
    return "{}/proposals/{}/approvals/communications/{}".format(
        settings.MEDIA_APP_DIR,
        instance.log_entry.approval.current_proposal.id,
        filename,
    )


class ApprovalDocument(Document):
    approval = models.ForeignKey(
        "Approval", related_name="documents", on_delete=models.CASCADE
    )
    _file = models.FileField(upload_to=update_approval_doc_filename, max_length=512)
    can_delete = models.BooleanField(
        default=True
    )  # after initial submit prevent document from being deleted

    def delete(self):
        if self.can_delete:
            return super(ApprovalDocument, self).delete()
        logger.info(
            "Cannot delete existing document object after Application has been submitted (including document submitted before Application pushback to status Draft): {}".format(
                self.name
            )
        )

    class Meta:
        app_label = "leaseslicensing"


class ApprovalSubType(RevisionedMixin):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        app_label = "leaseslicensing"

    def __str__(self):
        return self.name


class ApprovalType(RevisionedMixin):
    name = models.CharField(max_length=200, unique=True)
    details_placeholder = models.CharField(max_length=200, blank=True)
    #approval_type_document_types = models.ManyToManyField("ApprovalTypeDocumentType", through='ApprovalTypeDocumentTypeOnApprovalType')
    approvaltypedocumenttypes = models.ManyToManyField("ApprovalTypeDocumentType", through='ApprovalTypeDocumentTypeOnApprovalType')
    class Meta:
        app_label = "leaseslicensing"

    def __str__(self):
        return self.name


class ApprovalTypeDocumentType(RevisionedMixin):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        app_label = "leaseslicensing"

    def __str__(self):
        return self.name


class ApprovalTypeDocumentTypeOnApprovalType(RevisionedMixin):
    approval_type = models.ForeignKey(ApprovalType, on_delete=models.CASCADE)
    approval_type_document_type = models.ForeignKey(ApprovalTypeDocumentType, on_delete=models.CASCADE)
    mandatory = models.BooleanField(default=False)

    class Meta:
        app_label = "leaseslicensing"
        unique_together = ("approval_type", "approval_type_document_type")


class Approval(RevisionedMixin):
    APPROVAL_STATUS_CURRENT = "current"
    APPROVAL_STATUS_EXPIRED = "expired"
    APPROVAL_STATUS_CANCELLED = "cancelled"
    APPROVAL_STATUS_SURRENDERED = "surrendered"
    APPROVAL_STATUS_SUSPENDED = "suspended"
    APPROVAL_STATUS_EXTENDED = "extended"
    APPROVAL_STATUS_AWAITING_PAYMENT = "awaiting_payment"

    STATUS_CHOICES = (
        (APPROVAL_STATUS_CURRENT, "Current"),
        (APPROVAL_STATUS_EXPIRED, "Expired"),
        (APPROVAL_STATUS_CANCELLED, "Cancelled"),
        (APPROVAL_STATUS_SURRENDERED, "Surrendered"),
        (APPROVAL_STATUS_SUSPENDED, "Suspended"),
        (APPROVAL_STATUS_EXTENDED, "extended"),
        (APPROVAL_STATUS_AWAITING_PAYMENT, "Awaiting Payment"),
    )
    lodgement_number = models.CharField(max_length=9, blank=True, default="")
    status = models.CharField(
        max_length=40, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    licence_document = models.ForeignKey(
        ApprovalDocument,
        blank=True,
        null=True,
        related_name="licence_document",
        on_delete=models.SET_NULL,
    )
    cover_letter_document = models.ForeignKey(
        ApprovalDocument,
        blank=True,
        null=True,
        related_name="cover_letter_document",
        on_delete=models.SET_NULL,
    )
    replaced_by = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL
    )
    # current_proposal = models.ForeignKey(Proposal,related_name = '+')
    current_proposal = models.ForeignKey(
        Proposal, related_name="approvals", null=True, on_delete=models.SET_NULL
    )
    #    activity = models.CharField(max_length=255)
    #    region = models.CharField(max_length=255)
    #    tenure = models.CharField(max_length=255,null=True)
    #    title = models.CharField(max_length=255)
    renewal_document = models.ForeignKey(
        ApprovalDocument,
        blank=True,
        null=True,
        related_name="renewal_document",
        on_delete=models.SET_NULL,
    )
    renewal_sent = models.BooleanField(default=False)
    issue_date = models.DateTimeField()
    original_issue_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    expiry_date = models.DateField()
    surrender_details = JSONField(blank=True, null=True)
    suspension_details = JSONField(blank=True, null=True)
    # submitter = models.ForeignKey(EmailUser, on_delete=models.PROTECT, blank=True, null=True, related_name='leaseslicensing_approvals')
    submitter = models.IntegerField()  # EmailUserRo
    org_applicant = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="org_approvals",
    )
    # proxy_applicant = models.ForeignKey(EmailUser,on_delete=models.PROTECT, blank=True, null=True, related_name='proxy_approvals')
    proxy_applicant = models.IntegerField(null=True)  # EmailUserRO
    extracted_fields = JSONField(blank=True, null=True)
    cancellation_details = models.TextField(blank=True)
    extend_details = models.TextField(blank=True)
    cancellation_date = models.DateField(blank=True, null=True)
    set_to_cancel = models.BooleanField(default=False)
    set_to_suspend = models.BooleanField(default=False)
    set_to_surrender = models.BooleanField(default=False)

    # application_type = models.ForeignKey(ApplicationType, null=True, blank=True)
    renewal_count = models.PositiveSmallIntegerField(
        "Number of times an Approval has been renewed", default=0
    )
    migrated = models.BooleanField(default=False)
    # for eclass licence as it can be extended/ renewed once
    extended = models.BooleanField(default=False)
    expiry_notice_sent = models.BooleanField(default=False)

    class Meta:
        app_label = "leaseslicensing"
        unique_together = ("lodgement_number", "issue_date")

    # @classmethod
    # def approval_types_dict(cls, include_codes=[]):
    #    type_list = []
    #    for approval_type in Approval.__subclasses__():
    #        if hasattr(approval_type, 'code'):
    #            if approval_type.code in include_codes:
    #                type_list.append({
    #                    "code": approval_type.code,
    #                    "description": approval_type.description,
    #                })

    #    return type_list

    @property
    def bpay_allowed(self):
        if self.org_applicant:
            return self.org_applicant.bpay_allowed
        return False

    @property
    def monthly_invoicing_allowed(self):
        if self.org_applicant:
            return self.org_applicant.monthly_invoicing_allowed
        return False

    @property
    def monthly_invoicing_period(self):
        if self.org_applicant:
            return self.org_applicant.monthly_invoicing_period
        return None

    @property
    def monthly_payment_due_period(self):
        if self.org_applicant:
            return self.org_applicant.monthly_payment_due_period
        return None

    @property
    def applicant(self):
        if self.org_applicant:
            return self.org_applicant.organisation.name
        elif self.proxy_applicant:
            return "{} {}".format(
                self.proxy_applicant.first_name, self.proxy_applicant.last_name
            )
        else:
            # return None
            try:
                return "{} {}".format(
                    self.submitter.first_name, self.submitter.last_name
                )
            except:
                return "Applicant Not Set"

    @property
    def linked_applications(self):
        ids = Proposal.objects.filter(
            approval__lodgement_number=self.lodgement_number
        ).values_list("id", flat=True)
        all_linked_ids = Proposal.objects.filter(
            Q(previous_application__in=ids) | Q(id__in=ids)
        ).values_list("lodgement_number", flat=True)
        return all_linked_ids

    @property
    def applicant_type(self):
        if self.org_applicant:
            return "org_applicant"
        elif self.proxy_applicant:
            return "proxy_applicant"
        else:
            # return None
            return "submitter"

    @property
    def is_org_applicant(self):
        return True if self.org_applicant else False

    @property
    def applicant_id(self):
        if self.org_applicant:
            # return self.org_applicant.organisation.id
            return self.org_applicant.id
        elif self.proxy_applicant:
            return self.proxy_applicant.id
        else:
            # return None
            return self.submitter.id

    @property
    def region(self):
        return self.current_proposal.region.name

    @property
    def district(self):
        return self.current_proposal.district.name

    @property
    def tenure(self):
        return self.current_proposal.tenure.name

    @property
    def activity(self):
        return self.current_proposal.activity

    @property
    def title(self):
        return self.current_proposal.title

    @property
    def next_id(self):
        ids = map(
            int,
            [
                re.sub("^[A-Za-z]*", "", i)
                for i in Approval.objects.all().values_list(
                    "lodgement_number", flat=True
                )
                if i
            ],
        )
        ids = list(ids)
        return max(ids) + 1 if ids else 1

    # @property
    # def next_id(self):
    #    ids = map(int,[i.split('L')[1] for i in Approval.objects.all().values_list('lodgement_number', flat=True) if i])
    #    return max(list(ids)) + 1 if len(list(ids)) else 1

    def save(self, *args, **kwargs):
        if self.lodgement_number in ["", None]:
            self.lodgement_number = "L{0:06d}".format(self.next_id)
            # self.save()
        super(Approval, self).save(*args, **kwargs)

    def __str__(self):
        return self.lodgement_number

    @property
    def reference(self):
        return "L{}".format(self.id)

    @property
    def can_reissue(self):
        return self.status == "current" or self.status == "suspended"

    @property
    def can_reinstate(self):
        return (
            self.status == "cancelled"
            or self.status == "suspended"
            or self.status == "surrendered"
        ) and self.can_action

    @property
    def allowed_assessors(self):
        return self.current_proposal.allowed_assessors

    def is_assessor(self, user):
        if self.current_proposal:
            return self.current_proposal.is_assessor(user)
        else:
            logger.warning('Approval {} does not have current_proposal'.format(self.lodgement_number))
            return False

    def is_approver(self, user):
        if self.current_proposal:
            return self.current_proposal.is_approver(user)
        else:
            logger.warning('Approval {} does not have current_proposal'.format(self.lodgement_number))
            return False

    @property
    def is_issued(self):
        return self.licence_number is not None and len(self.licence_number) > 0

    @property
    def can_action(self):
        if not (self.set_to_cancel or self.set_to_suspend or self.set_to_surrender):
            return True
        else:
            return False

    @property
    def can_extend(self):
        if self.current_proposal:
            if self.current_proposal.application_type.name == "E Class":
                return (
                    self.current_proposal.application_type.max_renewals
                    > self.renewal_count
                )
        return False

    @property
    def can_renew(self):
        try:
            renew_conditions = {
                "previous_application": self.current_proposal,
                "proposal_type": ProposalType.objects.get(code=PROPOSAL_TYPE_RENEWAL),
            }
            proposal = Proposal.objects.get(**renew_conditions)
            if proposal:
                return False
        except Proposal.DoesNotExist:
            return True

    ## copy amend_renew() from ML?
    @property
    def can_amend(self):
        # try:
        if self.renewal_document and self.renewal_sent:
            # amend_renew = 'renew'
            return False
        else:
            amend_conditions = {
                "previous_application": self.current_proposal,
                "proposal_type": ProposalType.objects.get(code=PROPOSAL_TYPE_AMENDMENT),
            }
            proposals = Proposal.objects.filter(**amend_conditions)
            if proposals:
                if proposals.count() > 1:
                    logging.error('Approval: {} has more than one current amendment proposals'.format(self.lodgement_number))
                return False
        return True

    @property
    def approved_by(self):
        return self.current_proposal.approved_by

    @property
    def requirement_docs(self):
        if self.current_proposal:
            requirement_ids = (
                self.current_proposal.requirements.all()
                .exclude(is_deleted=True)
                .values_list("id", flat=True)
            )
            if requirement_ids:
                req_doc = RequirementDocument.objects.filter(
                    requirement__in=requirement_ids, visible=True
                )
                return req_doc
        else:
            logger.warning('Approval {} does not have current_proposal'.format(self.lodgement_number))
        return None

    #    @property
    #    def approved_by(self):
    #        try:
    #            proposal = self.proposal_set.all().order_by('-id')[0]
    #            if proposal.application_type.name == ApplicationType.FILMING:
    #                return proposal.action_logs.filter(what__contains='Awaiting Payment').last().who
    #            return proposal.action_logs.filter(what__contains='Issue Licence').last().who
    #        except:
    #            return None

    def generate_doc(self, user, preview=False):
        from leaseslicensing.components.approvals.pdf import (
            create_approval_doc,
            create_approval_pdf_bytes,
        )

        copied_to_permit = self.copiedToPermit_fields(
            self.current_proposal
        )  # Get data related to isCopiedToPermit tag

        if preview:
            return create_approval_pdf_bytes(
                self, self.current_proposal, copied_to_permit, user
            )

        self.licence_document = create_approval_doc(
            self, self.current_proposal, copied_to_permit, user
        )
        self.save(
            version_comment="Created Approval PDF: {}".format(
                self.licence_document.name
            )
        )
        self.current_proposal.save(
            version_comment="Created Approval PDF: {}".format(
                self.licence_document.name
            )
        )

    #    def generate_preview_doc(self, user):
    #        from leaseslicensing.components.approvals.pdf import create_approval_pdf_bytes
    #        copied_to_permit = self.copiedToPermit_fields(self.current_proposal) #Get data related to isCopiedToPermit tag

    def generate_renewal_doc(self):
        from leaseslicensing.components.approvals.pdf import create_renewal_doc

        self.renewal_document = create_renewal_doc(self, self.current_proposal)
        self.save(
            version_comment="Created Approval PDF: {}".format(
                self.renewal_document.name
            )
        )
        self.current_proposal.save(
            version_comment="Created Approval PDF: {}".format(
                self.renewal_document.name
            )
        )

    def copiedToPermit_fields(self, proposal):
        p = proposal
        copied_data = []
        search_assessor_data = []
        search_schema = search_multiple_keys(
            p.schema, primary_search="isCopiedToPermit", search_list=["label", "name"]
        )
        if p.assessor_data:
            search_assessor_data = search_keys(
                p.assessor_data, search_list=["assessor", "name"]
            )
        if search_schema:
            for c in search_schema:
                try:
                    if search_assessor_data:
                        for d in search_assessor_data:
                            if c["name"] == d["name"]:
                                if d["assessor"]:
                                    # copied_data.append({c['label'], d['assessor']})
                                    copied_data.append({c["label"]: d["assessor"]})
                except:
                    raise
        return copied_data

    def log_user_action(self, action, request):
        return ApprovalUserAction.log_action(self, action, request.user)

    def expire_approval(self, user):
        with transaction.atomic():
            try:
                today = timezone.localtime(timezone.now()).date()
                if self.status == "current" and self.expiry_date < today:
                    self.status = "expired"
                    self.save()
                    send_approval_expire_email_notification(self)
                    proposal = self.current_proposal
                    ApprovalUserAction.log_action(
                        self,
                        ApprovalUserAction.ACTION_EXPIRE_APPROVAL.format(self.id),
                        user,
                    )
                    ProposalUserAction.log_action(
                        proposal,
                        ProposalUserAction.ACTION_EXPIRED_APPROVAL_.format(proposal.id),
                        user,
                    )
            except:
                raise

    def approval_extend(self, request, details):
        with transaction.atomic():
            try:
                if not request.user in self.allowed_assessors:
                    raise ValidationError(
                        "You do not have access to extend this approval"
                    )
                if not self.can_extend and self.can_action:
                    raise ValidationError("You cannot extend approval any further")
                self.renewal_count += 1
                self.extend_details = details.get("extend_details")
                self.expiry_date = datetime.date(
                    self.expiry_date.year
                    + self.current_proposal.application_type.max_renewal_period,
                    self.expiry_date.month,
                    self.expiry_date.day,
                )
                today = timezone.now().date()
                if self.expiry_date <= today:
                    if not self.status == "extended":
                        self.status = "extended"
                        # send_approval_extend_email_notification(self)
                self.extended = True
                self.save()
                # Log proposal action
                self.log_user_action(
                    ApprovalUserAction.ACTION_EXTEND_APPROVAL.format(self.id), request
                )
                # Log entry for organisation
                self.current_proposal.log_user_action(
                    ProposalUserAction.ACTION_EXTEND_APPROVAL.format(
                        self.current_proposal.id
                    ),
                    request,
                )
            except:
                raise

    def approval_cancellation(self, request, details):
        with transaction.atomic():
            try:
                if not request.user in self.allowed_assessors:
                    raise ValidationError(
                        "You do not have access to cancel this approval"
                    )
                if not self.can_reissue and self.can_action:
                    raise ValidationError(
                        "You cannot cancel approval if it is not current or suspended"
                    )
                self.cancellation_date = details.get("cancellation_date").strftime(
                    "%Y-%m-%d"
                )
                self.cancellation_details = details.get("cancellation_details")
                cancellation_date = datetime.datetime.strptime(
                    self.cancellation_date, "%Y-%m-%d"
                )
                cancellation_date = cancellation_date.date()
                self.cancellation_date = cancellation_date  # test hack
                today = timezone.now().date()
                if cancellation_date <= today:
                    if not self.status == "cancelled":
                        self.status = "cancelled"
                        self.set_to_cancel = False
                        send_approval_cancel_email_notification(self)
                else:
                    self.set_to_cancel = True
                self.save()
                # Log proposal action
                self.log_user_action(
                    ApprovalUserAction.ACTION_CANCEL_APPROVAL.format(self.id), request
                )
                # Log entry for organisation
                self.current_proposal.log_user_action(
                    ProposalUserAction.ACTION_CANCEL_APPROVAL.format(
                        self.current_proposal.id
                    ),
                    request,
                )
            except:
                raise

    def approval_suspension(self, request, details):
        with transaction.atomic():
            try:
                if not request.user in self.allowed_assessors:
                    raise ValidationError(
                        "You do not have access to suspend this approval"
                    )
                if not self.can_reissue and self.can_action:
                    raise ValidationError(
                        "You cannot suspend approval if it is not current or suspended"
                    )
                if details.get("to_date"):
                    to_date = details.get("to_date").strftime("%d/%m/%Y")
                else:
                    to_date = ""
                self.suspension_details = {
                    "from_date": details.get("from_date").strftime("%d/%m/%Y"),
                    "to_date": to_date,
                    "details": details.get("suspension_details"),
                }
                today = timezone.now().date()
                from_date = datetime.datetime.strptime(
                    self.suspension_details["from_date"], "%d/%m/%Y"
                )
                from_date = from_date.date()
                if from_date <= today:
                    if not self.status == "suspended":
                        self.status = "suspended"
                        self.set_to_suspend = False
                        self.save()
                        send_approval_suspend_email_notification(self)
                else:
                    self.set_to_suspend = True
                self.save()
                # Log approval action
                self.log_user_action(
                    ApprovalUserAction.ACTION_SUSPEND_APPROVAL.format(self.id), request
                )
                # Log entry for proposal
                self.current_proposal.log_user_action(
                    ProposalUserAction.ACTION_SUSPEND_APPROVAL.format(
                        self.current_proposal.id
                    ),
                    request,
                )
            except:
                raise

    def reinstate_approval(self, request):
        with transaction.atomic():
            try:
                if not request.user in self.allowed_assessors:
                    raise ValidationError(
                        "You do not have access to reinstate this approval"
                    )
                if not self.can_reinstate:
                    # if not self.status == 'suspended':
                    raise ValidationError("You cannot reinstate approval at this stage")
                today = timezone.now().date()
                if not self.can_reinstate and self.expiry_date >= today:
                    # if not self.status == 'suspended' and self.expiry_date >= today:
                    raise ValidationError("You cannot reinstate approval at this stage")
                if self.status == "cancelled":
                    self.cancellation_details = ""
                    self.cancellation_date = None
                if self.status == "surrendered":
                    self.surrender_details = {}
                if self.status == "suspended":
                    self.suspension_details = {}

                self.status = "current"
                # self.suspension_details = {}
                self.save()
                send_approval_reinstate_email_notification(self, request)
                # Log approval action
                self.log_user_action(
                    ApprovalUserAction.ACTION_REINSTATE_APPROVAL.format(self.id),
                    request,
                )
                # Log entry for proposal
                self.current_proposal.log_user_action(
                    ProposalUserAction.ACTION_REINSTATE_APPROVAL.format(
                        self.current_proposal.id
                    ),
                    request,
                )
            except:
                raise

    def approval_surrender(self, request, details):
        with transaction.atomic():
            try:
                if not request.user.leaseslicensing_organisations.filter(
                    organisation_id=self.applicant_id
                ):
                    if request.user not in self.allowed_assessors and not is_customer(
                        request
                    ):
                        raise ValidationError(
                            "You do not have access to surrender this approval"
                        )
                if not self.can_reissue and self.can_action:
                    raise ValidationError(
                        "You cannot surrender approval if it is not current or suspended"
                    )
                self.surrender_details = {
                    "surrender_date": details.get("surrender_date").strftime(
                        "%d/%m/%Y"
                    ),
                    "details": details.get("surrender_details"),
                }
                today = timezone.now().date()
                surrender_date = datetime.datetime.strptime(
                    self.surrender_details["surrender_date"], "%d/%m/%Y"
                )
                surrender_date = surrender_date.date()
                if surrender_date <= today:
                    if not self.status == "surrendered":
                        self.status = "surrendered"
                        self.set_to_surrender = False
                        self.save()
                        send_approval_surrender_email_notification(self)
                else:
                    self.set_to_surrender = True
                self.save()
                # Log approval action
                self.log_user_action(
                    ApprovalUserAction.ACTION_SURRENDER_APPROVAL.format(self.id),
                    request,
                )
                # Log entry for proposal
                self.current_proposal.log_user_action(
                    ProposalUserAction.ACTION_SURRENDER_APPROVAL.format(
                        self.current_proposal.id
                    ),
                    request,
                )
            except:
                raise

    @property
    def as_related_item(self):
        related_item = RelatedItem(
            identifier=self.related_item_identifier,
            model_name=self._meta.verbose_name,
            descriptor=self.related_item_descriptor,
            action_url='<a href=/internal/approval/{} target="_blank">Open</a>'.format(self.id)
        )
        return related_item

    @property
    def related_item_identifier(self):
        return self.lodgement_number

    @property
    def related_item_descriptor(self):
        return '(return descriptor)'


class PreviewTempApproval(Approval):
    class Meta:
        app_label = "leaseslicensing"
        # unique_together= ('lodgement_number', 'issue_date')


class ApprovalLogEntry(CommunicationsLogEntry):
    approval = models.ForeignKey(
        Approval, related_name="comms_logs", on_delete=models.CASCADE
    )

    class Meta:
        app_label = "leaseslicensing"

    def save(self, **kwargs):
        # save the application reference if the reference not provided
        if not self.reference:
            self.reference = self.approval.id
        super(ApprovalLogEntry, self).save(**kwargs)


class ApprovalLogDocument(Document):
    log_entry = models.ForeignKey(
        "ApprovalLogEntry",
        related_name="documents",
        null=True,
        on_delete=models.CASCADE,
    )
    _file = models.FileField(
        upload_to=update_approval_comms_log_filename, null=True, max_length=512
    )

    class Meta:
        app_label = "leaseslicensing"


class ApprovalUserAction(UserAction):
    ACTION_CREATE_APPROVAL = "Create licence {}"
    ACTION_UPDATE_APPROVAL = "Create licence {}"
    ACTION_EXPIRE_APPROVAL = "Expire licence {}"
    ACTION_CANCEL_APPROVAL = "Cancel licence {}"
    ACTION_EXTEND_APPROVAL = "Extend licence {}"
    ACTION_SUSPEND_APPROVAL = "Suspend licence {}"
    ACTION_REINSTATE_APPROVAL = "Reinstate licence {}"
    ACTION_SURRENDER_APPROVAL = "surrender licence {}"
    ACTION_RENEW_APPROVAL = "Create renewal Application for licence {}"
    ACTION_AMEND_APPROVAL = "Create amendment Application for licence {}"

    class Meta:
        app_label = "leaseslicensing"
        ordering = ("-when",)

    @classmethod
    def log_action(cls, approval, action, user):
        return cls.objects.create(approval=approval, who=user, what=str(action))

    approval = models.ForeignKey(
        Approval, related_name="action_logs", on_delete=models.CASCADE
    )


@receiver(pre_delete, sender=Approval)
def delete_documents(sender, instance, *args, **kwargs):
    for document in instance.documents.all():
        try:
            document.delete()
        except:
            pass
