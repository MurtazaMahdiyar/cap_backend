from accounts.urls import router
from .views import (
    JobViewSet, ScholarshipViewSet,
    ClassViewSet, SubjectViewSet, ResultSheetViewSet,
)


router.register('scholarships', ScholarshipViewSet, basename='scholarship')
router.register('jobs', JobViewSet, basename='job')
router.register('classes', ClassViewSet, basename='class')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('result-sheets', ResultSheetViewSet, basename='result-sheet')
