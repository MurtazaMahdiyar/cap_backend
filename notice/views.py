from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import Notice, AudienceChoices
from .permissions import NoticePermission
from accounts.models import Student


class NoticeViewSet(ModelViewSet):
	queryset = Notice.objects.all()
	serializer_class = NoticeSerializer
	permission_classes = (NoticePermission, )

	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = Notice.objects.filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
			else:
				queryset = Notice.objects.filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))

		elif request.user.profile_type == 'TEACHER':
			queryset = Notice.objects.filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))

		elif request.user.profile_type in ['ADMIN', 'SUPER_ADMIN']:
			queryset = Notice.objects.all()

		serializer = NoticeSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		queryset = Notice.objects.all()
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			if student.graduated:
				queryset = Notice.objects.filter(Q(audience=AudienceChoices.ALUMNUS) | Q(audience=AudienceChoices.ALL))
			else:
				queryset = Notice.objects.filter(Q(audience=AudienceChoices.STUDENT) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type == 'TEACHER':
			queryset = Notice.objects.filter(Q(audience=AudienceChoices.TEACHER) | Q(audience=AudienceChoices.ALL))
		elif request.user.profile_type in ['ADMIN', 'SUPER_ADMIN']:
			queryset = Notice.objects.all()
		else:
			queryset = None

		notice = get_object_or_404(queryset, pk=pk)
		serializer = NoticeSerializer(notice)
		return Response(serializer.data)


	def perform_create(self, serializer):
		serializer.validated_data['author'] = self.request.user
		return super().perform_create(serializer)
