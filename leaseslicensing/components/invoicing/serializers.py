from rest_framework import serializers

from leaseslicensing.components.invoicing.models import ChargeMethod, RepetitionType, InvoicingDetails


class ChargeMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargeMethod
        fields = (
            'id',
            'key',
            'display_name',
        )


class RepetitionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepetitionType
        fields = (
            'id',
            'key',
            'display_name',
        )


class InvoicingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoicingDetails
        fields = (
            'id',
        )