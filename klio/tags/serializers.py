from rest_framework import serializers

from .models import Tag


class TagDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')
