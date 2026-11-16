from django.urls import path

from .views import event_api

urlpatterns = [
    path('events/', event_api),
]
