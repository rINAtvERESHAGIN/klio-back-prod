from django.contrib.auth import get_user_model

from rest_framework import serializers

from contacts.serializers import PhoneSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    birthday = serializers.DateField(format="%Y-%m-%d")
    # country = serializers.SerializerMethodField('get_country')
    phones = PhoneSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'middle_name', 'registered', 'birthday', 'email',
                  'city', 'address', 'last_login', 'phones', 'avatar')

        # def get_country(self, obj):
        #     if obj.country:
        #         return obj.country.alternate_names
