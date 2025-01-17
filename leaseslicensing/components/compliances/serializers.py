from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from leaseslicensing.components.compliances.models import (
    Compliance,
    ComplianceUserAction,
    ComplianceLogEntry,
    ComplianceAmendmentRequest,
    ComplianceAmendmentReason,
)
from rest_framework import serializers

from leaseslicensing.ledger_api_utils import retrieve_email_user
from leaseslicensing.components.main.serializers import EmailUserSerializer


class ComplianceSerializer(serializers.ModelSerializer):
    #regions = serializers.CharField(source="proposal.region")
    #activity = serializers.CharField(source="proposal.activity")
    title = serializers.CharField(source="proposal.title")
    holder = serializers.CharField(source="proposal.applicant")
    processing_status = serializers.CharField(source="get_processing_status_display")
    customer_status = serializers.CharField(source="get_customer_status_display")
    submitter = serializers.SerializerMethodField(read_only=True)
    documents = serializers.SerializerMethodField()
    # submitter = serializers.CharField(source='submitter.get_full_name')
    submitter = serializers.SerializerMethodField(read_only=True)
    allowed_assessors = serializers.SerializerMethodField(read_only=True)
    #allowed_assessors = EmailUserSerializer(many=True)
    # assigned_to = serializers.CharField(source='assigned_to.get_full_name')
    assigned_to = serializers.SerializerMethodField(read_only=True)
    requirement = serializers.CharField(
        source="requirement.requirement", required=False, allow_null=True
    )
    approval_lodgement_number = serializers.SerializerMethodField()
    application_type = serializers.SerializerMethodField(read_only=True)
    due_date = serializers.SerializerMethodField(read_only=True)
    lodgement_date_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Compliance
        fields = (
            "id",
            "proposal",
            "due_date",
            "processing_status",
            "customer_status",
            #"regions",
            #"activity",
            "title",
            "text",
            "holder",
            "assigned_to",
            "approval",
            "documents",
            "requirement",
            "can_user_view",
            "can_process",
            "reference",
            "lodgement_number",
            "lodgement_date",
            "submitter",
            "allowed_assessors",
            "lodgement_date",
            "approval_lodgement_number",
            "num_participants",
            "participant_number_required",
            "fee_invoice_reference",
            "fee_paid",
            "application_type",
            "lodgement_date_display",
        )
        datatables_always_serialize = (
            "id",
            "proposal",
            "due_date",
            "processing_status",
            "customer_status",
            #"regions",
            #"activity",
            "title",
            "text",
            "holder",
            "assigned_to",
            "approval",
            "documents",
            "requirement",
            "can_user_view",
            "can_process",
            "reference",
            "lodgement_number",
            "lodgement_date",
            "submitter",
            "allowed_assessors",
            "lodgement_date",
            "approval_lodgement_number",
            "num_participants",
            "participant_number_required",
            "fee_invoice_reference",
            "fee_paid",
            "application_type",
        )

    def get_due_date(self, obj):
        return obj.due_date.strftime("%d/%m/%Y") if obj.due_date else ""

    def get_allowed_assessors(self, obj):
        if obj.allowed_assessors:
            email_users = []
            for user in obj.allowed_assessors:
                email_users.append(retrieve_email_user(user))
            return EmailUserSerializer(email_users, many=True).data
        else:
            return ""

    def get_documents(self, obj):
        return [[d.name, d._file.url, d.can_delete, d.id] for d in obj.documents.all()]

    def get_approval_lodgement_number(self, obj):
        return obj.approval.lodgement_number

    def get_assigned_to(self, obj):
        if obj.assigned_to:
            return retrieve_email_user(obj.assigned_to).get_full_name()
        return None

    def get_submitter(self, obj):
        if obj.submitter:
            return retrieve_email_user(obj.submitter).get_full_name()
        return None

    def get_application_type(self, obj):
        if obj.proposal.application_type:
            return obj.proposal.application_type.name
        return None

    def get_lodgement_date_display(self, obj):
        if obj.lodgement_date:
            return obj.lodgement_date.strftime("%d/%m/%Y %I:%M %p")

