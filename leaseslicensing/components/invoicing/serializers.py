from rest_framework import serializers

from leaseslicensing import settings
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
            'charge_method',                    # FK
            'base_fee_amount',
            'once_off_charge_amount',
            'review_once_every',
            'review_repetition_type',           # FK
            'invoicing_once_every',
            'invoicing_repetition_type',        # FK
            'annual_increment_amounts',         # ReverseFK
            'annual_increment_percentages',     # ReverseFK
            'gross_turnover_percentages',       # ReverseFK
            'crown_land_rent_review_dates',     # ReverseFK
        )

    def validate(self, attrs):
        action = self.context.get('action')

        # TODO: conditional based on viewset.action?
        if action == 'finance_save':
            # When "Save and Continue"/"Save and Exit" button clicked
            pass
        elif action == 'finance_complete_editing':
            # When "Complete Editing" clicked
            charge_method = attrs.get('charge_method')

            if charge_method.key == settings.CHARGE_METHOD_ONCE_OFF_CHARGE:
                attrs['base_fee_amount'] = None
                attrs['review_once_every'] = None
                attrs['review_repetition_type'] = None
                attrs['invoicing_once_every'] = None
                attrs['invoicing_repetition_type'] = None
                attrs['annual_increment_amounts'] = None
                attrs['annual_increment_percentages'] = None
                attrs['gross_turnover_percentages'] = None
                attrs['crown_land_rent_review_dates'] = None
            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_INCREMENT:
                pass
            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_PERCENTAGE:
                pass
            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI:
                pass
            elif charge_method.key == settings.CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER:
                pass
            elif charge_method.key == settings.CHARGE_METHOD_NO_RENT_OR_LICENCE_CHARGE:
                pass

        return attrs

    def update(self, instance, validated_data):
        # Local fields
        instance.base_fee_amount = validated_data.get('base_fee_amount', instance.base_fee_amount)
        instance.once_off_charge_amount = validated_data.get('once_off_charge_amount', instance.once_off_charge_amount)
        instance.review_once_every = validated_data.get('review_once_every', instance.review_once_every)
        instance.invoicing_once_every = validated_data.get('invoicing_once_every', instance.invoicing_once_every)

        # FK fields
        instance.charge_method = validated_data.get('charge_method', instance.charge_method)
        instance.review_repetition_type = validated_data.get('review_repetition_type', instance.review_repetition_type)
        instance.invoicing_repetition_type = validated_data.get('invoicing_repetition_type', instance.invoicing_repetition_type)

        # Update local and FK fields
        instance.save()

        # Reverse FKs
        annual_increment_amounts_data = validated_data.pop('annual_increment_amounts')
        annual_increment_percentages_data = validated_data.pop('annual_increment_percentages')
        gross_turnover_percentages_data = validated_data.pop('gross_turnover_percentages')
        crown_land_rent_review_dates_data = validated_data.pop('crown_land_rent_review_dates')
        self.update_annual_increment_amounts(annual_increment_amounts_data, instance)
        self.update_annual_increment_percentages(annual_increment_percentages_data, instance)
        self.update_gross_turnover_percentages(gross_turnover_percentages_data, instance)
        self.update_crown_land_rent_review_dates(crown_land_rent_review_dates_data, instance)

        # TODO: Do we allow to delete the existing items if it's allowed...?

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

    def update_crown_land_rent_review_dates(self, crown_land_rent_review_dates_data, instance):
        for crown_land_rent_review_date_data in crown_land_rent_review_dates_data:
            if crown_land_rent_review_date_data.get('id', 0):
                # Existing
                crown_land_rent_review_date = CrownLandRentReviewDate.objects.get(id=int(crown_land_rent_review_date_data.get('id')))
                serializer = CrownLandRentReviewDateSerializer(
                    crown_land_rent_review_date, crown_land_rent_review_date_data, context={'invoicing_details': instance}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                # New
                if 'id' in crown_land_rent_review_date_data:
                    crown_land_rent_review_date_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = CrownLandRentReviewDateSerializer(data=crown_land_rent_review_date_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()


