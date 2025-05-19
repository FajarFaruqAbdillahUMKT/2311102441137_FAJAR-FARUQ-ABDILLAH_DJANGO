from django.db import models
from django.contrib.auth.models import AbstractUser


class Mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.nama


# class Nilai(models.Model):
#     mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
#     mata_kuliah = models.CharField(max_length=100)
#     nilai = models.DecimalField(max_digits=5, decimal_places=2)
#
#     def __str__(self):
#         return f"{self.mahasiswa.nama} - {self.mata_kuliah} - {self.nilai}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
