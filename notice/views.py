from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import Notice, AdminNotice, SuperAdminNotice, AudienceChoices
from .permissions import AdminNoticePermission, SuperAdminNoticePermission
from accounts.models import Student, Admin, SuperAdmin


class NoticeViewSet(ModelViewSet):
	queryset = Notice.objects.all()


class AdminNoticeViewSet(ModelViewSet):
	queryset = AdminNotice.objects.all()
	serializer_class = AdminNoticeSerializer
	permission_classes = (AdminNoticePermission, )

	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = AdminNotice.objects.filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
			else:
				queryset = AdminNotice.objects.filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'TEACHER':
			queryset = AdminNotice.objects.filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))
		else:
			queryset = AdminNotice.objects.all()
		serializer = AdminNoticeSerializer(queryset, many=True)
		return Response(serializer.data)
	

	def retrieve(self, request, pk=None):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = AdminNotice.objects.filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
			else:
				queryset = AdminNotice.objects.filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'TEACHER':
			queryset = AdminNotice.objects.filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type in ['ADMIN', 'SUPER_ADMIN']:
			queryset = AdminNotice.objects.all()
		notice = get_object_or_404(queryset, pk=pk)
		serializer = AdminNoticeSerializer(notice)
		return Response(serializer.data)

	def perform_create(self, serializer):
		serializer.validated_data['author'] = Admin.objects.get(pk = self.request.user.pk)
		return super().perform_create(serializer)

class SuperAdminNoticeViewSet(ModelViewSet):
	queryset = SuperAdminNotice.objects.all()
	serializer_class = SuperAdminNoticeSerializer
	permission_classes = (SuperAdminNoticePermission, )


	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
			else:
				queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'TEACHER':
			queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'ADMIN':
			queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.STAFF) | Q(audience=AudienceChoices.ALL))
		else:
			queryset = SuperAdminNotice.objects.all()
		serializer = SuperAdminNoticeSerializer(queryset, many=True)
		return Response(serializer.data)
	
	def retrieve(self, request, pk=None):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
			else:
				queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'TEACHER':
			queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'ADMIN':
			queryset = SuperAdminNotice.objects.filter(Q(audience=AudienceChoices.STAFF) | Q(audience=AudienceChoices.ALL))
		else:
			queryset = SuperAdminNotice.objects.all()
		notice = get_object_or_404(queryset, pk=pk)
		serializer = SuperAdminNoticeSerializer(notice)
		return Response(serializer.data)

	def perform_create(self, serializer):
		serializer.validated_data['author'] = SuperAdmin.objects.get(pk=self.request.user.pk)
		return super().perform_create(serializer)