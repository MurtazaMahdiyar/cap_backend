from django.contrib import admin
from .models import Complaint, ComplaintDocument

# Register your models here.
admin.site.register(Complaint)
admin.site.register(ComplaintDocument)