from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from ledger.accounts.models import EmailUser
from leaseslicensing.components.bookings.utils import create_monthly_invoice
from leaseslicensing.components.bookings.email import (
    send_monthly_invoices_failed_tclass,
)
import datetime

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the Monthly Invoices Script - generates invoices per licence/org_applicant for previous month"

    def handle(self, *args, **options):
        try:
            user = EmailUser.objects.get(email=settings.CRON_EMAIL)
        except:
            user = EmailUser.objects.create(email=settings.CRON_EMAIL, password="")

        logger.info("Running command {}".format(__name__))
        failed_bookings = create_monthly_invoice(user, offset_months=-1)

        if failed_bookings:
            # some invoices failed
            logger.info(
                "Command {} failed. Invoice failed to generate for booking IDs {}".format(
                    __name__, failed_bookings
                )
            )
            send_monthly_invoices_failed_tclass(failed_bookings)

        cmd_name = __name__.split(".")[-1].replace("_", " ").upper()
        err_str = (
            '<strong style="color: red;">Errors: {}</strong>'.format(
                len(failed_bookings)
            )
            if len(failed_bookings) > 0
            else '<strong style="color: green;">Errors: 0</strong>'
        )
        msg = "<p>{} completed. {}.</p>".format(cmd_name, err_str)
        logger.info(msg)
        print(msg)  # will redirect to cron_tasks.log file, by the parent script
