from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    registered = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField('get_city')
    country = serializers.SerializerMethodField('get_country')

    class Meta:
        model = User
        fields = '__all__'

    def get_city(self, obj):
        if obj.city:
            return obj.city.alternate_names

    def get_country(self, obj):
        if obj.country:
            return obj.country.name

    def get_date_joined(self, obj):
        return obj.date_joined

    def get_registered(self, obj):
        return obj.registered


class UserListSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField('get_city')

    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'city', 'email')

    def get_city(self, obj):
        if obj.city:
            return obj.city.alternate_names
