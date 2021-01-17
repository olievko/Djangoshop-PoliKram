from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage, Language, SettingLang


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'subject', 'update_at', 'status']
    readonly_fields = ('contact_name', 'subject', 'email', 'comment')
    list_filter = ['status']


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'status']
    list_filter = ['status']


class SettingLangAdmin(admin.ModelAdmin):
    list_display = ['title', 'keywords', 'description', 'lang']
    list_filter = ['lang']


admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingLang, SettingLangAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Language, LanguagesAdmin)
