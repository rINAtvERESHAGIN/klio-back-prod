from django.urls import path

from .views import UserDetailView, UserListView


urlpatterns = [
    path('list', UserListView.as_view()),
    path('<int:pk>/detail', UserDetailView.as_view()),
]
