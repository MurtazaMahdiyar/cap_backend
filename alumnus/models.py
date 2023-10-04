from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Teacher, Class, Student
from django.utils.translation import gettext_lazy as _
from django.db import models
import datetime



class Job(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	company = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	position = models.CharField(max_length=254)
	description = models.TextField()

	start_date = models.DateField(default=datetime.date.today, blank=True)
	end_date = models.DateField(blank=True, null=True)

	class Meta:
		unique_together = ('student', 'title', 'start_date')

	def __str__(self):
		return self.title
	

class Scholarship(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	country = models.CharField(max_length=100)
	university = models.CharField(max_length=150)
	study_field = models.CharField(max_length=254)
	description = models.TextField()

	start_date = models.DateField(default=datetime.date.today)
	end_date = models.DateField(blank=True, null=True)

	class Meta:
		unique_together = ('student', 'start_date')

	def __str__(self):
		return self.study_field
	


class Subject(models.Model):
	subject_code = models.CharField(max_length=100)
	subject_name = models.CharField(max_length=150)
	number_of_credits = models.PositiveSmallIntegerField(default=1)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	subject_class = models.ForeignKey(Class, on_delete=models.CASCADE)
	semester = models.PositiveSmallIntegerField(default=1, validators=[
		MaxValueValidator(8),
		MinValueValidator(1),
	])

	class Meta:
		unique_together = ('subject_code', 'semester', 'subject_class')

	def __str__(self):
		return self.subject_code + ': ' + self.subject_name


class ResultSheet(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	mark = models.PositiveSmallIntegerField(validators=[
		MaxValueValidator(100),
		MinValueValidator(1),
	])

	class Meta:
		unique_together = ('student', 'subject', )

	def __str__(self):
		return str(self.mark)
