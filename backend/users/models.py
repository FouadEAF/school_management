from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, cnie, email, password=None, **extra_fields):
        """ Create and return a regular user with a username, cnie, and email. """
        if not username:
            raise ValueError('The username field must be set')
        if not cnie:
            raise ValueError('The cnie field must be set')
        if not email:
            raise ValueError('The email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, cnie=cnie,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, cnie, email, password=None, **extra_fields):
        """ Create and return a superuser with a username, cnie, and email. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, cnie, email, password, **extra_fields)


class User(AbstractUser):
    cnie = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['cnie', 'email']

    def __str__(self):
        return self.username
