from django.contrib.auth import get_user_model

from rest_framework import serializers

from contacts.serializers import PhoneSerializer

from cities_light.models import City
User = get_user_model()


class CityRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        print(data)
        return self.get_queryset().get(pk=data)

    def to_representation(self, value):
        # print(type(value))
        return value.alternate_names



class UserDetailSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    birthday = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    # country = serializers.SerializerMethodField('get_country')
    phones = PhoneSerializer(many=True)
    city = CityRelatedField(queryset=City.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'middle_name', 'registered', 'birthday', 'email',
                  'city', 'address', 'last_login', 'phones', 'avatar')

        # def get_country(self, obj):
        #     if obj.country:
        #         return obj.country.alternate_names
