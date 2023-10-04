from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .permissions import (
    JobScholarshipPermission, ClassPermission, SubjectPermission, ResultSheetPermission
)
from .models import *
from accounts.models import Admin
from accounts.serializers import (
    JobSerializer, ScholarshipSerializer, ClassSerializer, SubjectSerializer, ResultSheetSerializer
)


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (JobScholarshipPermission, )

    def perform_create(self, serializer):
        count = Job.objects.filter(start_date__gte=datetime.date.today() - datetime.timedelta(30))
        if count == 0:
            serializer.save()


class ScholarshipViewSet(ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = (JobScholarshipPermission, )

    def perform_create(self, serializer):
        count = Scholarship.objects.filter(start_date__gte=datetime.date.today() - datetime.timedelta(30))
        if count == 0:
            serializer.save()


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = (ClassPermission, )

    
class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (SubjectPermission, )


class ResultSheetViewSet(ModelViewSet):
    queryset = ResultSheet.objects.all()
    serializer_class = ResultSheetSerializer
    permission_classes = (ResultSheetPermission, )

    def list(self, request):
        if request.user.profile_type == 'STUDENT':
            queryset = ResultSheet.objects.filter(subject__class=request.user.student_class)
        elif request.user.profile_type == 'TEACHER':
            queryset = ResultSheet.objects.filter(subject__teacher=request.user)
        elif request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=request.user.pk)
            queryset = ResultSheet.objects.filter(subject__class__department__faculty=admin.faculty)
        else:
            queryset = ResultSheet.objects.all()
        serializer = ResultSheetSerializer(queryset, many=True)
        return Response(serializer.data)
