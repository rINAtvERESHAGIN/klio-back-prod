from rest_framework import serializers

from tags.serializers import TagSerializer
from .models import Special


class SpecialDetailSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y")
    deadline = serializers.DateTimeField(format="%d.%m.%Y")
    tags = TagSerializer(many=True)

    class Meta:
        model = Special
        fields = ('id', 'name', 'slug', 'img', 'date', 'deadline', 'content', 'discount', 'discount_type',
                  'discount_amount', 'tags')


class SpecialListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y")
    deadline = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Special
        fields = ('id', 'name', 'slug', 'img', 'date', 'deadline')
