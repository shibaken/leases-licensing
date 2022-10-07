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
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }


class FixedAnnualIncrementPercentageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FixedAnnualIncrementPercentage
        fields = (
            'id',
            'year',
            'increment_percentage',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }


class PercentageOfGrossTurnoverSerializer(serializers.ModelSerializer):

    class Meta:
        model = PercentageOfGrossTurnover
        fields = (
            'id',
            'year',
            'percentage',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }


class CrownLandRentReviewDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrownLandRentReviewDate
        fields = (
            'id',
            'review_date',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }


class InvoicingDetailsSerializer(serializers.ModelSerializer):
    annual_increment_amounts = FixedAnnualIncrementAmountSerializer(many=True, required=False)
    annual_increment_percentages = FixedAnnualIncrementPercentageSerializer(many=True, required=False)
    gross_turnover_percentages = PercentageOfGrossTurnoverSerializer(many=True, required=False)
    crown_land_rent_review_dates = CrownLandRentReviewDateSerializer(many=True, required=False)

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

    def update(self, instance, validated_data):
        # Update nested serializers
        annual_increment_amounts_data = validated_data.pop('annual_increment_amounts')
        annual_increment_percentages_data = validated_data.pop('annual_increment_percentages')
        gross_turnover_percentages_data = validated_data.pop('gross_turnover_percentages')
        crown_land_rent_review_dates_data = validated_data.pop('crown_land_rent_review_dates')

        serializer = InvoicingDetailsSerializer(instance, data=validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.update_annual_increment_amounts(annual_increment_amounts_data, instance)
        self.update_annual_increment_percentages(annual_increment_percentages_data, instance)
        self.update_gross_turnover_percentages(gross_turnover_percentages_data, instance)
        self.update_crown_land_rent_review_dates(crown_land_rent_review_dates_data, instance)

        # TODO: Do we allow to delete the existing items...?

        return instance

    def update_annual_increment_amounts(self, annual_increment_amounts_data, instance):
        for annual_increment_amount_data in annual_increment_amounts_data:
            if annual_increment_amount_data.get('id', 0):
                # Existing
                annual_increment_amount = FixedAnnualIncrementAmount.objects.get(id=int(annual_increment_amount_data.get('id')))
                serializer = FixedAnnualIncrementAmountSerializer(
                    annual_increment_amount, annual_increment_amount_data, context={'invoicing_details': instance}
                    )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                # New
                if 'id' in annual_increment_amount_data:
                    annual_increment_amount_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = FixedAnnualIncrementAmountSerializer(data=annual_increment_amount_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()

    def update_annual_increment_percentages(self, annual_increment_percentages_data, instance):
        for annual_increment_percentage_data in annual_increment_percentages_data:
            if annual_increment_percentage_data.get('id', 0):
                # Existing
                annual_increment_percentage = FixedAnnualIncrementPercentage.objects.get(id=int(annual_increment_percentage_data.get('id')))
                serializer = FixedAnnualIncrementPercentageSerializer(
                    annual_increment_percentage, annual_increment_percentage_data, context={'invoicing_details': instance}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                # New
                if 'id' in annual_increment_percentage_data:
                    annual_increment_percentage_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = FixedAnnualIncrementPercentageSerializer(data=annual_increment_percentage_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()

    def update_gross_turnover_percentages(self, gross_turnover_percentages_data, instance):
        for gross_turnover_percentage_data in gross_turnover_percentages_data:
            if gross_turnover_percentage_data.get('id', 0):
                # Existing
                gross_turnover_percentage = PercentageOfGrossTurnover.objects.get(id=int(gross_turnover_percentage_data.get('id')))
                serializer = PercentageOfGrossTurnoverSerializer(
                    gross_turnover_percentage, gross_turnover_percentage_data, context={'invoicing_details': instance}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                # New
                if 'id' in gross_turnover_percentage_data:
                    gross_turnover_percentage_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = PercentageOfGrossTurnoverSerializer(data=gross_turnover_percentage_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()

    def update_crown_land_rent_review_dates(self, crown_land_rent_review_dates_date, instance):
        pass

