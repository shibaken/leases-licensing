from __future__ import unicode_literals
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from django.conf import settings
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)

def retrieve_email_user(email_user_id):
    return EmailUser.objects.get(id=email_user_id)
