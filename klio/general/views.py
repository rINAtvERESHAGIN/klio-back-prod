from rest_framework import generics

from .models import Article, Banner, Menu, News
from .serializers import (ArticleDetailSerializer, ArticleListSerializer,
                          BannerDetailSerializer, BannerListSerializer,
                          MenuListSerializer, NewsDetailSerializer, NewsListSerializer)


class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleDetailSerializer


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(activity=True)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.all()


class BannerCreateView(generics.CreateAPIView):
    serializer_class = BannerDetailSerializer


class BannerListView(generics.ListAPIView):
    serializer_class = BannerListSerializer
    queryset = Banner.objects.filter(activity=True)


class BannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BannerDetailSerializer
    queryset = Banner.objects.all()


class MenuListView(generics.ListAPIView):
    serializer_class = MenuListSerializer
    queryset = Menu.objects.filter(activity=True)


class NewsCreateView(generics.CreateAPIView):
    serializer_class = NewsDetailSerializer


class NewsListView(generics.ListAPIView):
    serializer_class = NewsListSerializer
    queryset = News.objects.filter(activity=True)


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()
