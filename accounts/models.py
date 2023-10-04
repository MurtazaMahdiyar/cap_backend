from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.db import models
import datetime


class ProfileManager(BaseUserManager):
	
	def create_user(self, first_name: str, last_name: str, email: str, password: str = None, is_staff = False, is_superuser = False) -> 'Profile':
		if not email:
			raise ValueError('User must have an email')
		
		if not first_name:
			raise ValueError('User must have a first name')

		if not last_name:
			raise ValueError('User must have a last name')
		
		profile = self.model(email = self.normalize_email(email))
		profile.first_name = first_name
		profile.last_name = last_name
		profile.set_password(password)
		profile.is_active = True
		profile.is_staff = is_staff
		profile.is_superuser = is_superuser
		profile.save()

		return profile


	def create_superuser(self, first_name: str, last_name: str, email: str, password: str) -> 'Profile':
		profile = self.create_user(
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password,
			is_staff=True,
			is_superuser=True
		)

		profile.save()

		return profile


class ProfileType(models.TextChoices):
	STUDENT = 'STUDENT', _('Student')
	TEACHER = 'TEACHER', _('Teacher')
	ADMIN = 'ADMIN', _('Admin')
	SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')



class Profile(AbstractUser):
	first_name = models.CharField(verbose_name='First name', max_length=255)
	last_name = models.CharField(verbose_name='Last name', max_length=255)
	email = models.CharField(verbose_name='Email', max_length=255, unique=True)
	password = models.CharField(max_length=255)
	username = None
	profile_type = models.CharField(max_length=50, choices=ProfileType.choices, default='')

	class GenderChoices(models.TextChoices):
		MALE = 'MALE', _('Male')
		FEMALE = 'FEMALE', _('Female')

	gender = models.CharField(max_length=15, choices=GenderChoices.choices, default=GenderChoices.MALE)
	date_of_birth = models.DateField(default=datetime.date.today)
	personal_photo = models.ImageField(upload_to='image/profile/%Y/%m/%d', blank=True)
	phone = models.CharField(max_length=15, unique=True)

	objects = ProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	class Meta:
		verbose_name = 'Profile'


class Faculty(models.Model):
	name = models.CharField(max_length=254)

	def __str__(self):
		return self.name


class Department(models.Model):
	name = models.CharField(max_length=100, default='')
	faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

	def __str__(self):
		return self.name



class Class(models.Model):
	name = models.CharField(max_length=150)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	year = models.CharField(max_length=4, default=datetime.datetime.now().year, blank=True)

	class Meta:
		verbose_name = 'Class'
		verbose_name_plural = 'Classes'
		unique_together = ('name', 'department', 'year')

	def __str__(self):
		return self.year + '-' + self.name + '-' + str(self.department)



class Student(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, default=1, related_name="student")

	university_id = models.CharField(max_length=50, unique=True)
	father_name = models.CharField(max_length=100)
	student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
	university_id_photo = models.ImageField(upload_to='image/university_id/%Y/%m/%d', blank=True)
	graduated = models.BooleanField(default=False)

	class student_status(models.TextChoices):
		JOBLESS = 'JOBLESS', _('Jobless')
		JOB = 'JOB', _('Job')
		SCHOLARSHIP = 'SCHOLARSHIP', _('Scholarship') 

	status = models.CharField(max_length=20, choices=student_status.choices, default=student_status.JOBLESS)

	def __str__(self):
		return self.university_id + ' ' + self.profile.first_name + ' ' + self.profile.last_name
	
	class Meta:
		verbose_name = 'Student'


class Teacher(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, default=1)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Teacher'

	def __str__(self) -> str:
		return self.department.name + ': ' + self.profile.__str__()


class Admin(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
	faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Admin'
		unique_together = ('profile', 'faculty')

	def __str__(self) -> str:
		return self.profile.__str__() + ': ' + self.faculty.__str__()


class SuperAdmin(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, default=1)
	
	class Meta:
		verbose_name = 'SuperAdmin'

	def __str__(self) -> str:
		return self.profile.__str__()