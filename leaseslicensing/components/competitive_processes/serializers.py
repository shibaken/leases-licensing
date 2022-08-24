from rest_framework import serializers
from leaseslicensing.components.competitive_processes.models import CompetitiveProcess, CompetitiveProcessLogEntry, CompetitiveProcessParty, CompetitiveProcessUserAction
from leaseslicensing.ledger_api_utils import retrieve_email_user
from ..organisations.serializers import OrganisationSerializer
from leaseslicensing.components.proposals.models import Proposal
from leaseslicensing.components.main.serializers import CommunicationLogEntrySerializer, EmailUserSerializer
from leaseslicensing.components.users.serializers import UserSerializerSimple


class RegistrationOfInterestSerializer(serializers.ModelSerializer):
    relevant_applicant_name = serializers.CharField()
    
    class Meta:
        model = Proposal
        fields = (
            'id',
            'lodgement_number',
            'relevant_applicant_name',
        )


class CompetitiveProcessPartySerializer(serializers.ModelSerializer):
    is_person = serializers.BooleanField()  # This is property at the model
    is_organisation = serializers.BooleanField()  # This is property at the model
    person = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()

    class Meta:
        model = CompetitiveProcessParty
        fields = (
            'id',
            'is_person',
            'is_organisation',
            'person',
            'organisation',
            'invited_at',
            'removed_at',
        )

    def get_person(self, obj):
        if obj.is_person:
            serializer = EmailUserSerializer(obj.person)
            return serializer.data
        return None

    def get_organisation(self, obj):
        if obj.is_organisation:
            serializer = OrganisationSerializer(obj.organisation)
            return serializer.data
        return None


class CompetitiveProcessSerializerBase(serializers.ModelSerializer):
    registration_of_interest = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField()
    site = serializers.CharField()  # For property
    group = serializers.CharField()  # For property
    can_accessing_user_view = serializers.SerializerMethodField()
    can_accessing_user_process = serializers.SerializerMethodField()

    class Meta:
        model = CompetitiveProcess
        fields = (
            'id',
            'lodgement_number',
            'registration_of_interest',
            'status',
            'created_at',
            'assigned_officer',
            'site',
            'group',
            'can_accessing_user_view',
            'can_accessing_user_process',
        )
        # additional data to be returned for datatable
        # fields listed here should be listed 'fields' above, otherwise not returned
        datatables_always_serialize = (
            'group',
            'site',
            'can_accessing_user_view',
            'can_accessing_user_process',
        )

    def get_registration_of_interest(self, obj):
        if obj.generated_from_registration_of_interest:
            return RegistrationOfInterestSerializer(obj.generating_proposal).data
        else:
            return None

    def get_status(self, obj):
        return obj.get_status_display()  # https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display

    def get_assigned_officer(self, obj):
        if obj.is_assigned:
            return EmailUserSerializer(obj.assigned_officer).data
        else:
            return None

    def get_can_accessing_user_view(self, obj):
        try:
            user = self.context.get("request").user
            can_view = obj.can_user_view(user)
            return can_view
        except:
            return False

    def get_can_accessing_user_process(self, obj):
        try:
            user = self.context.get("request").user
            can_process = obj.can_user_process(user)
            return can_process
        except:
            return False


class ListCompetitiveProcessSerializer(CompetitiveProcessSerializerBase):

    class Meta:
        model = CompetitiveProcess
        fields = (
            'id',
            'lodgement_number',
            'registration_of_interest',
            'status',
            'created_at',
            'assigned_officer',
            'site',
            'group',
            'can_accessing_user_view',
            'can_accessing_user_process',
        )
        # additional data to be returned for datatable
        # fields listed here should be listed 'fields' above, otherwise not returned
        datatables_always_serialize = (
            'group',
            'site',
            'can_accessing_user_view',
            'can_accessing_user_process',
        )


class CompetitiveProcessSerializer(CompetitiveProcessSerializerBase):
    accessing_user = serializers.SerializerMethodField()
    competitive_process_parties = CompetitiveProcessPartySerializer(many=True)

    class Meta:
        model = CompetitiveProcess
        fields = (
            'id',
            'lodgement_number',
            'registration_of_interest',
            'status',
            'created_at',
            'assigned_officer',
            'site',
            'group',
            'can_accessing_user_view',
            'can_accessing_user_process',
            'accessing_user',
            'competitive_process_parties',
            'winner',
            'details',
        )

    def get_accessing_user(self, obj):
        user = self.context.get("request").user
        serializer = UserSerializerSimple(user)
        return serializer.data


class CompetitiveProcessLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = CompetitiveProcessLogEntry
        fields = "__all__"
        read_only_fields = ("customer",)

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class CompetitiveProcessUserActionSerializer(serializers.ModelSerializer):
    who = serializers.SerializerMethodField()

    class Meta:
        model = CompetitiveProcessUserAction
        fields = "__all__"

    def get_who(self, proposal_user_action):
        email_user = retrieve_email_user(proposal_user_action.who)
        fullname = email_user.get_full_name()
        #return fullname