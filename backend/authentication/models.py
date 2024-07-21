from django.db import models
from api.models import Helpers
from users.models import User


class PasswordResetCode(Helpers):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_store')
    activation_code = models.CharField(max_length=5)
    expires_at = models.DateTimeField()
