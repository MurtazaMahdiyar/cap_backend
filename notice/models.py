from django.utils.translation import gettext_lazy as _
from accounts.models import Teacher, Admin, SuperAdmin
from alumnus.models import Subject
from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    attachment = models.FileField(upload_to='notice/%Y/%m/%d', blank=True)
    registry_date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class AudienceChoices(models.TextChoices):
    STUDENT = 'STUDENT', _('Student')
    TEACHER = 'TEACHER', _('Teacher')
    ALUMNUS = 'ALUMNUS', _('Alumnus')
    STAFF = 'STAFF', _('Staff')


class AdminNotice(Notice):
    author = models.ForeignKey(Admin, on_delete=models.CASCADE)
    audience = models.CharField(max_length=20, choices=(('TEACHER', _('Teacher')), ('STUDENT', _('Student')), ('ALUMNUS', _('Alumnus')), ))


class SuperAdminNotice(Notice):
    author = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE)
    audience = models.CharField(max_length=20, choices=AudienceChoices.choices)
