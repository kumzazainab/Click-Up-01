from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todolist.views import AdminTaskReportView, SubTaskViewSet, TaskActivityViewSet, CommentViewSet, \
    CommentAttachmentViewSet

router = DefaultRouter()
router.register(r'sub-tasks', SubTaskViewSet, basename='sub-tasks')
router.register(r'task-activity', TaskActivityViewSet, basename='task-activity')
router.register(r'add-comment', CommentViewSet, basename='add-comment')
router.register(r'comment-attachment', CommentAttachmentViewSet, basename='comment-attachment')

urlpatterns = [
    path('', include(router.urls)),
    path('reports', AdminTaskReportView.as_view(), name='admin-task-report'),
]
