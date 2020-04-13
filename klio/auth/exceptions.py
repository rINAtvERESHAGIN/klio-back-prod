from rest_framework import status
from rest_framework.exceptions import APIException


class RegistrationError(APIException):
    """
    Base class for registration errors.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, message, code=None, params=None):
        self.detail = message
        if code is not None:
            self.status_code = code
        self.params = params


class ActivationError(RegistrationError):
    """
    Base class for account-activation errors.
    """

    pass
