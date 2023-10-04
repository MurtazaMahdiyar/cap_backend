from rest_framework import permissions


class AdminNoticePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'TEACHER', 'STUDENT'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['ADMIN'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'TEACHER', 'STUDENT'])
        elif view.action in ['update', 'partial_update']:
            return obj.author == request.user
        elif view.action == 'destroy':
            return obj.author == request.user or request.user.profile_type == 'SUPER_ADMIN'
        else:
            return False
        


class SuperAdminNoticePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'TEACHER', 'STUDENT'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN', 'ADMIN', 'TEACHER', 'STUDENT'])
        elif view.action in ['update', 'partial_update']:
            return obj.author == request.user
        elif view.action == 'destroy':
            return obj.author == request.user or request.user.profile_type == 'SUPER_ADMIN'
        else:
            return False

