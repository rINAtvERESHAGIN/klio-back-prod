from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Brand, Category, Product, UserProduct
from .serializers import (BrandListSerializer, CategorySerializer, CategoryListSerializer, ProductSerializer,
                          ProductListSerializer)


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


class CategoryProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DynamicPageNumberPagination

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


class FavoriteCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('id')

        favorite, _ = UserProduct.objects.get_or_create(user=self.request.user, product_id=product_id)

        favorites = Product.objects.filter(activity=True, selected_by__user=self.request.user)
        serializer = self.serializer_class(favorites, many=True, context={'request': self.request})
        return Response(serializer.data)


class FavoriteDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('id')

        favorite = get_object_or_404(UserProduct, user=self.request.user, product_id=product_id)
        self.perform_destroy(favorite)

        favorites = Product.objects.filter(activity=True, selected_by__user=self.request.user)
        serializer = self.serializer_class(favorites, many=True, context={'request': self.request})
        return Response(serializer.data)


class FavoriteListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(activity=True, selected_by__user=self.request.user)
        return queryset


class ProductDetailView(RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(activity=True)


class ProductMainNewListView(ListAPIView):
    serializer_class = ProductListSerializer
    new_product_period = datetime.today() - timedelta(days=60)
    queryset = Product.objects.filter(
        Q(activity=True, is_new='new') | Q(activity=True, is_new='calculated', created__gte=new_product_period)
    )[:20]


class ProductMainSpecialListView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.filter(activity=True,
                                      special_relations__special__activity=True,
                                      special_relations__on_main=True)[:20]


class SearchProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DynamicPageNumberPagination

    def get_queryset(self):
        text = self.request.query_params.get('text')
        sort_by = self.request.query_params.get('sortby')
        direction = self.request.query_params.get('direction')

        queryset = Product.objects.filter(activity=True).order_by('name')

        if text:
            queryset = queryset .filter(
                Q(name__icontains=text) | Q(art__icontains=text) | Q(category__name__icontains=text),
            )
        if sort_by == 'name':
            if direction == 'desc':
                queryset = queryset.order_by('-name')
        if sort_by == 'price':
            if direction == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        return queryset
