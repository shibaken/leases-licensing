from __future__ import unicode_literals
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

import logging
logger = logging.getLogger(__name__)


def retrieve_email_user(email_user_id):
        try:
            return EmailUser.objects.get(id=email_user_id)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


