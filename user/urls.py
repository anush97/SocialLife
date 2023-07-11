from django.urls import path, include , re_path
from .views import CreateUserAPIView
app_name = 'user'

urlpatterns = [
    re_path(r'^create/$', CreateUserAPIView.as_view()),
]
