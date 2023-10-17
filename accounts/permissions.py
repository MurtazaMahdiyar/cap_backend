from rest_framework import permissions


class ProfilePermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user.profile_type in ['SUPER_ADMIN', 'ADMIN']
        elif view.action == 'create':
            return request.user.is_authenticated
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.profile_type in ['SUPER_ADMIN', 'ADMIN']
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.profile_type in ['SUPER_ADMIN', 'ADMIN']
        elif view.action == 'destroy':
            return request.user.is_authenticated and (request.user.profile_type == 'SUPER_ADMIN')
        else:
            return False


class StudentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj.pk == request.user.pk or (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action in ['update', 'partial_update']:
            print(obj.pk)
            return request.user.pk == obj.pk or (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action == 'destroy':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN'])
        else:
            return False


class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj.pk == request.user.pk or (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated and (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action == 'destroy':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN'])
        else:
            return False



class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type == 'SUPER_ADMIN')
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['ADMIN', 'SUPER_ADMIN'])
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated and obj.pk == request.user.pk or (request.user.profile_type == 'SUPER_ADMIN')
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated and (request.user.profile_type == 'SUPER_ADMIN')
        elif view.action == 'destroy':
            return request.user.is_authenticated and (request.user.profile_type == 'SUPER_ADMIN')
        else:
            return False


class SuperAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN'])
        elif view.action == 'create':
            return request.user.is_authenticated and (request.user.profile_type in ['SUPER_ADMIN'])
        elif view.action in ['retrieve']:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
        
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj.pk == request.user.pk or (request.user.profile_type in ['SUPER_ADMIN'])
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and obj.pk == request.user.pk
        else:
            return False
        


class FacultyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return request.user.is_authenticated and request.user.profile_type == 'SUPER_ADMIN'
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
            return request.user.is_authenticated and request.user.profile_type == 'SUPER_ADMIN'
        elif view.action == 'destroy':
            return request.user.is_authenticated and request.user.profile_type == 'SUPER_ADMIN'
        else:
            return False


class DepartmentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return request.user.is_authenticated and request.user.profile_type in ['SUPER_ADMIN', 'ADMIN']
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
            return request.user.is_authenticated and (request.user.profile_type == 'SUPER_ADMIN' or (request.user.profile_type == 'ADMIN' and request.user.faculty == obj.faculty))
        elif view.action == 'destroy':
            return request.user.is_authenticated and (request.user.profile_type == 'SUPER_ADMIN' or (request.user.profile_type == 'ADMIN' and request.user.faculty == obj.faculty))
        else:
            return False
