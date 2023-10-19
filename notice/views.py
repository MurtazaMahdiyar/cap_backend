from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import Notice, AudienceChoices
from .permissions import NoticePermission
from accounts.models import Student, Admin, SuperAdmin


class NoticeViewSet(ModelViewSet):
	queryset = Notice.objects.all()
	serializer_class = NoticeSerializer
	permission_classes = (NoticePermission, )

	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = Notice.objects.filter((Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL)) and (Q(faculty=student.student_class.department.faculty)))
			else:
				queryset = Notice.objects.filter((Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL)) and (Q(faculty=student.student_class.department.faculty)))

		elif request.user.profile_type == 'TEACHER':
			teacher = Teacher.objects.get(pk=request.user.pk)
			queryset = Notice.objects.filter((Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL)) and (Q(faculty=teacher.department.faculty)))

		elif request.user.profile_type == 'ADMIN':
			admin = Admin.objects.get(pk=request.user.pk)
			queryset = Notice.objects.filter((Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL)) and (Q(faculty=admin.faculty)))

		elif request.user.profile_type == 'SUPER_ADMIN':
			queryset = Notice.objects.filter(author=request.user)

		serializer = NoticeSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = Notice.objects.filter((Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL)) and Q(faculty=student.student_class.department.faculty))
			else:
				queryset = Notice.objects.filter((Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL)) and Q(faculty=student.student_class.department.faculty))

		elif request.user.profile_type == 'TEACHER':
			teacher = Teacher.objects.get(pk=request.user.pk)
			queryset = Notice.objects.filter((Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL)) and Q(faculty=teacher.department.faculty))

		elif request.user.profile_type == 'ADMIN':
			admin = Admin.objects.get(pk=request.user.pk)
			queryset = Notice.objects.filter((Q(audience=AudienceChoices.STAFF) | Q(audience=AudienceChoices.ALL)) and Q(faculty=admin.faculty))

		elif request.user.profile_type == 'SUPER_ADMIN':
			queryset = Notice.objects.filter(Q(author=request.user) | Q(audience=AudienceChoices.ALL))

		return Response(serializer.data)


	def perform_create(self, serializer):

		notice_faculty = None
		if self.request.user.profile_type == 'ADMIN':
			notice_faculty = Admin.objects.get(pk=self.request.user.pk).faculty
		elif self.request.user.profile_type == 'SUPER_ADMIN':
			notice_faculty = SuperAdmin.objects.get(pk=self.request.user.pk).faculty

		serializer.validated_data['faculty'] = notice_faculty
		serializer.validated_data['author'] = self.request.user
		return super().perform_create(serializer)
