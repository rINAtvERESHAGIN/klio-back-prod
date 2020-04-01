from datetime import datetime, timedelta
from django.db.models import Q

from rest_framework import generics

from .models import Brand, Category, Product
from .serializers import (BrandListSerializer, CategorySerializer, CategoryListSerializer, ProductSerializer,
                          ProductListSerializer)


class BrandListView(generics.ListAPIView):
    serializer_class = BrandListSerializer
    queryset = Brand.objects.filter(activity=True)


class CategoryDetailView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(activity=True)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(activity=True)


class CategoryMainListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(activity=True, on_main=True)


class CategoryProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        sort_by = self.request.query_params.get('sortby')
        direction = self.request.query_params.get('direction')
        queryset = Product.objects.filter(activity=True, category__slug=self.kwargs['slug']).order_by('name')
        if sort_by == 'name':
            if direction == 'desc':
                queryset = queryset.order_by('-name')
        if sort_by == 'price':
            if direction == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(activity=True)


class ProductMainNewListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    new_product_period = datetime.today() - timedelta(days=60)
    queryset = Product.objects.filter(
        Q(activity=True, is_new='new') | Q(activity=True, is_new='calculated', created__gte=new_product_period)
    )


class ProductMainSpecialListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.filter(activity=True,
                                      special_relations__special__activity=True,
                                      special_relations__on_main=True)
