from django.contrib.gis import admin
from leaseslicensing.components.main import models
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.db.models import Q

#from ledger.accounts.models import EmailUser
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from django.http import HttpResponse

from copy import deepcopy

admin.site.index_template = 'admin-index.html'
admin.autodiscover()

@admin.register(models.EmailUser)
class EmailUserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name','is_staff','is_active',)
    ordering = ('email',)
    search_fields = ('id','email','first_name','last_name')

    def has_change_permission(self, request, obj=None):
        if obj is None: # and obj.status > 1:
            return True
        return None 
    def has_delete_permission(self, request, obj=None):
        return None



from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.conf import settings
#
#from ledger.accounts import admin as ledger_admin
##from ledger.accounts.models import EmailUser, Document, Address, Profile
#from ledger.accounts.models import EmailUser
#from copy import deepcopy
#
#
class LeasesLicensingAdminSite(AdminSite):
    site_header = 'Commercial Operator Administration'
    site_title = 'Commercial Operator Licensing'
    index_title = 'Commercial Operator Licensing'

leaseslicensing_admin_site = LeasesLicensingAdminSite(name='leaseslicensingadmin')
#
#admin.site.unregister(EmailUser) # because this base classAdmin alsready registered in ledger.accounts.admin
#@admin.register(EmailUser)
#class EmailUserAdmin(ledger_admin.EmailUserAdmin):
#    """
#    Overriding the EmailUserAdmin from ledger.accounts.admin, to remove is_superuser checkbox field on Admin page
#    """
#
#    def get_fieldsets(self, request, obj=None):
#        """ Remove the is_superuser checkbox from the Admin page, if user is LeasesLicensingAdmin and NOT superuser """
#        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
#        #if not obj:
#        #    return fieldsets
#
#        if request.user.is_superuser:
#            return fieldsets
#
#        # User is not a superuser, remove is_superuser checkbox
#        fieldsets = deepcopy(fieldsets)
#        for fieldset in fieldsets:
#            if 'is_superuser' in fieldset[1]['fields']:
#                if type(fieldset[1]['fields']) == tuple :
#                    fieldset[1]['fields'] = list(fieldset[1]['fields'])
#                fieldset[1]['fields'].remove('is_superuser')
#                break
#
#        return fieldsets


