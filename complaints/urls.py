from alumnus.urls import router
from django.urls import path, include
from .views import ComplaintViewSet, ComplaintDocumentViewSet


router.register('complaints', ComplaintViewSet, basename='complaint')
router.register('complaint-documents', ComplaintDocumentViewSet, basename='complaint-document')
