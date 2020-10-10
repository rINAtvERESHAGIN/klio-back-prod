from datetime import datetime, timedelta
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import CharField, Q
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Brand, Category, Product, ProductProperty, ProductPropertyValue, UserProduct
from .serializers import (BrandListSerializer, CategoryCatalogSerializer, CategorySerializer, CategoryListSerializer, FilterListSerializer,
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
    serializer_class = CategoryCatalogSerializer
    queryset = Category.objects.filter(activity=True, parent__isnull=True)


class CategoryMainListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(activity=True, on_main=True)[:2]


class CategoryFilterListView(ListAPIView):
    serializer_class = FilterListSerializer

    def get_products_ids(self):
        # Get the category id
        categories_ids = list(Category.objects.filter(
            slug=self.kwargs['slug'], activity=True
        ).values_list('id', flat=True))
        if not categories_ids:
            return None

        # Get all nested categories ids
        parents = categories_ids
        children = True
        while children:
            children = list(Category.objects.filter(activity=True, parent_id__in=parents).values_list('id', flat=True))
            categories_ids += children
            parents = children

        # Get the products ids
        products_ids = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).filter(
            Q(categories__in=categories_ids) | Q(parent__categories__in=categories_ids)
        ).values_list('id', flat=True)
        return products_ids

    def get_queryset(self):
        queryset = ProductProperty.objects.filter(
            values__product__in=self.get_products_ids(), activity=True
        ).distinct()
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

        # Get the category id
        categories_ids = list(Category.objects.filter(
            activity=True, slug=self.kwargs['slug']
        ).values_list('id', flat=True))
        if not categories_ids:
            return []

        # Get all nested categories ids
        parents = categories_ids
        children = True
        while children:
            children = list(Category.objects.filter(activity=True, parent_id__in=parents).values_list('id', flat=True))
            categories_ids += children
            parents = children

        if not categories_ids:
            return []

        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.PARENT]).filter(
            Q(categories__in=categories_ids) | Q(parent__categories__in=categories_ids)
        )

        if not queryset:
            return []

        # Filtering block
        if in_stock:
            queryset = queryset.filter(in_stock__gt=0)

        for key, value in prop_filters.items():
            [prop_name, prop_type] = key.split("_")

            value = query_dict.get(key)
            value = True if value == 'true' else False if value == 'false' else value.split("|;|")

            # Filter by boolean type properties
            if prop_type == 'b' and value:
                pvs_ids = list(ProductPropertyValue.objects.filter(
                    prop__slug=prop_name, value_boolean=value).values_list('id', flat=True))
                queryset = queryset.filter(property_values__in=pvs_ids)

                # ids = [product.id for product in queryset if
                #        product.get_actual_value_by_property_slug(prop_name)]
                # queryset = queryset.filter(id__in=ids)

            # Filter by text (choices) type properties. Example: prop=['var1', 'var2', ...]
            if prop_type == 't':
                pvs_ids = list(ProductPropertyValue.objects.filter(
                    prop__slug=prop_name, value_text__in=value).values_list('id', flat=True))
                queryset = queryset.filter(property_values__in=pvs_ids)

                # ids = [product.id for product in queryset if
                #        product.get_actual_value_by_property_slug(prop_name) in value]
                # queryset = queryset.filter(id__in=ids)

            # Filter by digit (int/float) type properties. Example: prop=[100, 1090]
            if prop_type == 'd' and isinstance(value, list):
                value = value[0].split(',')
                # pvs_ids = list(ProductPropertyValue.objects.filter(
                #     Q(value_integer=value) | Q(value_float=value), prop__slug=prop_name).values_list('id', flat=True))
                # queryset = queryset.filter(property_values__in=pvs_ids)
                ids = [product.id for product in queryset if
                       float(value[0]) <= product.get_actual_value_by_property_slug(prop_name) <= float(value[1])]
                queryset = queryset.filter(id__in=ids)

        # Sorting block
        ordering = []
        if sort_by == 'name':
            if direction == 'asc':
                # queryset = queryset.order_by('name')
                ordering.append('name')
            if direction == 'desc':
                # queryset = queryset.order_by('-name')
                ordering.append('-name')
        if sort_by == 'price':
            if direction == 'desc':
                # queryset = queryset.order_by('-price')
                ordering.append('-price')
            else:
                # queryset = queryset.order_by('price')
                ordering.append('price')
        ordering.append('order')
        return queryset.order_by(*ordering)


