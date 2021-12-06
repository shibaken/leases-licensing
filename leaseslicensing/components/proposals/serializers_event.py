from django.conf import settings
from ledger.accounts.models import EmailUser,Address
from leaseslicensing.components.proposals.models import (
#                                    ProposalType,
#                                    Proposal,
#                                    ProposalUserAction,
#                                    ProposalLogEntry,
#                                    Referral,
#                                    ProposalRequirement,
#                                    ProposalStandardRequirement,
#                                    ProposalDeclinedDetails,
#                                    AmendmentRequest,
#                                    AmendmentReason,
#                                    ProposalApplicantDetails,
#                                    ProposalActivitiesLand,
#                                    ProposalActivitiesMarine,
#                                    ProposalPark,
#                                    ProposalParkActivity,
#                                    Vehicle,
#                                    Vessel,
#                                    ProposalTrail,
#                                    QAOfficerReferral,
#                                    ProposalParkAccess,
#                                    ProposalTrailSection,
#                                    ProposalTrailSectionActivity,
#                                    ProposalParkZoneActivity,
#                                    ProposalParkZone,
#                                    ProposalAccreditation,
#                                    ChecklistQuestion,
#                                    ProposalAssessmentAnswer,
#                                    ProposalAssessment,
#                                    RequirementDocument,
#                                    ProposalOtherDetails,
                                    ProposalEventActivities,
                                    ProposalEventManagement,
                                    ProposalEventVehiclesVessels,
                                    ProposalEventOtherDetails,
                                    ProposalEventsParks,
                                    EventsParkDocument,
                                    AbseilingClimbingActivity,
                                    PreEventsParkDocument,
                                    ProposalPreEventsParks,
                                    ProposalEventsTrails,
                                    #ProposalEventOnlineTraining,
                                )
from leaseslicensing.components.main.serializers import CommunicationLogEntrySerializer, ParkFilterSerializer, TrailSerializer, SectionSerializer
from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version


class ProposalEventActivitiesSerializer(serializers.ModelSerializer):
    commencement_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    completion_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    max_num_months_ahead = serializers.SerializerMethodField()
    last_event_application_fee_date = serializers.SerializerMethodField()

    class Meta:
        model = ProposalEventActivities
        #fields = '__all__'
        fields=(
                'id',
                'event_name',
                'proposal',
                'commencement_date',
                'completion_date',
                'event_date',
                'pdswa_location',
                #'can_occur',
                'max_num_months_ahead',
                'last_event_application_fee_date',
        )

    def get_max_num_months_ahead(self, obj):
        return obj.proposal.org_applicant.max_num_months_ahead

    def get_last_event_application_fee_date(self, obj):
        try:
            return obj.proposal.org_applicant.last_event_application_fee_date.strftime('%d/%m/%Y')
        except:
            return None

class ProposalEventManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalEventManagement
        fields = '__all__'


class ProposalEventVehiclesVesselsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalEventVehiclesVessels
        fields = '__all__'


class ProposalEventOtherDetailsSerializer(serializers.ModelSerializer):
    insurance_expiry = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    training_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)

    class Meta:
        model = ProposalEventOtherDetails
        #fields = '__all__'
        fields=(
                'id',
                'insurance_expiry',
                'training_date',
                'participants_number',
                'officials_number',
                'support_vehicle_number',
                'other_comments',
                'proposal',
                )

class EventsParkDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsParkDocument
        fields = ('id', 'name', '_file')

class ProposalEventsParksSerializer(serializers.ModelSerializer):
    park=ParkFilterSerializer()
    #activities=serializers.CharField(source='activities.name', many=True)
    activities_assessor_names=serializers.SerializerMethodField()
    events_park_documents = EventsParkDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ProposalEventsParks
        fields = ('id', 'park','event_activities',  'proposal', 'events_park_documents', 'activities_assessor', 'activities_assessor_names')

    def get_activities_assessor_names(self,obj):
        return [a.name for a in obj.activities_assessor.all() ] if obj.activities_assessor else None

class SaveProposalEventsParksSerializer(serializers.ModelSerializer):
    #park=ParkFilterSerializer()
    class Meta:
        model = ProposalEventsParks
        fields = ('id', 'park','proposal', 'event_activities', 'activities_assessor')

class AbseilingClimbingActivitySerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    class Meta:
        model = AbseilingClimbingActivity
        fields = '__all__'


class PreEventsParkDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreEventsParkDocument
        fields = ('id', 'name', '_file')

class ProposalPreEventsParksSerializer(serializers.ModelSerializer):
    park=ParkFilterSerializer()
    #activities=serializers.CharField(source='activities.name', many=True)
    pre_event_park_documents = PreEventsParkDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ProposalPreEventsParks
        fields = ('id', 'park', 'activities', 'pre_event_park_documents', 'proposal')

class SaveProposalPreEventsParksSerializer(serializers.ModelSerializer):
    #park=ParkFilterSerializer()
    class Meta:
        model = ProposalPreEventsParks
        fields = ('id', 'park','proposal', 'activities')

class ProposalEventsTrailsSerializer(serializers.ModelSerializer):
    trail=TrailSerializer()
    section=SectionSerializer()
    activities_assessor_names=serializers.SerializerMethodField()
    class Meta:
        model = ProposalEventsTrails
        fields = ('id', 'trail','section',  'proposal', 'event_trail_activities', 'activities_assessor', 'activities_assessor_names')

    def get_activities_assessor_names(self,obj):
        return [a.name for a in obj.activities_assessor.all() ] if obj.activities_assessor else None

class SaveProposalEventsTrailsSerializer(serializers.ModelSerializer):
    #park=ParkFilterSerializer()
    class Meta:
        model = ProposalEventsTrails
        fields = ('id', 'trail','proposal','section', 'event_trail_activities', 'activities_assessor')
