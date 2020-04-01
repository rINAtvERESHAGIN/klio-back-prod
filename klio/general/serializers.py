from django.contrib.auth import get_user_model

from rest_framework import serializers

from products.serializers import CategoryListSerializer, ProductListSerializer
from .models import Article, Banner, Menu, MenuItem, News

User = get_user_model()


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):

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


class MenuItemListSerializer(serializers.ModelSerializer):
    letter = serializers.SerializerMethodField('get_letter')

    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'letter', 'slug', 'related_type', 'link', 'children')

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


class MenuListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Menu
        fields = ('id', 'items', 'name', 'position')

    def get_items(self, obj):
        items = MenuItem.objects.filter(menu=obj, activity=True, parent__isnull=True)
        serializer = MenuItemListSerializer(instance=items, many=True)
        return serializer.data


class NewsDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = '__all__'


class NewsListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'date', 'author')

    def get_author(self, obj):
        return obj.author.__str__()


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
