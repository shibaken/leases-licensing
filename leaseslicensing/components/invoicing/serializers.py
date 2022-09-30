from rest_framework import serializers

from leaseslicensing.components.invoicing.models import ChargeMethod


class ChargeMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargeMethod
        fields = (
            'id',
            'key',
            'display_name',
        )
