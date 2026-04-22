from django.db import models


class Ruta(models.Model):
    origen = models.CharField(max_length=120)
    destino = models.CharField(max_length=120)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.origen} -> {self.destino}"
