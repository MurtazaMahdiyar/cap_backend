from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .permissions import (
    AdminPermission, SuperAdminPermission, TeacherPermission,
    FacultyPermission, DepartmentPermission, ProfilePermission, StudentPermission
)
from .serializers import *



class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermission, )


    def perform_create(self, serializer):
        try:
            if self.request.user.profile_type in ['ADMIN', 'SUPER_ADMIN']:
                serializer.validated_data['is_active'] = True
        except:
            serializer.validated_data['is_active'] = False

        password = serializer.validated_data.pop('password')
        serializer.validated_data.update({'password' : make_password(password)})
        super().perform_create(serializer)

    def perform_update(self, serializer):
        if self.request.user.profile_type not in ['ADMIN', 'SUPER_ADMIN']:
            try:
                serializer.validated_data.pop('is_active')
            except:
                pass

            try:
                password = serializer.validated_data.pop('password')
                serializer.validated_data.update({'password' : make_password(password)})
            except:
                pass

        super().perform_update(serializer)



class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (StudentPermission, )



    def list(self, request):

        if request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=request.user.id)
            queryset = Student.objects.prefetch_related(*['jobs', 'scholarships']).filter(student_class__department__faculty = admin.faculty)

        elif request.user.profile_type == 'SUPER_ADMIN':
            queryset = Student.objects.prefetch_related(*['jobs', 'scholarships']).all()

        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        if request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=request.user.id)
            queryset = Student.objects.prefetch_related(*['jobs', 'scholarships']).filter(student_class__department__faculty = admin.faculty)

        elif request.user.profile_type == 'SUPER_ADMIN':
            queryset = Student.objects.prefetch_related(*['jobs', 'scholarships']).all()
        
        _object = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(_object)
        return Response(serializer.data)


    def perform_create(self, serializer):
        if serializer.validated_data['profile'].profile_type == '':
            profile = serializer.validated_data['profile']
            profile.profile_type = 'STUDENT'

            profile.save()
            serializer.save()
        

    def perform_update(self, serializer):
        try:
            profile = serializer.validated_data['profile']
            profile.profile_type = 'STUDENT'
            profile.save()
        except:
            pass
        
        serializer.save()

    def perform_destroy(self, instance):
        student = instance.profile
        student.profile_type = ''
        student.save()
        instance.delete()
        

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (TeacherPermission, )


    def list(self, request):

        if request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=request.user.id)
            queryset = Teacher.objects.filter(department__faculty = admin.faculty)

        elif request.user.profile_type == 'SUPER_ADMIN':
            queryset = Teacher.objects.all()

        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        if request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=request.user.id)
            queryset = Teacher.objects.filter(department__faculty = admin.faculty)

        elif request.user.profile_type == 'SUPER_ADMIN':
            queryset = Teacher.objects.all()
        
        _object = get_object_or_404(queryset, pk=pk)
        serializer = TeacherSerializer(_object)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.validated_data['profile'].profile_type == '':
            profile = serializer.validated_data['profile']
            profile.profile_type = 'TEACHER'

            profile.save()
            serializer.save()


    def perform_update(self, serializer):
        profile = serializer.validated_data['profile']
        profile.profile_type = 'TEACHER'

        profile.save()
        serializer.save()


    def perform_destroy(self, instance):
        teacher = instance.profile
        teacher.profile_type = ''
        teacher.save()
        instance.delete()


class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (AdminPermission, )

    def perform_create(self, serializer):
        if serializer.validated_data['profile'].profile_type == '':
            profile = serializer.validated_data['profile']
            profile.profile_type = 'ADMIN'
            profile.is_staff = True

            profile.save()
            serializer.save()
        

    def perform_update(self, serializer):
        profile = serializer.validated_data['profile']
        profile.profile_type = 'ADMIN'
        profile.is_staff = True

        profile.save()
        serializer.save()


    def perform_destroy(self, instance):
        admin = instance.profile
        admin.profile_type = ''
        admin.save()
        instance.delete()


class SuperAdminViewSet(ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    permission_classes = (SuperAdminPermission, )

    def perform_create(self, serializer):
        if serializer.validated_data['profile'].profile_type == '':
            profile = serializer.validated_data['profile']
            profile.profile_type = 'SUPER_ADMIN'
            profile.is_staff = True

            profile.save()
            serializer.save()



    def perform_update(self, serializer):
        profile = serializer.validated_data['profile']
        profile.profile_type = 'SUPER_ADMIN'
        profile.is_staff = True

        profile.save()
        serializer.save()



    def perform_destroy(self, instance):
        super_admin = instance.profile
        super_admin.profile_type = ''
        super_admin.save()
        instance.delete()



class FacultyViewSet(ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = (FacultyPermission, )


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (DepartmentPermission, )


    def perform_create(self, serializer):
        if self.request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=self.request.user)
            if admin.faculty == serializer.validated_data['faculty']:
                serializer.save()
        else:
            serializer.save()


    def perform_update(self, serializer):
        if self.request.user.profile_type == 'ADMIN':
            admin = Admin.objects.get(pk=self.request.user)
            if admin.faculty == serializer.validated_data['faculty']:
                serializer.save()
        else:
            serializer.save()
