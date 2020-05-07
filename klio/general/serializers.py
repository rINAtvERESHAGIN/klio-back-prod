from django.contrib.auth import get_user_model

from cities_light.models import City
from rest_framework import serializers

from products.serializers import CategoryListSerializer, ProductListSerializer
from tags.serializers import TagSerializer
from .models import Article, Banner, Menu, MenuItem, Page, SubscriberInfo

User = get_user_model()


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%d.%m.%Y")
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'meta_title', 'meta_description', 'meta_keywords', 'title', 'slug', 'author', 'img', 'date',
                  'content', 'tags')

    def get_author(self, obj):
        return obj.author.__str__()


class ArticleListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Article
        fields = ('id', 'title', 'slug', 'img', 'date', 'abstract')


class BannerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


class CityListSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('value', 'text')

    def get_value(self, obj):
        if obj.id:
            return obj.id
        return None

    def get_text(self, obj):
        if obj.alternate_names:
            return obj.alternate_names
        return None


class MenuItemListSerializer(serializers.ModelSerializer):
    letter = serializers.SerializerMethodField('get_letter')
    path = serializers.SerializerMethodField('get_path')

    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'letter', 'slug', 'icon', 'path', 'related_type', 'link', 'children')

    def __init__(self, *args, **kwargs):
        super(MenuItemListSerializer, self).__init__(*args, **kwargs)
        self.temp_array = []

    def get_letter(self, obj):
        if not obj.parent and not obj.name[0].isdigit() and not obj.name[0] in self.temp_array:
            self.temp_array.append(obj.name[0])
            return obj.name[0]

    def get_fields(self):
        fields = super(MenuItemListSerializer, self).get_fields()
        fields['children'] = MenuItemListSerializer(many=True)
        return fields

    def get_path(self, obj):
        if obj.related_type == 'root':
            return obj.slug
        if obj.related_type == 'category':
            return '/catalog/categories/' + obj.slug
        if obj.related_type == 'products':
            return '/catalog/categories/' + obj.slug + '/products'
        if obj.related_type == 'page':
            return '/info/' + obj.slug
        if obj.related_type == 'article':
            return '/articles/' + obj.slug
        if obj.related_type == 'news':
            return '/news/' + obj.slug
        if obj.related_type == 'special':
            return '/specials/' + obj.slug
        if obj.related_type == 'external':
            return obj.link


class MenuListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Menu
        fields = ('id', 'items', 'name', 'position')

    def get_items(self, obj):
        items = MenuItem.objects.filter(menu=obj, activity=True, parent__isnull=True)
        serializer = MenuItemListSerializer(instance=items, many=True, context={"request": self.context.get('request')})
        return serializer.data


class NewsDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%d.%m.%Y")
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'meta_title', 'meta_description', 'meta_keywords', 'title', 'slug', 'author', 'img', 'date',
                  'content', 'tags')

    def get_author(self, obj):
        return obj.author.__str__()


class NewsListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Article
        fields = ('id', 'title', 'slug', 'img', 'date', 'abstract')


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('id', 'meta_title', 'meta_description', 'meta_keywords', 'name', 'slug', 'content')


class SearchDataSerializer(serializers.Serializer):
    categories = CategoryListSerializer(many=True)
    products = ProductListSerializer(many=True)
    articles = ArticleListSerializer(many=True)
    news = NewsListSerializer(many=True)
    counts = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.counts = kwargs.pop('counts')
        super().__init__(*args, **kwargs)

    def get_counts(self, obj):
        return self.counts


class SubscriberInfoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriberInfo
        fields = '__all__'