class InternalComplianceSerializer(serializers.ModelSerializer):
    #regions = serializers.CharField(source="proposal.region")
    #activity = serializers.CharField(source="proposal.activity")
    title = serializers.CharField(source="proposal.title")
    holder = serializers.CharField(source="proposal.applicant")
    processing_status = serializers.CharField(source="get_processing_status_display")
    customer_status = serializers.CharField(source="get_customer_status_display")
    submitter = serializers.SerializerMethodField(read_only=True)
    documents = serializers.SerializerMethodField()
    # submitter = serializers.CharField(source='submitter.get_full_name')
    submitter = serializers.SerializerMethodField(read_only=True)
    #allowed_assessors = EmailUserSerializer(many=True)
    allowed_assessors = serializers.SerializerMethodField(read_only=True)
    # assigned_to = serializers.CharField(source='assigned_to.get_full_name')
    # assigned_to = serializers.SerializerMethodField(read_only=True)
    requirement = serializers.CharField(
        source="requirement.requirement", required=False, allow_null=True
    )
    approval_lodgement_number = serializers.SerializerMethodField()
    lodgement_date = serializers.SerializerMethodField()

    class Meta:
        model = Compliance
        fields = (
            "id",
            "proposal",
            "due_date",
            "processing_status",
            "customer_status",
            #"regions",
            #"activity",
            "title",
            "text",
            "holder",
            "assigned_to",
            "approval",
            "documents",
            "requirement",
            "can_user_view",
            "can_process",
            "reference",
            "lodgement_number",
            "lodgement_date",
            "submitter",
            "allowed_assessors",
            "lodgement_date",
            "approval_lodgement_number",
            "participant_number_required",
            "num_participants",
            "fee_invoice_reference",
            "fee_paid",
        )

    def get_allowed_assessors(self, obj):
        if obj.allowed_assessors:
            email_users = []
            for user in obj.allowed_assessors:
                email_users.append(retrieve_email_user(user))
            return EmailUserSerializer(email_users, many=True).data
        else:
            return ""
    
    def get_lodgement_date(self, obj):
        return obj.lodgement_date.strftime("%d/%m/%Y") if obj.lodgement_date else ""

    def get_documents(self, obj):
        return [[d.name, d._file.url, d.can_delete, d.id] for d in obj.documents.all()]

    def get_approval_lodgement_number(self, obj):
        return obj.approval.lodgement_number

    # def get_assigned_to(self,obj):
    #     if obj.assigned_to:
    #         return obj.assigned_to.get_full_name()
    #     return None

    def get_submitter(self, obj):
        if obj.submitter:
            return retrieve_email_user(obj.submitter).get_full_name()
        return None


class SaveComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliance
        fields = (
            "id",
            "title",
            "text",
            "num_participants",
        )


class ComplianceActionSerializer(serializers.ModelSerializer):
    #who = serializers.CharField(source="who.get_full_name")
    who = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceUserAction
        fields = "__all__"

    def get_who(self, obj):
        user = retrieve_email_user(obj.id)
        #return user.first_name + " " + user.last_name
        return "{} {}".format(user.first_name, user.last_name)

class ComplianceCommsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceLogEntry
        fields = "__all__"

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class ComplianceAmendmentRequestSerializer(serializers.ModelSerializer):
    # reason = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceAmendmentRequest
        fields = "__all__"

    # def get_reason (self,obj):
    #     return obj.get_reason_display()


class CompAmendmentRequestDisplaySerializer(serializers.ModelSerializer):
    reason = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceAmendmentRequest
        fields = "__all__"

    def get_reason(self, obj):
        # return obj.get_reason_display()
        return obj.reason.reason if obj.reason else None
