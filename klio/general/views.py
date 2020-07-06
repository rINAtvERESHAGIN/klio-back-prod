from collections import namedtuple
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import EmailMessage
from django.db.models import IntegerField, Q, Value
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cities_light.models import City
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from products.models import Category, Product
from .models import Article, Banner, Menu, News, Page, SiteSettings
from .serializers import (ArticleDetailSerializer, ArticleListSerializer, BannerDetailSerializer,
                          BannerListSerializer, CityListSerializer, MenuListSerializer, NewsDetailSerializer,
                          NewsListSerializer, PageDetailSerializer, SearchDataSerializer, SiteDetailSerializer,
                          SubscriberInfoDetailSerializer)


class ArticleListView(ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(
        activity=True
    ).exclude(
        start_date__isnull=False, start_date__gt=timezone.localtime()
    ).exclude(
        deadline__isnull=False, deadline__lt=timezone.localtime()
    )


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.all()


class BannerListView(ListAPIView):
    serializer_class = BannerListSerializer
    queryset = Banner.objects.filter(
        activity=True
    ).exclude(
        start_date__isnull=False, start_date__gt=timezone.localtime()
    ).exclude(
        deadline__isnull=False, deadline__lt=timezone.localtime()
    )


class BannerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BannerDetailSerializer
    queryset = Banner.objects.all()


class CityListView(ListAPIView):
    serializer_class = CityListSerializer
    queryset = City.objects.all().exclude(alternate_names='null').order_by('alternate_names')


class MenuListView(ListAPIView):
    serializer_class = MenuListSerializer
    queryset = Menu.objects.filter(activity=True)


class NewsListView(ListAPIView):
    serializer_class = NewsListSerializer
    queryset = News.objects.filter(
        activity=True
    ).exclude(
        start_date__isnull=False, start_date__gt=timezone.localtime()
    ).exclude(
        deadline__isnull=False, deadline__lt=timezone.localtime()
    )


class NewsDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()


class PageDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = PageDetailSerializer
    queryset = Page.objects.filter(activity=True)


class SearchListView(ViewSet):
    SearchData = namedtuple('SearchData', ('categories', 'products', 'articles', 'news'))

    def list(self, request):
        tags = self.request.query_params.get('tags')
        text = self.request.query_params.get('text')
        obj_type = self.request.query_params.get('type')
        sort_by = self.request.query_params.get('sortby')
        direction = self.request.query_params.get('direction')

        # Get all active categories with only active parents ids
        categories_ids = list(Category.objects.filter(activity=True, parent__isnull=True).values_list('id', flat=True))
        parents = categories_ids
        children = True
        while children:
            children = list(Category.objects.filter(activity=True, parent_id__in=parents).values_list('id', flat=True))
            categories_ids += children
            parents = children

        active_child_categories_ids = list(Category.objects.filter(
            id__in=categories_ids, children__isnull=True
        ).values_list('id', flat=True))

        categories = Category.objects.filter(activity=True)
        products = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).filter(
            Q(categories__in=active_child_categories_ids) | Q(parent__categories__in=active_child_categories_ids)
        ).distinct().order_by('name')
        articles = Article.objects.filter(activity=True)
        news = News.objects.filter(activity=True)

        if text:
            categories = categories.annotate(
                similarity=TrigramSimilarity('name', text)
            ).filter(
                similarity__gt=0.15
            ).order_by('-similarity')

            products_art = products.annotate(
                similarity=Value(1, IntegerField())
            ).filter(art__icontains=text)
            products_trgm = products.exclude(id__in=products_art.values_list('id', flat=True)).annotate(
                similarity=TrigramSimilarity('name', text)
            ).filter(similarity__gt=0.15).order_by('-similarity')
            products = products_art | products_trgm

            articles = articles.annotate(
                similarity=TrigramSimilarity('title', text)
            ).filter(
                similarity__gt=0.15
            ).order_by('-similarity')

            news = news.annotate(
                similarity=TrigramSimilarity('title', text)
            ).filter(
                similarity__gt=0.15
            ).order_by('-similarity')

        if tags:
            tags_list = tags.split(',')
            # Need to get empty set of categories
            categories = categories.filter(id=0)
            products = products.filter(tags__name__in=tags_list)
            articles = articles.filter(tags__name__in=tags_list)
            news = news.filter(tags__name__in=tags_list)

        categories_count = categories.count()
        products_count = products.count()
        articles_count = articles.count()
        news_count = news.count()

        search_data = self.SearchData(
            categories=categories[:4], products=products[:8], articles=articles[:4], news=news[:4]
        )

        if obj_type:
            if obj_type == 'categories':
                if sort_by == 'name':
                    if direction == 'asc':
                        categories = categories.order_by('name')
                    if direction == 'desc':
                        categories = categories.order_by('-name')
                search_data = self.SearchData(categories=categories, products=None, articles=None, news=None)
            if obj_type == 'products':
                # if sort_by == 'name':
                #     if direction == 'asc':
                #         products = products.order_by('name')
                #     if direction == 'desc':
                #         products = products.order_by('-name')
                # if sort_by == 'price':
                #     if direction == 'desc':
                #         products = products.order_by('-price')
                #     else:
                #         products = products.order_by('price')
                # search_data = self.SearchData(categories=None, products=products, articles=None, news=None)
                search_data = self.SearchData(categories=None, products=None, articles=None, news=None)
            if obj_type == 'articles':
                if sort_by == 'title':
                    if direction == 'acs':
                        articles = articles.order_by('title')
                    if direction == 'desc':
                        articles = articles.order_by('-title')
                search_data = self.SearchData(categories=None, products=None, articles=articles, news=None)
            if obj_type == 'news':
                if sort_by == 'title':
                    if direction == 'acs':
                        news = news.order_by('title')
                    if direction == 'desc':
                        news = news.order_by('-title')
                search_data = self.SearchData(categories=None, products=None, articles=None, news=news)

        serializer = SearchDataSerializer(search_data, context={'request': request},
                                          counts={'categories': categories_count, 'products': products_count,
                                                  'articles': articles_count, 'news': news_count})
        return Response(serializer.data)


class SettingsDetailView(RetrieveAPIView):
    serializer_class = SiteDetailSerializer
    queryset = SiteSettings.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, activity=True)
        return obj


class SuscriberInfoCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SubscriberInfoDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if self.request.user:
            data['user'] = self.request.user.id

        serializer = self.serializer_class(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.create(validated_data=serializer.validated_data)
            self.admin_email_notification('new_subscription.html', data=serializer.validated_data)
            return Response(HTTP_200_OK)

    def admin_email_notification(self, template, subj='Письмо с сайта Klio!', **kwargs):
        html_content = render_to_string(template, {'kwargs': kwargs})
        from_email, to = 'Klio Website <pythonchem1st@gmail.com>', ['reactive.90@mail.ru']
        msg = EmailMessage(subj, html_content, from_email, to)
        msg.content_subtype = "html"
        msg.send()

    def email_confirm(self, template, **kwargs):
        html_content = render_to_string(template, kwargs)
        from_email, to = 'Klio AutoReply <pythonchem1st@gmail.com>', [kwargs['email']]
        msg = EmailMessage(_('Your Request Received!'), html_content, from_email, to)
        msg.content_subtype = "html"
        msg.send()
