from django.contrib.auth import get_user_model

from rest_framework import serializers

from contacts.serializers import PhoneSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    birthday = serializers.DateField(format="%Y-%m-%d")
    city = serializers.SerializerMethodField('get_city')
    country = serializers.SerializerMethodField('get_country')
    phones = PhoneSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'middle_name', 'registered', 'birthday', 'email',
                  'country', 'city', 'address', 'last_login', 'phones', 'avatar')

    def get_city(self, obj):
        if obj.city:
            return obj.city.alternate_names

    def get_country(self, obj):
        if obj.country:
            return obj.country.alternate_names
