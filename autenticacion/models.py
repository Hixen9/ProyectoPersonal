from django.db import models

class Usuario(models.Model):
    username = models.CharField(max_length=255, unique=True)
    contraseña = models.CharField(max_length=20)

    def __str__(self):
        return self.username