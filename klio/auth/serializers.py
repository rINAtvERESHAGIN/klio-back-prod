from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=4,
                                     required=True, label=_('password'))
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

    def validate(self, data):
        user_query = User.objects.filter(email=data.get('email', None))
        if user_query.exists() and user_query.count() == 1:
            user = user_query.first()
            if user.check_password(data['password']):
                data['token'] = "RANDOM TOKEN"
                return data

        raise serializers.ValidationError(_('Incorrect email or password.'))


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
    last_name = serializers.CharField(required=False, label=_('last name'))
    first_name = serializers.CharField(required=True, label=_('first name'))
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=4,
                                     required=True, label=_('password'))
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True,
                                             label=_('password_confirm'))

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password', 'password_confirm', 'personal_data']

    def validate_personal_data(self, value):
        if not value:
            raise serializers.ValidationError(_('You must agree to the processing of personal data.'))
        return value

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        password = validated_data['password']
        password_confirm = validated_data['password_confirm']

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': _('User with this email already exists.')})

        if password != password_confirm:
            raise serializers.ValidationError({'password': [_('Passwords must match.')]})

        new_user = User(first_name=first_name, email=email)
        new_user.set_password(password)
        new_user.is_active = False
        new_user.save()
        new_user.username = 'user' + str(new_user.id)
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def get_activation_key(self, user):
        """
        Generate the activation key which will be emailed to the user.
        """
        return signing.dumps(obj=user.email, salt=settings.REGISTRATION_SALT)

    def get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.
        """
        scheme = "https" if self.context['request'].is_secure() else "http"
        return {
            "scheme": scheme,
            "activation_key": activation_key,
            "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
            "site": get_current_site(self.context['request']),
        }

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the email,
        signed using sha1.
        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(
            template_name="registration/activation_email_subject.txt",
            context=context,
            request=self.context['request'],
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = "".join(subject.splitlines())
        message = render_to_string(
            template_name="registration/activation_email_body.txt",
            context=context,
            request=self.context['request'],
        )
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
