from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'registered', 'city', 'phone', 'email', 'activity']
    list_filter = ['activity']


admin.site.register(User, UserAdmin)
