from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *
from .models import AdminNotice, SuperAdminNotice, AudienceChoices
from .permissions import AdminNoticePermission, SuperAdminNoticePermission
from accounts.models import Student


class AdminNoticeViewSet(ModelViewSet):
	queryset = AdminNotice.objects.all()
	serializer_class = AdminNoticeSerializer
	permission_classes = (AdminNoticePermission, )

	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = AdminNotice.objects.filter(audience=AudienceChoices.ALUMNUS)
			else:
				queryset = AdminNotice.objects.filter(audience=AudienceChoices.STUDENT)
		elif request.user.profile_type == 'TEACHER':
			queryset = AdminNotice.objects.filter(audience=AudienceChoices.TEACHER)
		else:
			queryset = AdminNotice.objects.all()
		serializer = AdminNoticeSerializer(queryset, many=True)
		return Response(serializer.data)
	

	def retrieve(self, request, pk=None):
		if request.user.profile_type == 'STUDENT':
			if request.user.graduated:
				queryset = AdminNotice.objects.filter(audience=AudienceChoices.ALUMNUS)
			else:
				queryset = AdminNotice.objects.filter(audience=AudienceChoices.STUDENT)
		elif request.user.profile_type == 'TEACHER':
			queryset = AdminNotice.objects.filter(audience=AudienceChoices.TEACHER)
		else:
			queryset = AdminNotice.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		serializer = AdminNoticeSerializer(user)
		return Response(serializer.data)

class SuperAdminNoticeViewSet(ModelViewSet):
	queryset = SuperAdminNotice.objects.all()
	serializer_class = SuperAdminNoticeSerializer
	permission_classes = (SuperAdminNoticePermission, )


	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.ALUMNUS)
			else:
				queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.STUDENT)
		elif request.user.profile_type == 'TEACHER':
			queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.TEACHER)
		elif request.user.profile_type == 'ADMIN':
			queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.STAFF)
		else:
			queryset = SuperAdminNotice.objects.all()
		serializer = SuperAdminNoticeSerializer(queryset, many=True)
		return Response(serializer.data)
	
	def retrieve(self, request, pk=None):
		if request.user.profile_type == 'STUDENT':
			if request.user.graduated:
				queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.ALUMNUS)
			else:
				queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.STUDENT)
		elif request.user.profile_type == 'TEACHER':
			queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.TEACHER)
		elif request.user.profile_type == 'ADMIN':
			queryset = SuperAdminNotice.objects.filter(audience=AudienceChoices.STAFF)
		else:
			queryset = SuperAdminNotice.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		serializer = SuperAdminNoticeSerializer(user)
		return Response(serializer.data)