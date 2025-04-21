from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todolist.views import AdminTaskReportView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('reports', AdminTaskReportView.as_view(), name='admin-task-report'),
]
