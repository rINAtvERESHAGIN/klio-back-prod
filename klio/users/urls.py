from django.urls import path

from .views import CurrentUserDetailView, CurrentUserUpdateView


urlpatterns = [
    path('current', CurrentUserDetailView.as_view(), name='current_user'),
    path('current/update', CurrentUserUpdateView.as_view(), name='current_user_update'),
]
