from django.db import models

# Create your models here.

class Mahasiswa(models.Model):
    nim = models.IntegerField(unique=True)
    nama = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return f"{self.nim} {self.nama} {self.prodi} {self.email}"