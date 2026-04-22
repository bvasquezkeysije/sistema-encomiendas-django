from django.db import models


class Cliente(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}".strip()
