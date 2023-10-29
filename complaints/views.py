from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import *
from .permissions import ComplaintPermission
from accounts.models import Admin, Student, Teacher



class ComplaintViewSet(ModelViewSet):
	queryset = Complaint.objects.all()
	serializer_class = ComplaintSerializer
	permission_classes = (ComplaintPermission, )

	def list(self, request):
		if request.user.profile_type in ['STUDENT', 'TEACHER']:
			queryset = Complaint.objects.filter(profile__id=request.user.id)

		elif request.user.profile_type == 'ADMIN':
			admin = Admin.objects.get(pk=request.user.id)
			queryset = Complaint.objects.filter(~Q(complaint_against = 'STAFF') & Q(faculty=admin.faculty))

		elif request.user.profile_type == 'SUPER_ADMIN':
			queryset = Complaint.objects.filter(complaint_against='STAFF')

		serializer = ComplaintSerializer(queryset, many=True)
		return Response(serializer.data)
	

	def perform_update(self, serializer):

		if self.request.user.profile_type in ['SUPER_ADMIN', 'ADMIN']:
			try:
				status = serializer.validated_data['status']
				serializer.validated_data.clear()
				serializer.validated_data.update({'status': status})
			except:
				pass
		else:
			try:
				serializer.validated_data.pop('status')
			except:
				pass

		return super().perform_update(serializer)


	def perform_create(self, serializer):
		
		complaint_faculty = None
		if self.request.user.profile_type == 'STUDENT':
			complaint_faculty = Student.objects.get(pk=self.request.user.pk).student_class.department.faculty
		elif self.request.user.profile_type == 'TEACHER':
			complaint_faculty = Teacher.objects.get(pk=self.request.user.pk).department.faculty

		serializer.validated_data['faculty'] = complaint_faculty
		serializer.validated_data['profile'] = self.request.user

		return super().perform_create(serializer)
