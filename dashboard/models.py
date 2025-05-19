from django.db import models

# Create your models here.
import dashboard


# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
# class CustomUser(AbstractUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, unique=True)  # Wajib pakai email kampus 2311102440001@umkt.ac.id
#     password = models.CharField(max_length=100)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
# from django.db import models

# Create your models here.

from django.db import models


class Mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    # Tambahkan field lain sesuai kebutuhan

    def __str__(self):
        return self.nama