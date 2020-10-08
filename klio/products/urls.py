from django.urls import path

from .views import (BrandListView, CategoryDetailView, CategoryListView, CategoryMainListView, CategoryFilterListView,
                    CategoryProductListView, BrandDetailView, BrandFilterListView, BrandProductListView, FavoriteCreateView, FavoriteDeleteView, FavoriteListView,
                    ProductDetailView, ProductMainNewListView, ProductMainSpecialListView, SearchProductListView)


urlpatterns = [
    path('brands/list', BrandListView.as_view()),
    path('categories/list', CategoryListView.as_view()),
    path('categories/list/mainpage', CategoryMainListView.as_view()),
    path('categories/<str:slug>/detail', CategoryDetailView.as_view()),
    path('categories/<str:slug>/filters/list', CategoryFilterListView.as_view()),
    path('categories/<str:slug>/products/list', CategoryProductListView.as_view()),
    path('categories/<str:category_slug>/products/<str:slug>/detail', ProductDetailView.as_view()),
    path('brands/<str:slug>/detail', BrandDetailView.as_view()),
    path('brands/<str:slug>/filters/list', BrandFilterListView.as_view()),
    path('brands/<str:slug>/products/list', BrandProductListView.as_view()),
    path('favorites', FavoriteListView.as_view(), name='favorites'),
    path('favorites/<int:id>/add', FavoriteCreateView.as_view(), name='favorite_add'),
    path('favorites/<int:id>/delete', FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('list/mainpage/new', ProductMainNewListView.as_view()),
    path('list/mainpage/special', ProductMainSpecialListView.as_view()),
    path('search/list', SearchProductListView.as_view(), name='search_products_list'),
]
