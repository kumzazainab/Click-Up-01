from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import SignupViewSet, LoginView
from user.viewsets import UserViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'users', UserViewSet, basename='users')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