class BrandDetailView(RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = BrandListSerializer
    queryset = Brand.objects.filter(activity=True)


class BrandFilterListView(ListAPIView):
    serializer_class = FilterListSerializer

    def get_products_ids(self):
        # Get the products ids
        products_ids = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.PARENT]).filter(
            brand__activity=True, brand__slug=self.kwargs['slug']
        ).values_list('id', flat=True)
        return products_ids

    def get_queryset(self):
        queryset = ProductProperty.objects.filter(
            values__product__in=self.get_products_ids(), activity=True
        ).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True,
                                           context={'request': self.request, 'products_ids': self.get_products_ids()})
        return Response(serializer.data)


class BrandProductListView(ListAPIView):
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
        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.PARENT]).filter(
            brand__activity=True, brand__slug=self.kwargs['slug']
        )
        if not queryset:
            return []
        # Filtering block
        if in_stock:
            queryset = queryset.filter(in_stock__gt=0)
        for key, value in prop_filters.items():
            [prop_name, prop_type] = key.split("_")
            value = query_dict.get(key)
            value = True if value == 'true' else False if value == 'false' else value.split("|;|")
            # Filter by boolean type properties
            if prop_type == 'b' and value:
                pvs_ids = list(ProductPropertyValue.objects.filter(
                    prop__slug=prop_name, value_boolean=value).values_list('id', flat=True))
                queryset = queryset.filter(property_values__in=pvs_ids)
            # Filter by text (choices) type properties. Example: prop=['var1', 'var2', ...]
            if prop_type == 't':
                pvs_ids = list(ProductPropertyValue.objects.filter(
                    prop__slug=prop_name, value_text__in=value).values_list('id', flat=True))
                queryset = queryset.filter(property_values__in=pvs_ids)
            # Filter by digit (int/float) type properties. Example: prop=[100, 1090]
            if prop_type == 'd' and isinstance(value, list):
                value = value[0].split(',')
                ids = [product.id for product in queryset if
                       float(value[0]) <= product.get_actual_value_by_property_slug(prop_name) <= float(value[1])]
                queryset = queryset.filter(id__in=ids)
        # Sorting block
        ordering = []
        if sort_by == 'name':
            if direction == 'asc':
                ordering.append('name')
            if direction == 'desc':
                ordering.append('-name')
        if sort_by == 'price':
            if direction == 'desc':
                ordering.append('-price')
            else:
                ordering.append('price')
        ordering.append('order')
        return queryset.order_by(*ordering)


class NewFilterListView(ListAPIView):
    serializer_class = FilterListSerializer

    def get_products_ids(self):
        # Get the products ids
        products_ids = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.PARENT]).filter(
            Q(is_new=Product.NEW) | Q(Q(is_new=Product.CALCULATED), Q(created__gte=datetime.now() - timedelta(days=60)))
        ).values_list('id', flat=True)
        return products_ids

    def get_queryset(self):
        queryset = ProductProperty.objects.filter(
            values__product__in=self.get_products_ids(), activity=True
        ).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True,
                                           context={'request': self.request, 'products_ids': self.get_products_ids()})
        return Response(serializer.data)


