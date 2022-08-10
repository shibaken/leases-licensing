from rest_framework import serializers
from leaseslicensing.components.competitive_processes.models import CompetitiveProcess
from leaseslicensing.components.proposals.models import Proposal
from leaseslicensing.components.main.serializers import EmailUserSerializer


class RegistrationOfInterestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Proposal
        fields = (
            'id',
            'lodgement_number'
        )


class ListCompetitiveProcessSerializer(serializers.ModelSerializer):
    registration_of_interest = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField()
    site = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()

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
            'action',
        )

    def get_registration_of_interest(self, obj):
        if obj.generated_from_registration_of_interest:
            return RegistrationOfInterestSerializer(obj.registration_of_interest).data
        else:
            return ''
    
    def get_status(self, obj):
        return obj.get_status_display()  # https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display

    def get_assigned_officer(self, obj):
        if obj.is_assigned:
            return EmailUserSerializer(obj.assigned_officer).data
        else:
            return ''

    def get_site(self, obj):
        return '(TODO: site)'

    def get_group(self, obj):
        return '(TODO: group)'

    def get_action(self, obj):
        request = self.context.get("request")
        user = request.user
        can_view = obj.can_user_view(user)
        can_process = obj.can_user_process(user)
        return {
            'can_view': can_view,
            'can_process': can_process
        }
