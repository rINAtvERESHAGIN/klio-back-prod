from django.contrib import admin

from .models import Contact, ContactPhone, Phone, SocialNet, WorkingHours


class ContactPhoneInline(admin.TabularInline):
    model = ContactPhone


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours


class ContactAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['__str__', 'slug', 'city', 'email', 'get_phones', 'order', 'activity']
    list_editable = ['order', 'activity']
    inlines = [
        ContactPhoneInline,
        WorkingHoursInline
    ]

    def get_phones(self, obj):
        return "; ".join([phone.__str__() for phone in obj.phones.filter(activity=True)])


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_contacts', 'activity']
    list_editable = ['activity']
    list_filter = ['activity']

    def get_contacts(self, obj):
        return ", ".join(
            [contact.name for contact in obj.contacts.all()] + [user.__str__() for user in obj.users.filter(
                activity=True)]
        )


class SocialNetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'url', 'order', 'activity']
    list_editable = ['order', 'activity']
    list_filter = ['activity']


admin.site.register(Contact, ContactAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(SocialNet, SocialNetAdmin)
