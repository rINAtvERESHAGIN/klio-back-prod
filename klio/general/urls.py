from django.urls import path

from .views import (ArticleCreateView, ArticleDetailView, ArticleListView,
                    BannerCreateView, BannerDetailView, BannerListView,
                    MenuListView, NewsCreateView, NewsDetailView, NewsListView)


urlpatterns = [
    path('articles/create', ArticleCreateView.as_view()),
    path('articles/list', ArticleListView.as_view()),
    path('articles/<int:pk>/detail', ArticleDetailView.as_view()),

    path('banners/create', BannerCreateView.as_view()),
    path('banners/list', BannerListView.as_view()),
    path('banners/<int:pk>/detail', BannerDetailView.as_view()),

    path('menu/list', MenuListView.as_view()),

    path('news/create', NewsCreateView.as_view()),
    path('news/list', NewsListView.as_view()),
    path('news/<int:pk>/detail', NewsDetailView.as_view()),
]
