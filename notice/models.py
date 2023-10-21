from django.utils.translation import gettext_lazy as _
from accounts.models import Profile, Admin, SuperAdmin, Faculty
from django.db import models


class AudienceChoices(models.TextChoices):
    STUDENT = 'STUDENT', _('Student')
    TEACHER = 'TEACHER', _('Teacher')
    ALUMNUS = 'ALUMNUS', _('Alumnus')
    STAFF = 'STAFF', _('Staff')
    ALL = 'ALL', _('All')

class Notice(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    attachment = models.FileField(upload_to='notice/%Y/%m/%d', blank=True)
    registry_date = models.DateField(auto_now_add=True)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    audience = models.CharField(max_length=20, choices=AudienceChoices.choices)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
