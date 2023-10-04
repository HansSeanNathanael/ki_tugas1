import json

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import EncryptionUserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    
    nama = models.CharField(max_length=64, default=None, blank=True, null=True)
    email = models.EmailField(max_length=254, default=None, blank=True, null=True)
    tanggal_lahir = models.DateField(default=None, blank=True, null=True)
    alamat = models.CharField(max_length=255, default=None, blank=True, null=True)
    nomor_telepon = models.CharField(max_length=16, default=None, blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = EncryptionUserManager()

    def __str__(self):
        return json.dumps({
            'id' : str(self.id),
            'username' : self.username
        }) 