from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import Notice, AudienceChoices
from .permissions import NoticePermission
from accounts.models import Student, Admin, Teacher
from django.core.mail import send_mail


class NoticeViewSet(ModelViewSet):
	queryset = Notice.objects.all()
	serializer_class = NoticeSerializer
	permission_classes = (NoticePermission, )

	def list(self, request):

		match(request.user.profile_type):
			case 'STUDENT':
				student = Student.objects.get(pk=request.user.pk)
				if student.graduated:
					queryset = Notice.objects.filter((Q(faculty=student.student_class.department.faculty) | Q(faculty__isnull=True))).filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
				else:
					queryset = Notice.objects.filter((Q(faculty=student.student_class.department.faculty) | Q(faculty__isnull=True))).filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))

			case 'TEACHER':
				teacher = Teacher.objects.get(pk=request.user.pk)
				queryset = Notice.objects.filter(Q(faculty=teacher.department.faculty) | Q(faculty__isnull=True)).filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))

			case 'ADMIN':
				admin = Admin.objects.get(pk=request.user.pk)
				queryset = Notice.objects.filter(Q(faculty=admin.faculty) | Q(faculty__isnull=True)).filter(Q(audience=AudienceChoices.STAFF) | Q(audience=AudienceChoices.ALL) | Q(author=request.user))

			case 'SUPER_ADMIN':
				queryset = Notice.objects.filter(author=request.user)


		serializer = NoticeSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		match(request.user.profile_type):
			case 'STUDENT':
				student = Student.objects.get(pk=request.user.pk)
				if student.graduated:
					queryset = Notice.objects.filter((Q(faculty=student.student_class.department.faculty) | Q(faculty__isnull=True))).filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
				else:
					queryset = Notice.objects.filter((Q(faculty=student.student_class.department.faculty) | Q(faculty__isnull=True))).filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))

			case 'TEACHER':
				teacher = Teacher.objects.get(pk=request.user.pk)
				queryset = Notice.objects.filter(Q(faculty=teacher.department.faculty) | Q(faculty__isnull=True)).filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))

			case 'ADMIN':
				admin = Admin.objects.get(pk=request.user.pk)
				queryset = Notice.objects.filter(Q(faculty=admin.faculty) | Q(faculty__isnull=True)).filter(Q(audience=AudienceChoices.STAFF) | Q(audience=AudienceChoices.ALL)) | Q(author=request.user)

			case 'SUPER_ADMIN':
				queryset = Notice.objects.filter(author=request.user)


		_object = get_object_or_404(queryset, pk=pk)
		serializer = NoticeSerializer(_object)
		return Response(serializer.data)


	def perform_create(self, serializer):

		notice_faculty = None
		if self.request.user.profile_type == 'ADMIN':
			notice_faculty = Admin.objects.get(pk=self.request.user.pk).faculty

		serializer.validated_data['faculty'] = notice_faculty
		serializer.validated_data['author'] = self.request.user
		instance = super().perform_create(serializer)

		try:
			if serializer.validated_data['audience'] in ['ALUMNUS']:
				# SEND EMAIL TO ALUMNUS
				students = Student.objects.filter(graduated=True)

				if notice_faculty is not None:
					students.filter(student_class__department__faculty=notice_faculty)

				list_emails = []
				for student in students:
					list_emails.append(student.profile.email)

				send_mail(
				    serializer.validated_data['title'],
				    serializer.validated_data['description'],
				    "admin@cap.com",
				    list_emails,
				    fail_silently=False,
				)

			elif serializer.validated_data['audience'] in ['STUDENT']:
				# SEND EMAIL TO ALUMNUS
				students = Student.objects.filter(graduated=False)

				if notice_faculty is not None:
					students.filter(student_class__department__faculty=notice_faculty)

				list_emails = []
				for student in students:
					list_emails.append(student.profile.email)

				send_mail(
				    serializer.validated_data['title'],
				    serializer.validated_data['description'],
				    "admin@cap.com",
				    list_emails,
				    fail_silently=False,
				)


			elif serializer.validated_data['audience'] in ['TEACHER']:
				teachers = Teacher.objects.all()

				if notice_faculty is not None:
					teachers.filter(faculty=notice_faculty)

				list_emails = []
				for teacher in teachers:
					list_emails.append(teacher.profile.email)

				send_mail(
				    serializer.validated_data['title'],
				    serializer.validated_data['description'],
				    "admin@cap.com",
				    list_emails,
				    fail_silently=False,
				)

			elif serializer.validated_data['audience'] in ['ADMIN']:
				admins = Admin.objects.all()

				if notice_faculty is not None:
					admins.filter(faculty=notice_faculty)

				list_emails = []
				for admin in admins:
					list_emails.append(admin.profile.email)

				send_mail(
				    serializer.validated_data['title'],
				    serializer.validated_data['description'],
				    "admin@cap.com",
				    list_emails,
				    fail_silently=False,
				)

			elif serializer.validated_data['audience'] == 'ALL':
				admins = Admin.objects.all()
				students = Student.objects.all()
				teachers = Teacher.objects.all()


				if notice_faculty is not None:
					admins.filter(faculty=notice_faculty)
					students.filter(student_class__department__faculty=notice_faculty)
					teachers.filter(faculty=notice_faculty)

				list_emails = []
				for admin in admins:
					list_emails.append(admin.profile.email)

				for teacher in teachers:
					list_emails.append(admin.profile.email)

				for student in students:
					list_emails.append(admin.profile.email)

				send_mail(
				    serializer.validated_data['title'],
				    serializer.validated_data['description'],
				    "admin@cap.com",
				    list_emails,
				    fail_silently=False,
				)
		except:
			pass

		return instance
