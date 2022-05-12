from django.db.models.signals import post_delete, pre_save, post_save, m2m_changed
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from leaseslicensing.components.proposals.models import Referral, Proposal

import logging

logger = logging.getLogger(__name__)


class ReferralListener(object):
    """
    Event listener for Referral
    """

    @staticmethod
    @receiver(pre_save, sender=Referral)
    def _pre_save(sender, instance, **kwargs):
        if instance.pk:
            original_instance = Referral.objects.get(pk=instance.pk)
            setattr(instance, "_original_instance", original_instance)

        elif hasattr(instance, "_original_instance"):
            delattr(instance, "_original_instance")

    @staticmethod
    @receiver(post_save, sender=Referral)
    def _post_save(sender, instance, **kwargs):
        original_instance = (
            getattr(instance, "_original_instance")
            if hasattr(instance, "_original_instance")
            else None
        )
        if original_instance:
            # Check if the proposal attached to the referral outstanding referrals
            outstanding = instance.proposal.referrals.filter(
                processing_status=Referral.PROCESSING_STATUS_WITH_REFERRAL
            )
            if len(outstanding) == 0:
                instance.proposal.processing_status = (
                    Proposal.PROCESSING_STATUS_WITH_ASSESSOR
                )
                instance.proposal.save()
