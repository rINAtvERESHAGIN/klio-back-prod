from django.utils import timezone
from rest_framework import generics

from products.models import Product
from products.serializers import ProductListSerializer
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
    queryset = Special.objects.all()


class SpecialProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        sort_by = self.request.query_params.get('sortby')
        direction = self.request.query_params.get('direction')
        queryset = Product.objects.filter(activity=True, specials__slug=self.kwargs['slug']).order_by('name')
        if sort_by == 'name':
            if direction == 'desc':
                queryset = queryset.order_by('-name')
        if sort_by == 'price':
            if direction == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        return queryset
