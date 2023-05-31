from django.urls import path,include
from .views import *

urlpatterns = [
    path('auth',Authorize.as_view())
]