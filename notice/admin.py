from django.contrib import admin
from .models import AdminNotice, SuperAdminNotice
# Register your models here.

admin.site.register(AdminNotice)
admin.site.register(SuperAdminNotice)