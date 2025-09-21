from django.contrib import admin
from django.urls import path, include
from user_profile import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", user_views.landing, name="landing"),  # root landing page
    path("accounts/", include("user_profile.urls")),
]