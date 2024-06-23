from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UploadedFileViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('files', UploadedFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
