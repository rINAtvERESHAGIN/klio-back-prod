from django.urls import path

from .views import (ArticleDetailView, ArticleListView, BannerDetailView, BannerListView,
                    MenuListView, NewsDetailView, NewsListView, PageDetailView, SuscriberInfoCreateView)


urlpatterns = [
    path('articles/list', ArticleListView.as_view()),
    path('articles/<str:slug>/detail', ArticleDetailView.as_view()),
    path('banners/list', BannerListView.as_view()),
    path('banners/<int:pk>/detail', BannerDetailView.as_view()),
    path('menu/list', MenuListView.as_view()),
    path('news/list', NewsListView.as_view()),
    path('news/<str:slug>/detail', NewsDetailView.as_view()),
    path('pages/<str:slug>/detail', PageDetailView.as_view()),
    path('subscribe', SuscriberInfoCreateView.as_view()),
]
