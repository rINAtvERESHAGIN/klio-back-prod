from django.urls import path

from .views import UserCreateView, UserDetailView, UserListView


urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('list/', UserListView.as_view()),
    path('<int:pk>/detail/', UserDetailView.as_view()),
]
