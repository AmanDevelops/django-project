from django.urls import path

from core.views import *

urlpatterns = [path("", Public.as_view(), name="home")]
