from django.urls import path

from .views import TagDetailView, TagListView


urlpatterns = [
    path('list', TagListView.as_view()),
    path('<int:pk>/detail', TagDetailView.as_view()),
]
