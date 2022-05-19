from django.contrib import admin

from .models import TimeZone


class TimezoneAdmin(admin.ModelAdmin):

    list_filter = ('from_ist', 'to_ist', 'priority')
    list_display = ('name', 'from_ist', 'to_ist', 'priority')


admin.site.register(TimeZone, TimezoneAdmin)
