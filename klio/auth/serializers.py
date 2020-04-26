# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.sites.shortcuts import get_current_site
# from django.core import signing
# from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=4,
                                     required=True, label=_('password'))

    class Meta:
        model = User
        fields = ['email', 'password']


class PasswordResetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']


class PasswordSetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=4,
                                     required=True, label=_('password'))
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True,
                                             label=_('password_confirm'))

    class Meta:
        model = User
        fields = ['password', 'password_confirm']

    def update(self, instance, validated_data):
        password = validated_data['password']
        password_confirm = validated_data['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError({'password': [_('Passwords must match.')]})

        instance.set_password(password)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(required=True, label=_('last name'))
    first_name = serializers.CharField(required=True, label=_('first name'))
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=4,
                                     required=True, label=_('password'))
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True,
                                             label=_('password_confirm'))

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password', 'password_confirm', 'personal_data']

    def validate_personal_data(self, value):
        if not value:
            raise serializers.ValidationError(_('You must agree to the processing of personal data.'))
        return value

    def validate_password_confirm(self, value):
        if self.initial_data['password'] != value:
            raise serializers.ValidationError(_('Passwords must match.'))

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        new_user = User.objects.create(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.is_active = False
        new_user.username = 'user{0}'.format(new_user.id)
        new_user.save()
        return new_user
