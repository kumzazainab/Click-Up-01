from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home.views import SearchViewSet, GreetingAPIView

router = DefaultRouter()
router.register('search', SearchViewSet, basename='search')
urlpatterns = [
    path('', include(router.urls)),
    path('greeting/', GreetingAPIView.as_view(), name='greeting-api'),

]