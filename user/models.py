from django.db import models

from autentikasi.models import User

# Create your models here.
class File(models.Model):
    id = models.UUIDField(primary_key=True)
    id_user= models.ForeignKey(User, on_delete=models.CASCADE)
    nama_file = models.CharField(max_length=255)
    nama_file_fisik = models.CharField(max_length=255)