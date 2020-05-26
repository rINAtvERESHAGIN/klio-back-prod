from datetime import datetime, timedelta
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Brand, Category, Product, ProductProperty, UserProduct
from .serializers import (BrandListSerializer, CategorySerializer, CategoryListSerializer, FilterListSerializer,
                          ProductSerializer, ProductListSerializer)


class DynamicPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 100


class BrandListView(ListAPIView):
    serializer_class = BrandListSerializer
    queryset = Brand.objects.filter(activity=True)


class CategoryDetailView(RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(activity=True)


class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(activity=True)


class CategoryMainListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(activity=True, on_main=True)[:2]


class CategoryFilterListView(ListAPIView):
    serializer_class = FilterListSerializer

    def get_products_ids(self):
        products_ids = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).filter(
            Q(category__slug=self.kwargs['slug']) | Q(parent__category__slug=self.kwargs['slug'])
        ).values_list('id', flat=True)
        return products_ids

    def get_queryset(self):
        queryset = ProductProperty.objects.filter(values__product__in=self.get_products_ids()).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True,
                                           context={'request': self.request, 'products_ids': self.get_products_ids()})
        return Response(serializer.data)


class CategoryProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DynamicPageNumberPagination

    def get_queryset(self):
        query_dict = self.request.query_params.copy()
        sort_by = query_dict.get('sortby')
        direction = query_dict.get('direction', None)
        in_stock = query_dict.get('in_stock', None)
        for k in ('sortby', 'direction', 'size', 'page', 'in_stock'):
            query_dict.pop(k, None)
        prop_filters = query_dict

        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).filter(
            Q(category__slug=self.kwargs['slug']) | Q(parent__category__slug=self.kwargs['slug'])
        ).order_by('name')

        # Filtering block
        if in_stock:
            queryset = queryset.filter(in_stock__gt=0)

        for key, value in prop_filters.items():
            [prop_name, prop_type] = key.split("_")

            value = query_dict.get(key)
            value = True if value == 'true' else value.split(",")

            # Filter by boolean type properties
            if prop_type == 'b' and value:
                ids = [product.id for product in queryset if
                       product.get_actual_value_by_property_slug(prop_name)]
                queryset = queryset.filter(id__in=ids)

            # Filter by text (choices) type properties. Example: prop=['var1', 'var2', ...]
            if prop_type == 't':
                ids = [product.id for product in queryset if
                       product.get_actual_value_by_property_slug(prop_name) in value]
                queryset = queryset.filter(id__in=ids)

            # Filter by digit (int/float) type properties. Example: prop=[100, 1090]
            if prop_type == 'd' and isinstance(value, list):
                ids = [product.id for product in queryset if
                       float(value[0]) <= product.get_actual_value_by_property_slug(prop_name) <= float(value[1])]
                queryset = queryset.filter(id__in=ids)

        # Sorting block
        if sort_by == 'name':
            if direction == 'desc':
                queryset = queryset.order_by('-name')
        if sort_by == 'price':
            if direction == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        return queryset


class FavoriteCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('id')

        favorite, _ = UserProduct.objects.get_or_create(user=self.request.user, product_id=product_id)

        favorites = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD],
                                           selected_by__user=self.request.user)
        serializer = self.serializer_class(favorites, many=True, context={'request': self.request})
        return Response(serializer.data)


class FavoriteDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('id')

        favorite = get_object_or_404(UserProduct, user=self.request.user, product_id=product_id)
        self.perform_destroy(favorite)

        favorites = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD],
                                           selected_by__user=self.request.user)
        serializer = self.serializer_class(favorites, many=True, context={'request': self.request})
        return Response(serializer.data)


class FavoriteListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD],
                                          selected_by__user=self.request.user)
        return queryset


class ProductDetailView(RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(activity=True, category__slug=self.kwargs.get('category_slug'),
                                      kind__in=[Product.UNIQUE, Product.CHILD])


class ProductMainNewListView(ListAPIView):
    serializer_class = ProductListSerializer
    new_product_period = datetime.today() - timedelta(days=60)
    queryset = Product.objects.filter(
        Q(activity=True, is_new='new', kind__in=[Product.UNIQUE, Product.CHILD]) | Q(
            activity=True, is_new='calculated', created__gte=new_product_period,
            kind__in=[Product.UNIQUE, Product.CHILD]
        )
    )[:20]


class ProductMainSpecialListView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.filter(activity=True,
                                      kind__in=[Product.UNIQUE, Product.CHILD],
                                      special_relations__special__activity=True,
                                      special_relations__on_main=True)[:20]


class SearchProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DynamicPageNumberPagination

    def get_queryset(self):
        direction = self.request.query_params.get('direction')
        tags = self.request.query_params.get('tags')
        text = self.request.query_params.get('text')
        sort_by = self.request.query_params.get('sortby')

        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).order_by('name')

        if text:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('name', text)
            ).filter(
                Q(similarity__gt=0.1) | Q(art__icontains=text)
            ).order_by('-similarity')
        if tags:
            tags_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags_list)
        if sort_by == 'name':
            if direction == 'asc':
                queryset = queryset.order_by('name')
            if direction == 'desc':
                queryset = queryset.order_by('-name')
        if sort_by == 'price':
            if direction == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        return queryset
