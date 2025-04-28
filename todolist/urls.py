from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todolist.views import StopTimerAPIView, GreetingAPIView
from todolist.viewsets import SubTaskViewSet, TaskActivityViewSet, CommentViewSet, \
    CommentAttachmentViewSet, TaskAttachmentViewSet, TaskViewSet, TagViewSet, TaskStatusViewSet

router = DefaultRouter()

router.register(r'create-tasks', TaskViewSet, basename='create-tasks')
router.register(r'add-tags', TagViewSet, basename='add-tag')
router.register(r'add-status', TaskStatusViewSet, basename='add-status')

router.register(r'sub-tasks', SubTaskViewSet, basename='sub-tasks')
router.register(r'task-activity', TaskActivityViewSet, basename='task-activity')
router.register(r'add-comment', CommentViewSet, basename='add-comment')
router.register(r'comment-attachment', CommentAttachmentViewSet, basename='comment-attachment')
router.register(r'task-attachment', TaskAttachmentViewSet, basename='task-attachment')

urlpatterns = [
    path('', include(router.urls)),
    path('stop-timer/', StopTimerAPIView.as_view(), name='stop-timer'),
    path('greeting/', GreetingAPIView.as_view(), name='greeting-api')
]
