from django.urls import path

from .views import ActivationView, LoginView, LogoutView, PasswordResetView, PasswordSetView, RegistrationView


login_template = {'template_name': 'rest_framework/login.html'}

urlpatterns = [
    path('activate/<str:activation_key>', ActivationView.as_view(), name="activate"),
    path('password/reset', PasswordResetView.as_view(), name="password-reset"),
    path('password/<int:user_id>/set/<str:reset_key>', PasswordSetView.as_view(), name="password-set"),
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), login_template, name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
