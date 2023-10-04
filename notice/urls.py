from complaints.urls import router
from django.urls import path, include
from .views import (
	AdminNoticeViewSet, SuperAdminNoticeViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router.register('admin-notices', AdminNoticeViewSet, basename='admin-notice')
router.register('super-admin-notices', SuperAdminNoticeViewSet, basename='super-admin-notice')


urlpatterns = [
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('', include(router.urls)),
]
