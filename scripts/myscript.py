import os
import sys
import django

proj_path = "/var/www/leaseslicensing"
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leaseslicensing.settings")
django.setup()


from leaseslicensing.components.proposals.models import Proposal

p = Proposal.objects.last()

print(p.__dict__)
