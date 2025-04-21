from django.urls import path, include
app_name = 'twofactor'

urlpatterns = [
    path('two_factor/', include('two_factor.urls', namespace='two_factor')),
]