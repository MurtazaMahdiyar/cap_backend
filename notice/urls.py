from complaints.urls import router
from django.urls import path, include
from .views import (
	NoticeViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router.register('notices', NoticeViewSet, basename='notice')


urlpatterns = [
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('', include(router.urls)),
]
