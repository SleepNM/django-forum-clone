from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'accounts'
urlpatterns = [
    path("register", views.registration_view, name="register"),
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("login", LoginView.as_view(
        template_name='accounts/login.html'
        ), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("pwchange", views.ChangePasswordView.as_view(), name="pwchange"),
    path("update", views.profile_update, name="update"),
]
