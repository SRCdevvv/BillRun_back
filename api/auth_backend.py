from django.contrib.auth.backends import ModelBackend
from .models import BillrunUser


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(phone=None):
        try:
            return BillrunUser.objects.get(phone=phone)
        except BillrunUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return BillrunUser.objects.get(id=user_id)
        except BillrunUser.DoesNotExist:
            return None