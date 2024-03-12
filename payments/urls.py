from django.urls import path
from payments.views import *


urlpatterns = [
    path("", home, name="home"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
]

