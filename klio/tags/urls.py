from django.urls import path

from .views import TagCreateView, TagDetailView, TagListView


urlpatterns = [
    path('create', TagCreateView.as_view()),
    path('list', TagListView.as_view()),
    path('<int:pk>/detail', TagDetailView.as_view()),
]
