from django.urls import path

from .views import certificate_file, cv_file, portfolio_api

urlpatterns = [
    path('portfolio/', portfolio_api),
    path('cv/', cv_file),
    path('certificates/<int:pk>/file/', certificate_file),
]
