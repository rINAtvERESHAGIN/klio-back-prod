from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .exceptions import ActivationError
from .serializers import LoginSerializer, PasswordResetSerializer, PasswordSetSerializer, RegistrationSerializer


class ActivationView(APIView):
    """
    Given a valid activation key, activate the user's account.
    Otherwise, show an error message stating the account couldn't be activated.
    """

    model = get_user_model()
    permission_classes = [AllowAny]

    SUCCESSFULLY_ACTIVATED_MESSAGE = _(
        "The account is successfully activated! Now you can log in."
    )
    ALREADY_ACTIVATED_MESSAGE = _(
        "The account you tried to activate has already been activated."
    )
    BAD_USERNAME_MESSAGE = _("The account you attempted to activate is invalid.")
    EXPIRED_MESSAGE = _("This account has expired.")
    INVALID_KEY_MESSAGE = _("The activation key you provided is invalid.")

    def get(self, request, *args, **kwargs):
        email = self.validate_key(kwargs.get("activation_key"))
        user = self.get_user(email)
        user.is_active = True
        user.save()
        return Response({'detail': self.SUCCESSFULLY_ACTIVATED_MESSAGE}, status=HTTP_200_OK)

    def validate_key(self, activation_key):
        """
        Verify that the activation key is valid and within the permitted activation
        time window, returning the email if valid or raising ``ActivationError`` if not.
        """
        try:
            email = signing.loads(
                activation_key,
                salt=settings.REGISTRATION_SALT,
                max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400,
            )
            return email
        except signing.SignatureExpired:
            raise ActivationError(self.EXPIRED_MESSAGE)
        except signing.BadSignature:
            raise ActivationError(self.INVALID_KEY_MESSAGE, params={"activation_key": activation_key})

    def get_user(self, email):
        """
        Given the verified username, look up and return the corresponding user
        account if it exists, or raising ``ActivationError`` if it doesn't.
        """

        try:
            user = self.model.objects.get(email=email)
            if user.is_active:
                raise ActivationError(self.ALREADY_ACTIVATED_MESSAGE)
            return user
        except self.model.DoesNotExist:
            raise ActivationError(self.BAD_USERNAME_MESSAGE)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):


class PasswordResetView(UpdateAPIView):

    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        data = request.data

        if not self.model.objects.filter(email=data.get('email')).exists():
            return Response({'email': _('User with this email does not exist.')}, status=HTTP_400_BAD_REQUEST)

        instance = self.model.objects.filter(email=data.get('email')).first()
        self.send_password_reset_email(instance, request)

        return Response(status=HTTP_200_OK)

    def get_reset_key(self, user):
        """
        Generate the reset key which will be emailed to the user.
        """
        return signing.dumps(obj=user.password, salt=settings.REGISTRATION_SALT)

    def get_email_context(self, reset_key, user, request):
        """
        Build the template context used for the reset email.
        """
        scheme = "https" if request.is_secure() else "http"
        return {
            "scheme": scheme,
            "reset_key": reset_key,
            "email": user.email,
            "user_id": user.id,
            "site": get_current_site(request),
        }

    def send_password_reset_email(self, user, request):
        """
        Send the password reset email. The reset key is the password,
        signed using sha1.
        """
        reset_key = self.get_reset_key(user)
        context = self.get_email_context(reset_key, user, request)
        context["user"] = user
        subject = render_to_string(
            template_name="registration/password_reset_email_subject.txt",
            context=context,
            request=request,
        )
        # Force subject to a single line to avoid header-injection issues.
        subject = "".join(subject.splitlines())
        message = render_to_string(
            template_name="registration/password_reset_email_body.txt",
            context=context,
            request=request,
        )
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class PasswordSetView(UpdateAPIView):
    """
    Given a valid reset key, allows to set new user's password.
    Otherwise, show an error message stating the password couldn't be reset.
    """

    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = PasswordSetSerializer

    SUCCESSFULLY_RESET_MESSAGE = _("The password is successfully reset! Now you can log in.")
    BAD_ACCOUNT_MESSAGE = _("The account you attempted to reset password for is invalid.")
    NOT_ACTIVATED_MESSAGE = _("The account you attempted to reset password for is not active.")
    EXPIRED_MESSAGE = _("The reset key has expired.")
    INVALID_KEY_MESSAGE = _("The reset key you provided is invalid.")

    def get_object(self):
        try:
            user = self.model.objects.get(id=self.kwargs.get("user_id"))
            if not user.is_active:
                raise ActivationError(self.NOT_ACTIVATED_MESSAGE)
            return user
        except self.model.DoesNotExist:
            raise ActivationError(self.BAD_ACCOUNT_MESSAGE)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        password = self.validate_key(self.kwargs.get("reset_key"))
        if user.password != password:
            raise ActivationError(self.INVALID_KEY_MESSAGE)
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self.SUCCESSFULLY_RESET_MESSAGE, status=HTTP_200_OK)

    def validate_key(self, reset_key):
        """
        Verify that the reset key is valid or raising ``ActivationError`` if not.
        """
        try:
            password = signing.loads(
                reset_key,
                salt=settings.REGISTRATION_SALT,
                max_age=settings.PASSWORD_RESET_DAYS * 86400,
            )
            return password
        except signing.SignatureExpired:
            raise ActivationError(self.EXPIRED_MESSAGE)
        except signing.BadSignature:
            raise ActivationError(self.INVALID_KEY_MESSAGE)


class RegistrationView(CreateAPIView):

    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
