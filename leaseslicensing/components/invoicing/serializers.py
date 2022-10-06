from rest_framework import serializers

from leaseslicensing.components.invoicing.models import ChargeMethod, RepetitionType, InvoicingDetails, \
    FixedAnnualIncrementAmount, FixedAnnualIncrementPercentage, PercentageOfGrossTurnover, CrownLandRentReviewDate


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


class FixedAnnualIncrementAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = FixedAnnualIncrementAmount
        fields = (
            'id',
            'year',
            'increment_amount',
        )


class FixedAnnualIncrementPercentageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FixedAnnualIncrementPercentage
        fields = (
            'id',
            'year',
            'increment_percentage',
        )


class PercentageOfGrossTurnoverSerializer(serializers.ModelSerializer):

    class Meta:
        model = PercentageOfGrossTurnover
        fields = (
            'id',
            'year',
            'percentage',
        )


class CrownLandRentReviewDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrownLandRentReviewDate
        fields = (
            'id',
            'review_date',
        )


class InvoicingDetailsSerializer(serializers.ModelSerializer):
    charge_method = ChargeMethodSerializer()
    review_repetition_type = RepetitionTypeSerializer()
    invoicing_repetition_type = RepetitionTypeSerializer()
    annual_increment_amounts = FixedAnnualIncrementAmountSerializer(many=True)
    annual_increment_percentages = FixedAnnualIncrementPercentageSerializer(many=True)
    gross_turnover_percentages = PercentageOfGrossTurnoverSerializer(many=True)
    crown_land_rent_review_dates = CrownLandRentReviewDateSerializer(many=True)

    class Meta:
        model = InvoicingDetails
        fields = (
            'id',
            'charge_method',
            'base_fee_amount',
            'once_off_charge_amount',
            'review_once_every',
            'review_repetition_type',
            'invoicing_once_every',
            'invoicing_repetition_type',
            'annual_increment_amounts',
            'annual_increment_percentages',
            'gross_turnover_percentages',
            'crown_land_rent_review_dates',
        )