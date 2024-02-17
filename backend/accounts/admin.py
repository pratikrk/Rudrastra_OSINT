from django.contrib import admin
from .models import PhoneNumber
from .models import RequestLog
# Register your models here.
admin.site.register(PhoneNumber)

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('url', 'method', 'ip_address', 'timestamp')
    search_fields = ('url', 'ip_address')
    list_filter = ('method', 'timestamp')