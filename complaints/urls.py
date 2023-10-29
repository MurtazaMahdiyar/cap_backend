from alumnus.urls import router
from django.urls import path, include
from .views import ComplaintViewSet


router.register('complaints', ComplaintViewSet, basename='complaint')