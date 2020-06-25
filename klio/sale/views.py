from django.db.models import Q
from django.utils import timezone
from rest_framework import generics

from products.models import Product
from products.serializers import ProductListSerializer
from products.views import DynamicPageNumberPagination
from .models import Special
from .serializers import SpecialDetailSerializer, SpecialListSerializer


class SpecialListView(generics.ListAPIView):
    serializer_class = SpecialListSerializer
    queryset = Special.objects.filter(
        activity=True
    ).exclude(
        start_date__isnull=False, start_date__gt=timezone.localtime()
    ).exclude(
        deadline__isnull=False, deadline__lt=timezone.localtime()
    )


class SpecialDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = SpecialDetailSerializer
    queryset = Special.objects.filter(activity=True)


class SpecialProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DynamicPageNumberPagination

    def get_queryset(self):
        sort_by = self.request.query_params.get('sortby')
        direction = self.request.query_params.get('direction')
        special = Special.objects.filter(slug=self.kwargs['slug']).first()
        special_tags_ids = [tag.id for tag in special.tags.filter(activity=True)]
        queryset = Product.objects.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]).filter(
            Q(
                specials__in=[special.id]
            ) | Q(
                categories__in=special.categories.filter(activity=True)
            ) | Q(
                parent__categories__in=special.categories.filter(activity=True)
            ) | Q(
                tags__in=special_tags_ids
            )
        ).distinct().order_by('name')

        if sort_by == 'name':
            if direction == 'desc':
                queryset = queryset.order_by('-name')
        if sort_by == 'price':
            if direction == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        return queryset
