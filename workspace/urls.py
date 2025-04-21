from rest_framework.routers import DefaultRouter
from workspace.views import WorkspaceViewSet, WorkspaceInvitationViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'create-workspace', WorkspaceViewSet, basename='create-workspace')
router.register(r'invitation', WorkspaceInvitationViewSet, basename='invitation')

urlpatterns = [
    path('', include(router.urls)),
]
