from django.db.models import Max, Min
from django.utils.timezone import now, timedelta

from rest_framework import serializers

from sale.models import Special
from tags.serializers import TagSerializer
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
        fields = ('id', 'name', 'slug', 'meta_title', 'meta_description', 'meta_keywords', 'img', 'description',
                  'children', 'parent')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'img', 'children')


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('id', 'label', 'url')

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img.url)


class ProductPropertySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = ProductProperty
        fields = ('id', 'name', 'units', 'value')

    def get_value(self, obj):
        own_value = obj.values.get(product_id=self.context.get('product_id')).value
        if self.context.get('is_child') and not own_value:
            return obj.values.get(product_id=self.context.get('parent_id')).value
        return own_value

    def get_units(self, obj):
        if obj.units:
            return obj.units.name
        return None


class ProductListSerializer(serializers.ModelSerializer):
    base_amount = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'image', 'in_stock', 'art', 'base_amount', 'units', 'price',
                  'wholesale_threshold', 'wholesale_price', 'is_new', 'special')

    def get_base_amount(self, obj):
        return obj.get_base_amount()

    def get_category(self, obj):
        return obj.get_category().slug if obj.get_category() else 'no-category'

    def get_image(self, obj):
        return ProductImageSerializer(instance=obj.images.filter().first(),
                                      context={"request": self.context.get('request')}
                                      ).data

    def get_special(self, obj):
        result = {}
        special = None
        # TODO: do smth with selection of just the first special
        # First get private product special
        special_relation = obj.special_relations.filter(special__activity=True).first()
        if special_relation:
            special = special_relation.special
        # Else get special via category
        if not special:
            if obj.get_category():
                special = Special.objects.filter(categories__in=[obj.get_category().id]).first()
        # Or via tags
        if not special:
            tags_ids = [tag.id for tag in obj.tags.filter(activity=True)]
            special = Special.objects.filter(tags__in=tags_ids).first()

        if special:
            result['slug'] = special.slug
            result['threshold'] = special.threshold if special.threshold else 0
            if special_relation and special_relation.discount_amount:
                result['new_price'] = str(round(obj.price - special.discount_amount, 2))
                return result
            else:
                if special.discount_type == 'percent':
                    result['new_price'] = str(round(obj.price * (1 - special.discount_amount / 100), 2))
                elif special.special.discount_type == 'fixed':
                    result['new_price'] = str(round(obj.price - special.discount_amount, 2))
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

    def get_units(self, obj):
        if obj.get_units():
            return obj.get_units().name
        return None


class BasketProductListSerializer(ProductListSerializer):
    quantity = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ('quantity', 'current_price',)

    def get_current_price(self, obj):
        return obj.in_basket.get(basket_id=self.context.get('basket_id')).price

    def get_quantity(self, obj):
        return obj.in_basket.get(basket_id=self.context.get('basket_id')).quantity


class FilterListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()
    max = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = ProductProperty
        fields = ('name', 'slug', 'type', 'units', 'value', 'options', 'min', 'max', 'interval')

    def get_type(self, obj):
        if obj.type in ['integer', 'float']:
            return 'digit'
        return obj.type

    def get_options(self, obj):
        if obj.type == 'text':
            products_ids = self.context.get('products_ids')
            return obj.values.filter(product__in=products_ids).values_list('value_text', flat=True)
        return None

    def get_min(self, obj):
        if obj.type in ['integer', 'float']:
            products_ids = self.context.get('products_ids')
            return list(obj.values.filter(product__in=products_ids).aggregate(Min('value_%s' % obj.type)).values())[0]
        return None

    def get_max(self, obj):
        if obj.type in ['integer', 'float']:
            products_ids = self.context.get('products_ids')
            return list(obj.values.filter(product__in=products_ids).aggregate(Max('value_%s' % obj.type)).values())[0]
        return None

    def get_value(self, obj):
        if self.get_min(obj) and self.get_max(obj):
            return [self.get_min(obj), self.get_max(obj)]
        return None

    def get_units(self, obj):
        if obj.units:
            return obj.units.name
        return None


class ProductSerializer(serializers.ModelSerializer):
    base_amount = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True)
    is_new = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()
    recommended = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    units = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'meta_title', 'meta_description', 'meta_keywords', 'name', 'description', 'category', 'images',
                  'in_stock', 'art', 'tags', 'base_amount', 'price', 'units', 'wholesale_threshold', 'wholesale_price',
                  'is_new', 'special', 'properties', 'recommended')

    def get_base_amount(self, obj):
        return obj.get_base_amount()

    def get_category(self, obj):
        if obj.get_category():
            return SubCategorySerializer(obj.get_category()).data
        else:
            return None

    def get_is_new(self, obj):
        result = None
        if obj.is_new == 'new':
            result = True
        if obj.is_new == 'calculated':
            if obj.created > now() - timedelta(days=60):
                result = True
        return result

    def get_properties(self, obj):
        self.context['product_id'] = obj.id
        if obj.parent:
            self.context['parent_id'] = obj.parent.id
        self.context['is_child'] = obj.is_child
        return ProductPropertySerializer(obj.properties.all(), many=True, context=self.context).data

    def get_recommended(self, obj):
        return ProductListSerializer(obj.recommended.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]),
                                     many=True, context=self.context).data

    def get_special(self, obj):
        result = {}
        special = None
        # TODO: do smth with selection of just the first special
        # First get private product special
        special_relation = obj.special_relations.filter(special__activity=True).first()
        if special_relation:
            special = special_relation.special
        # Else get special via category
        if not special:
            if obj.get_category():
                special = Special.objects.filter(categories__in=[obj.get_category().id]).first()
        # Or via tags
        if not special:
            tags_ids = [tag.id for tag in obj.tags.filter(activity=True)]
            special = Special.objects.filter(tags__in=tags_ids).first()

        if special:
            result['slug'] = special.slug
            result['threshold'] = special.threshold if special.threshold else 0
            if special_relation and special_relation.discount_amount:
                result['new_price'] = str(round(obj.price - special.discount_amount, 2))
                return result
            else:
                if special.discount_type == 'percent':
                    result['new_price'] = str(round(obj.price * (1 - special.discount_amount / 100), 2))
                elif special.special.discount_type == 'fixed':
                    result['new_price'] = str(round(obj.price - special.discount_amount, 2))
            return result
        return None

    def get_units(self, obj):
        if obj.get_units():
            return obj.get_units().name
        return None
