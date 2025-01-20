from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

class Funcionario(AbstractUser):
    username = None
    email = models.EmailField(("email address"), unique=True)
    id_loja = models.IntegerField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email