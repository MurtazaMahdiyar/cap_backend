from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import *
from .permissions import ComplaintPermission, ComplaintDocumentPermission
from accounts.models import Admin, Student



class ComplaintViewSet(ModelViewSet):
	queryset = Complaint.objects.all()
	serializer_class = ComplaintSerializer
	permission_classes = (ComplaintPermission, )

	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			student = Student.objects.get(pk=request.user.pk)
			queryset = Complaint.objects.filter(student=student)
		elif request.user.profile_type == 'ADMIN':
			admin = Admin.objects.get(pk=request.user.id)
			queryset = Complaint.objects.filter(student__student_class__department__faculty=admin.faculty)
		else:
			queryset = Complaint.objects.all()
		serializer = ComplaintSerializer(queryset, many=True)
		return Response(serializer.data)


class ComplaintDocumentViewSet(ModelViewSet):
	queryset = ComplaintDocument.objects.all()
	serializer_class = ComplaintDocumentSerializer
	permission_classes = (ComplaintDocumentPermission, )

	def list(self, request):
		if request.user.profile_type == 'STUDENT':
			queryset = ComplaintDocument.objects.filter(complaint__student=request.user.pk)
		elif request.user.profile_type == 'ADMIN':
			admin = Admin.objects.get(pk=request.user.pk)
			queryset = Complaint.objects.filter(complaint__student__class__department__faculty=admin.faculty)
		else:
			queryset = ComplaintDocument.objects.all()
		serializer = ComplaintDocumentSerializer(queryset, many=True)
		return Response(serializer.data)
