from django.db import models


class ChargeMethod(models.Model):
    """A class to represent a competitive process"""

    display_name = models.CharField(max_length=200, unique=True)

    class Meta:
        app_label = "leaseslicensing"

    def __str__(self):
        return self.display_name
