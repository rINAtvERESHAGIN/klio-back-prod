from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from .models import Article, Banner, CallbackInfo, Menu, MenuItem, News, Page, SiteSettings, SubscriberInfo


admin.site.site_header = _('Klio Site Administration')


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'start_date', 'deadline', 'activity']
    list_editable = ['activity']
    prepopulated_fields = {"slug": ("title",)}


class BannerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'deadline', 'link', 'order', 'activity']
    list_editable = ['order', 'activity']
    list_filter = ['activity']


class CallBackInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'name', 'phone', 'comment']


class MenuItemAdmin(admin.ModelAdmin):
    search_fields = ['name']


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ['parent']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'position', 'get_items', 'activity']
    list_editable = ['activity']
    list_filter = ['position', 'activity']
    inlines = [
        MenuItemInline,
    ]
    save_on_top = True

    def get_items(self, obj):
        return ', '.join([item.name for item in obj.items.filter(activity=True, parent__isnull=True)])
    get_items.short_description = 'Items'
    get_items.admin_order_field = 'item__order'


class NewsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'start_date', 'deadline', 'activity']
    list_editable = ['activity']
    prepopulated_fields = {"slug": ("title",)}


class PageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'modified', 'activity']
    list_editable = ['activity']
    prepopulated_fields = {"slug": ("name",)}


class SiteSettingsInline(admin.StackedInline):
    model = SiteSettings


class SiteAdmin(BaseSiteAdmin):
    inlines = (SiteSettingsInline,)


class SubscriberInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'email']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(CallbackInfo, HiddenAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Page, PageAdmin)
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(SubscriberInfo, SubscriberInfoAdmin)
