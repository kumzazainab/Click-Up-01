from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sprint.views import SprintViewSet, TaskViewSet, SharedFolderViewSet

router = DefaultRouter()
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'shared-folders', SharedFolderViewSet, basename='shared-folder')

urlpatterns = [
    path('', include(router.urls)),
]
