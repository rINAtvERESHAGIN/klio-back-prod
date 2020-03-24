from django.utils.timezone import now, timedelta

from rest_framework import serializers

from tags.models import Tag
from .models import Brand, Category, Product, ProductImage, ProductProperty


class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'logo')


class SubCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'parent')

    def get_parent(self, obj):
        if obj.parent:
            return SubCategorySerializer(obj.parent).data
        else:
            return None


class CategorySerializer(serializers.ModelSerializer):
    parent = SubCategorySerializer()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'img', 'children', 'parent')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'img', 'children')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'label', 'img')


class ProductPropertySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = ProductProperty
        fields = ('id', 'name', 'units', 'value')

    def get_value(self, obj):
        value_obj = obj.values.first()
        field_name = 'value_' + obj.type
        return getattr(value_obj, field_name)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'image', 'in_stock', 'art', 'base_amount', 'price', 'is_new',
                  'special')

    def get_category(self, obj):
        return obj.category.slug if obj.category else 'no-category'

    def get_image(self, obj):
        return ProductImageSerializer(instance=obj.images.filter().first(),
                                      context={"request": self.context.get('request')}
                                      ).data

    def get_special(self, obj):
        result = {}
        main_special = obj.special_relations.filter(special__activity=True, on_main=True).first()
        if main_special:
            result['slug'] = main_special.special.slug
            if main_special.discount_amount:
                result['new_price'] = str(round(obj.price - main_special.discount_amount, 2))
                return result
            else:
                if main_special.special.discount_type == 'percent':
                    result['new_price'] = str(round(obj.price * (1 - main_special.special.discount_amount / 100), 2))
                elif main_special.special.discount_type == 'fixed':
                    result['new_price'] = str(round(obj.price - main_special.special.discount_amount, 2))
            return result
        return None

    def get_is_new(self, obj):
        result = None
        if obj.is_new == 'new':
            result = True
        if obj.is_new == 'calculated':
            if obj.created > now() - timedelta(days=60):
                result = True
        return result


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True)
    is_new = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    properties = ProductPropertySerializer(many=True)
    recommended = ProductListSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'images', 'in_stock', 'art', 'tags', 'base_amount', 'price',
                  'is_new', 'special', 'properties', 'recommended')

    def get_category(self, obj):
        if obj.category:
            return SubCategorySerializer(obj.category).data
        else:
            return None

    def get_special(self, obj):
        result = {}
        main_special = obj.special_relations.filter(special__activity=True, on_main=True).first()
        if main_special:
            result['slug'] = main_special.special.slug
            if main_special.discount_amount:
                result['new_price'] = str(round(obj.price - main_special.discount_amount, 2))
                return result
            else:
                if main_special.special.discount_type == 'percent':
                    result['new_price'] = str(round(obj.price * (1 - main_special.special.discount_amount / 100), 2))
                elif main_special.special.discount_type == 'fixed':
                    result['new_price'] = str(round(obj.price - main_special.special.discount_amount, 2))
            return result
        return None

    def get_is_new(self, obj):
        result = None
        if obj.is_new == 'new':
            result = True
        if obj.is_new == 'calculated':
            if obj.created > now() - timedelta(days=60):
                result = True
        return result
