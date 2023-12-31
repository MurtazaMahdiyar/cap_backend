from rest_framework import permissions
from accounts.models import Admin


class JobScholarshipPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'STUDENT'])
        elif view.action == 'create':
            return request.user.is_authenticated and request.user.profile_type == 'STUDENT'
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            if request.user.profile_type == 'ADMIN':
                admin = Admin.objects.get(pk=request.user.pk)
                return obj.student.student_class.department.faculty == admin.faculty
            return obj.student.profile == request.user or (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'STUDENT'])
        elif view.action in ['update', 'partial_update']:
            return obj.student.profile == request.user
        elif view.action == 'destroy':
            return obj.student.profile == request.user or (request.user.profile_type in ['SUPER_ADMIN'])
        else:
            return False



class ClassPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update']:
            if request.user.profile_type == 'ADMIN':
                admin = Admin.objects.get(pk = request.user.pk)
                return admin.faculty == obj.department.faculty

            return request.user.profile_type == 'SUPER_ADMIN'

        elif view.action == 'destroy':
            if request.user.profile_type == 'ADMIN':
                admin = Admin.objects.get(pk = request.user.pk)
                return admin.faculty == obj.department.faculty

            return request.user.profile_type == 'SUPER_ADMIN'
        else:
            return False




class SubjectPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update']:
            if request.user.profile_type == 'ADMIN':
                admin = Admin.objects.get(pk = request.user.pk)
                return admin.faculty == obj.subject_class.department.faculty

            return request.user.profile_type == 'SUPER_ADMIN'

        elif view.action == 'destroy':
            if request.user.profile_type == 'ADMIN':
                admin = Admin.objects.get(pk = request.user.pk)
                return admin.faculty == obj.subject_class.department.faculty

            return request.user.profile_type == 'SUPER_ADMIN'
        else:
            return False



class ResultSheetPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'TEACHER'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'TEACHER'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated and request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'TEACHER', 'STUDENT']
        elif view.action in ['update', 'partial_update']:
            return request.user.profile_type in ['SUPER_ADMIN', 'ADMIN'] or (request.user.profile_type == 'TEACHER' and request.user == obj.subject.teacher)
        elif view.action == 'destroy':
            return request.user.profile_type in ['SUPER_ADMIN', 'ADMIN'] or (request.user.profile_type == 'TEACHER' and request.user == obj.subject.teacher.profile)
        else:
            return False