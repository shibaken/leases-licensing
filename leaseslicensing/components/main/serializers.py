from rest_framework import serializers
from django.db.models import Sum, Max
from leaseslicensing.components.main.models import (
        CommunicationsLogEntry, 
        RequiredDocument, Question, GlobalSettings, ApplicationType,
        )
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from datetime import datetime, date
#from leaseslicensing.components.proposals.serializers import ProposalTypeSerializer

class CommunicationLogEntrySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=EmailUser.objects.all(),required=False)
    documents = serializers.SerializerMethodField()
    class Meta:
        model = CommunicationsLogEntry
        fields = (
            'id',
            'customer',
            'to',
            'fromm',
            'cc',
            'type',
            'reference',
            'subject'
            'text',
            'created',
            'staff',
            'proposal'
            'documents'
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]


class ApplicationTypeSerializer(serializers.ModelSerializer):
    #regions = RegionSerializer(many=True)
    #activity_app_types = ActivitySerializer(many=True)
    #tenure_app_types = TenureSerializer(many=True)
    class Meta:
        model = ApplicationType
        #fields = ('id', 'name', 'activity_app_types', 'tenure_app_types')
        #fields = ('id', 'name', 'tenure_app_types')
        fields = '__all__'
        #extra_fields = ['pizzas']


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = ('key', 'value')



class RequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = ('id', 'park','activity', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'answer_one', 'answer_two', 'answer_three', 'answer_four','correct_answer', 'correct_answer_value')


class BookingSettlementReportSerializer(serializers.Serializer):
    date = serializers.DateTimeField(input_formats=['%d/%m/%Y'])


class OracleSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=['%d/%m/%Y','%Y-%m-%d'])
    override = serializers.BooleanField(default=False)
