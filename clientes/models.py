from django.db import models
from django.utils import timezone

from config.choices import TipoDocumento
from envios.querysets import ClienteQuerySet


class Cliente(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    tipo_doc = models.CharField(
        max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.DNI
    )
    nro_doc = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)

    objects = ClienteQuerySet.as_manager()

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}".strip()

    @property
    def esta_activo(self) -> bool:
        return self.activo

    @property
    def total_encomiendas_enviadas(self) -> int:
        return self.encomiendas_enviadas.count()

    def __str__(self):
        return f"{self.nombre_completo} ({self.nro_doc})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["apellidos", "nombres"]
