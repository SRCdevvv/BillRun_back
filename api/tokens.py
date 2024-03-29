from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationToken(PasswordResetTokenGenerator):
# PasswordResetTokenGenerator 의 내장 함수를 불러온다.
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp)) + text_type(user.is_active)

account_activation_token = AccountActivationToken()