class NewProductListView(ListAPIView):
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
        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.PARENT]).filter(
            Q(is_new=Product.NEW) | Q(Q(is_new=Product.CALCULATED), Q(created__gte=datetime.now() - timedelta(days=60)))
        )
        if not queryset:
            return []
        # Filtering block
        if in_stock:
            queryset = queryset.filter(in_stock__gt=0)
        for key, value in prop_filters.items():
            [prop_name, prop_type] = key.split("_")
            value = query_dict.get(key)
            value = True if value == 'true' else False if value == 'false' else value.split("|;|")
            # Filter by boolean type properties
            if prop_type == 'b' and value:
                pvs_ids = list(ProductPropertyValue.objects.filter(
                    prop__slug=prop_name, value_boolean=value).values_list('id', flat=True))
                queryset = queryset.filter(property_values__in=pvs_ids)
            # Filter by text (choices) type properties. Example: prop=['var1', 'var2', ...]
            if prop_type == 't':
                pvs_ids = list(ProductPropertyValue.objects.filter(
                    prop__slug=prop_name, value_text__in=value).values_list('id', flat=True))
                queryset = queryset.filter(property_values__in=pvs_ids)
            # Filter by digit (int/float) type properties. Example: prop=[100, 1090]
            if prop_type == 'd' and isinstance(value, list):
                value = value[0].split(',')
                ids = [product.id for product in queryset if
                       float(value[0]) <= product.get_actual_value_by_property_slug(prop_name) <= float(value[1])]
                queryset = queryset.filter(id__in=ids)
        # Sorting block
        ordering = []
        if sort_by == 'name':
            if direction == 'asc':
                ordering.append('name')
            if direction == 'desc':
                ordering.append('-name')
        if sort_by == 'price':
            if direction == 'desc':
                ordering.append('-price')
            else:
                ordering.append('price')
        ordering.append('order')
        return queryset.order_by(*ordering)


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
        return Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, context={'request': self.request, 'category_slug': self.kwargs.get('category_slug')}
        )
        return Response(serializer.data)


class ProductMainNewListView(ListAPIView):
    serializer_class = ProductListSerializer

    # def list(self, request, *args, **kwargs):
    #     return Response(self.get_queryset())

    def get_queryset(self):

        # Get all active categories with only active parents ids
        categories_ids = list(Category.objects.filter(
            activity=True, parent__isnull=True
        ).distinct().values_list('id', flat=True))
        parents = categories_ids
        children = True
        while children:
            children = list(Category.objects.filter(
                activity=True, parent_id__in=parents
            ).distinct().values_list('id', flat=True))
            categories_ids += children
            parents = children

        active_child_categories_ids = list(Category.objects.filter(
            id__in=categories_ids, children__isnull=True
        ).distinct().values_list('id', flat=True))

        new_product_period = datetime.today() - timedelta(days=60)

        queryset = Product.objects.filter(
            Q(is_new='new') | Q(is_new='calculated', created__gte=new_product_period),
            activity=True, kind__in=[Product.UNIQUE, Product.CHILD], categories__in=active_child_categories_ids
        ).distinct()
        return queryset[:20]


class ProductMainSpecialListView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):

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

        queryset = Product.objects.filter(
            activity=True, kind__in=[Product.UNIQUE, Product.CHILD],
            special_relations__special__activity=True,
            special_relations__on_main=True
        ).filter(
            Q(categories__in=active_child_categories_ids) | Q(parent__categories__in=active_child_categories_ids)
        ).distinct()
        return queryset[:20]


class SearchProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DynamicPageNumberPagination

    def get_queryset(self):
        direction = self.request.query_params.get('direction')
        tags = self.request.query_params.get('tags')
        text = self.request.query_params.get('text')
        article = self.request.query_params.get('article')
        sort_by = self.request.query_params.get('sortby')

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

        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).filter(
            Q(categories__in=active_child_categories_ids) | Q(parent__categories__in=active_child_categories_ids)
        ).distinct().order_by('name')

        if text:
            queryset_art = queryset.annotate(
                similarity=TrigramSimilarity(Cast('art', CharField()), text)
            ).filter(similarity__gt=0.3)
            queryset_trgm = queryset.exclude(id__in=queryset_art.values_list('id', flat=True)).annotate(
                similarity=TrigramSimilarity('name', text)
            ).filter(similarity__gt=0.15)
            queryset = (queryset_art | queryset_trgm).order_by('-similarity')

        if tags:
            tags_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags_list)
        if article:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity(Cast('art', CharField()), article)
            ).filter(similarity__gt=0.7).order_by('-similarity')
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
