from rest_framework import permissions
from accounts.models import Admin, Student, Teacher
from .models import (
    Complaint
)


class ComplaintPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'STUDENT', 'TEACHER'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['STUDENT', 'TEACHER'])
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
                return obj.faculty == admin.faculty and obj.complaint_against != Complaint.ComplaintTarget.STAFF
            return obj.profile == request.user or (request.user.profile_type == 'SUPER_ADMIN')
        elif view.action in ['update', 'partial_update']:
            if request.user.profile_type == 'ADMIN':
                admin = Admin.objects.get(pk=request.user.pk)
                return request.user.profile_type == 'ADMIN' and obj.student.student_class.department.faculty == admin.faculty
            return obj.profile == request.user or (request.user.profile_type == 'SUPER_ADMIN')
        elif view.action == 'destroy':
            return (obj.student == request.user and obj.status == Complaint.ComplaintStatus.RECEIVED) or (request.user.profile_type == 'SUPER_ADMIN')
        else:
            return False



class ComplaintDocumentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'STUDENT'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type == 'STUDENT')
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj.complaint.student == request.user or (request.user.profile_type == 'SUPER_ADMIN') or (request.user.profile_type == 'ADMIN' and obj.complaint.complaint_against != Complaint.ComplaintTarget.STAFF)
        elif view.action in ['update', 'partial_update']:
            return obj.student == request.user
        elif view.action == 'destroy':
            return (obj.complaint.student == request.user and obj.status == Complaint.ComplaintStatus.RECEIVED) or (request.user.profile_type == 'SUPER_ADMIN')
        else:
            return False

