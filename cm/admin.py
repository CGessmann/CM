__author__ = 'preuss'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from cm.models import *

admin.site.register(PaperType)
admin.site.register(Paper)
admin.site.register(Keyword)
admin.site.register(UserProfile)
admin.site.register(Configuration)
admin.site.register(AdditionalEmail)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)