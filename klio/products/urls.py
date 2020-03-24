from django.urls import path

from .views import (BrandListView, CategoryDetailView, CategoryListView, CategoryMainListView, CategoryProductListView,
                    ProductDetailView, ProductMainNewListView, ProductMainSpecialListView)


urlpatterns = [
    path('brands/list', BrandListView.as_view()),
    path('categories/list', CategoryListView.as_view()),
    path('categories/list/mainpage', CategoryMainListView.as_view()),
    path('categories/<str:slug>/detail', CategoryDetailView.as_view()),
    path('categories/<str:slug>/products/list', CategoryProductListView.as_view()),
    path('categories/<str:categoty_slug>/products/<str:slug>/detail', ProductDetailView.as_view()),
    path('list/mainpage/new', ProductMainNewListView.as_view()),
    path('list/mainpage/special', ProductMainSpecialListView.as_view()),
]
