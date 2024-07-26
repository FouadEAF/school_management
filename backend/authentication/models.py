from django.db import models
from django.conf import settings


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=8, unique=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'{self.user.email} - {self.reset_code}'
