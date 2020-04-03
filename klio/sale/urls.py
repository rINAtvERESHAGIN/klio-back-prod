from django.urls import path

from .views import SpecialDetailView, SpecialListView, SpecialProductListView


urlpatterns = [
    path('specials/list', SpecialListView.as_view()),
    path('specials/<str:slug>/detail', SpecialDetailView.as_view()),
    path('specials/<str:slug>/products/list', SpecialProductListView.as_view()),
]
