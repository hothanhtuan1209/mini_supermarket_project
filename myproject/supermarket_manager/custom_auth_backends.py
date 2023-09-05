from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from .models import Account


class EmailBackend(ModelBackend):
    """
    Custom authentication backend for email-based authentication.

    This backend allows users to authenticate using their email address
    and password, instead of the default username and password.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
