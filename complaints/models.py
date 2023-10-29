from django.utils.translation import gettext_lazy as _
from accounts.models import Profile, Faculty
from django.db import models


class Complaint(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='complaint', null=True)
    title = models.CharField(max_length=254)
    description = models.TextField()

    class ComplaintStatus(models.TextChoices):
        RECEIVED = 'RECEIVED', _('Received')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        REJECTED = 'REJECTED', _('Rejected')

    class ComplaintTarget(models.TextChoices):
        STUDENT = 'STUDENT', _('Student')
        TEACHER = 'TEACHER', _('Teacher')
        STAFF = 'STAFF', _('Staff')

    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default=ComplaintStatus.RECEIVED)
    comment = models.CharField(max_length=254, default="Your complaint received! thank you.")
    complaint_against = models.CharField(max_length=20, choices=ComplaintTarget.choices)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=1)
    attachment = models.FileField(upload_to='attachment/%Y/%m/%d', blank=True)
    private = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
