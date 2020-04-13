from django.urls import path

from .views import ActivationView, PasswordResetView, PasswordSetView, RegistrationView


urlpatterns = [
    path('activate/<str:activation_key>', ActivationView.as_view(), name="activate"),
    path('password/reset', PasswordResetView.as_view(), name="password-reset"),
    path('password/<int:user_id>/set/<str:reset_key>', PasswordSetView.as_view(), name="password-set"),
    path('register', RegistrationView.as_view(), name="register"),
    # path('logout', LogoutView.as_view(), name="logout"),
]
