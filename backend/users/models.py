# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, cnie, password=None, **extra_fields):
        """ Create and return a regular user with a username and cnie. """
        if not username:
            raise ValueError('The username field must be set')
        if not cnie:
            raise ValueError('The cnie field must be set')

        user = self.model(username=username, cnie=cnie, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, cnie, password=None, **extra_fields):
        """ Create and return a superuser with a username and cnie. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, cnie, password, **extra_fields)


class User(AbstractUser):
    cnie = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=50)
    security_question = models.CharField(max_length=255, blank=True, null=True)
    security_answer = models.CharField(max_length=255, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['cnie']

    def __str__(self):
        return self.username
