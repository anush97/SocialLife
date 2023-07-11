from django.conf.urls import url, patterns
from .views import CreateUserAPIView
urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
]
