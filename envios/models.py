from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from clientes.models import Cliente
from config.choices import EstadoEnvio
from rutas.models import Ruta

from .querysets import EncomiendaQuerySet
from .validators import (
    validar_codigo_encomienda,
    validar_fecha_no_pasada,
    validar_peso_kg,
)


class Empleado(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    nro_doc = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    rutas_asignadas = models.ManyToManyField(Ruta, blank=True, related_name="empleados")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}".strip()

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ["apellidos", "nombres"]


class Encomienda(models.Model):
    codigo = models.CharField(
        max_length=20, unique=True, validators=[validar_codigo_encomienda]
    )
    remitente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="encomiendas_enviadas"
    )
    destinatario = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="encomiendas_recibidas"
    )
    ruta = models.ForeignKey(
        Ruta, on_delete=models.PROTECT, related_name="encomiendas"
    )
    empleado_registro = models.ForeignKey(
        Empleado, on_delete=models.PROTECT, related_name="encomiendas_registradas"
    )
    descripcion = models.CharField(max_length=255)
    peso_kg = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[validar_peso_kg]
    )
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=2, choices=EstadoEnvio.choices, default=EstadoEnvio.PENDIENTE
    )
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)
    fecha_entrega_estimada = models.DateField(
        null=True, blank=True, validators=[validar_fecha_no_pasada]
    )
    fecha_entrega_real = models.DateField(null=True, blank=True)

    objects = EncomiendaQuerySet.as_manager()

    def clean(self):
        errors = {}
        if self.remitente_id and self.destinatario_id and self.remitente_id == self.destinatario_id:
            errors["destinatario"] = "El destinatario debe ser distinto al remitente."

        if self.fecha_entrega_estimada and self.fecha_entrega_estimada < timezone.localdate():
            errors["fecha_entrega_estimada"] = "La fecha estimada no puede estar en el pasado."

        if self.fecha_entrega_real and self.fecha_entrega_estimada:
            if self.fecha_entrega_real < self.fecha_entrega_estimada:
                errors["fecha_entrega_real"] = "La fecha real no puede ser menor a la fecha estimada."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def esta_entregada(self) -> bool:
        return self.estado == EstadoEnvio.ENTREGADO

    @property
    def tiene_retraso(self) -> bool:
        if not self.fecha_entrega_estimada:
            return False
        if self.estado == EstadoEnvio.ENTREGADO and self.fecha_entrega_real:
            return self.fecha_entrega_real > self.fecha_entrega_estimada
        return (
            self.estado in {EstadoEnvio.PENDIENTE, EstadoEnvio.EN_TRANSITO}
            and timezone.localdate() > self.fecha_entrega_estimada
        )

    @property
    def dias_en_transito(self) -> int:
        base = self.fecha_registro.date()
        fin = self.fecha_entrega_real or timezone.localdate()
        return max((fin - base).days, 0)

    @property
    def descripcion_corta(self) -> str:
        return (
            self.descripcion if len(self.descripcion) <= 60 else f"{self.descripcion[:57]}..."
        )

    def cambiar_estado(self, nuevo_estado: str, empleado=None, observacion: str = ""):
        estado_anterior = self.estado
        self.estado = nuevo_estado
        if nuevo_estado == EstadoEnvio.ENTREGADO and not self.fecha_entrega_real:
            self.fecha_entrega_real = timezone.localdate()
        self.save()
        HistorialEstado.objects.create(
            encomienda=self,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            empleado=empleado,
            observacion=observacion,
        )
        return self

    @classmethod
    def crear_con_costo_calculado(
        cls,
        *,
        codigo: str,
        remitente: Cliente,
        destinatario: Cliente,
        ruta: Ruta,
        empleado_registro: Empleado,
        descripcion: str,
        peso_kg: Decimal,
        fecha_entrega_estimada=None,
    ):
        costo_base = Decimal("8.00")
        costo_distancia = Decimal(ruta.distancia_km) * Decimal("0.06")
        costo_peso = Decimal(peso_kg) * Decimal("1.30")
        costo_total = (costo_base + costo_distancia + costo_peso).quantize(Decimal("0.01"))
        return cls.objects.create(
            codigo=codigo,
            remitente=remitente,
            destinatario=destinatario,
            ruta=ruta,
            empleado_registro=empleado_registro,
            descripcion=descripcion,
            peso_kg=peso_kg,
            costo_envio=costo_total,
            fecha_entrega_estimada=fecha_entrega_estimada,
        )

    def __str__(self):
        return f"{self.codigo} - {self.get_estado_display()}"

    class Meta:
        verbose_name = "Encomienda"
        verbose_name_plural = "Encomiendas"
        ordering = ["-fecha_registro"]


class HistorialEstado(models.Model):
    encomienda = models.ForeignKey(
        Encomienda, on_delete=models.CASCADE, related_name="historial_estados"
    )
    estado_anterior = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    estado_nuevo = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    fecha = models.DateTimeField(default=timezone.now, editable=False)
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name="historiales_creados",
        null=True,
        blank=True,
    )
    observacion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.encomienda.codigo}: {self.estado_anterior} -> {self.estado_nuevo}"

    class Meta:
        verbose_name = "Historial de estado"
        verbose_name_plural = "Historiales de estado"
        ordering = ["-fecha"]
