from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login/logout
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # password reset
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # signup
    path("signup/customer/", views.signup_customer, name="signup_customer"),
    path("signup/stylist/", views.signup_stylist, name="signup_stylist"),

    # dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
]