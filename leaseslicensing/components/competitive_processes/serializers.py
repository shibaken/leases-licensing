from rest_framework import serializers
from leaseslicensing.components.competitive_processes.models import CompetitiveProcess


class ListCompetitiveProcessSerializer(serializers.ModelSerializer):
    registration_of_interest = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CompetitiveProcess
        fields = (
            'id',
            'lodgement_number',
            'registration_of_interest',
            'status',
            'created_at',
        )

    def get_registration_of_interest(self, obj):
        if obj.registration_of_interest:
            return {
                'id': obj.registration_of_interest.id,
                'lodgement_number': obj.registration_of_interest.lodgement_number,
            }
        else:
            return ''
    
    def get_status(self, obj):
        return obj.get_status_display()  # https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display