from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sprint.viewsets import SprintViewSet, SharedFolderViewSet

router = DefaultRouter()
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'shared-folders', SharedFolderViewSet, basename='shared-folder')

urlpatterns = [
    path('', include(router.urls)),
]
