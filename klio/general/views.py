from collections import namedtuple
from django.db.models import Q

from rest_framework import generics, viewsets
from rest_framework.response import Response

from products.models import Category, Product
from .models import Article, Banner, Menu, News
from .serializers import (ArticleDetailSerializer, ArticleListSerializer, BannerDetailSerializer,
                          BannerListSerializer, MenuListSerializer, NewsDetailSerializer, NewsListSerializer,
                          SearchDataSerializer)


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


class SearchListView(viewsets.ViewSet):
    SearchData = namedtuple('SearchData', ('categories', 'products', 'articles', 'news'))

    def list(self, request):
        text = self.request.query_params.get('text')
        obj_type = self.request.query_params.get('type')
        sort_by = self.request.query_params.get('sortby')
        direction = self.request.query_params.get('direction')

        categories = Category.objects.filter(activity=True)
        products = Product.objects.filter(activity=True)
        articles = Article.objects.filter(activity=True)
        news = News.objects.filter(activity=True)

        if text:
            categories = categories.filter(
                name__icontains=text
            )
            products = products.filter(
                Q(name__icontains=text) | Q(art__icontains=text) | Q(category__name__icontains=text),
            )
            articles = articles.filter(
                Q(title__icontains=text) | Q(tags__name__icontains=text) | Q(content__icontains=text),
            )
            news = news.filter(
                Q(title__icontains=text) | Q(tags__name__icontains=text) | Q(content__icontains=text),
            )

        categories_count = categories.count()
        products_count = products.count()
        articles_count = articles.count()
        news_count = news.count()

        search_data = self.SearchData(
            categories=categories[:4], products=products[:8], articles=articles[:4], news=news[:4]
        )

        if obj_type:
            if obj_type == 'categories':
                categories = categories.order_by('-name') if direction == 'desc' else categories.order_by('name')
                search_data = self.SearchData(categories=categories, products=None, articles=None, news=None)
            if obj_type == 'products':
                products = products.order_by('name')
                if sort_by == 'name':
                    if direction == 'desc':
                        products = products.order_by('-name')
                if sort_by == 'price':
                    if direction == 'desc':
                        products = products.order_by('-price')
                    else:
                        products = products.order_by('price')
                search_data = self.SearchData(categories=None, products=products, articles=None, news=None)
            if obj_type == 'articles':
                articles = (articles.order_by('-title') if sort_by == 'title' and direction == 'desc'
                            else articles.order_by('title'))
                search_data = self.SearchData(categories=None, products=None, articles=articles, news=None)
            if obj_type == 'news':
                news = (news.order_by('-title') if sort_by == 'title' and direction == 'desc'
                        else news.order_by('title'))
                search_data = self.SearchData(categories=None, products=None, articles=None, news=news)

        serializer = SearchDataSerializer(search_data, context={'request': request},
                                          counts={'categories': categories_count, 'products': products_count,
                                                  'articles': articles_count, 'news': news_count})
        return Response(serializer.data)
