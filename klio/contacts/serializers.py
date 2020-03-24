from rest_framework import serializers

from .models import Contact, Phone, SocialNet, WorkingHours


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = '__all__'


class WorkingHoursSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingHours
        fields = ('id', 'label', 'time')


class ContactDetailSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField('get_city')
    country = serializers.SerializerMethodField('get_country')

    class Meta:
        model = Contact
        fields = '__all__'

    def get_city(self, obj):
        return obj.city.name

    def get_country(self, obj):
        return obj.country.name


class ContactListSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True)
    hours = WorkingHoursSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'name', 'slug', 'address', 'email', 'phones', 'hours', 'content', 'map')


class SocialListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialNet
        fields = ('name', 'img', 'url')
