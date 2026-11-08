from django.urls import path
from checker.views import home

urlpatterns = [path("", home, name="home")]
