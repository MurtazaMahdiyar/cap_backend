from rest_framework.routers import DefaultRouter
from accounts import views


router = DefaultRouter()

router.register('profile', views.ProfileViewSet, basename='profile')
router.register('super-admins', views.SuperAdminViewSet, basename='super-admin')
router.register('admins', views.AdminViewSet, basename='admin')
router.register('teachers', views.TeacherViewSet, basename='teacher')
router.register('facultys', views.FacultyViewSet, basename='faculty')
router.register('departments', views.DepartmentViewSet, basename='department')
router.register('students', views.StudentViewSet, basename='student')
