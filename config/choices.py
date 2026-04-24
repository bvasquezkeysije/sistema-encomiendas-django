from django.db import models


class TipoDocumento(models.TextChoices):
    DNI = "DNI", "DNI"
    CE = "CE", "Carnet de Extranjeria"
    PAS = "PAS", "Pasaporte"


class EstadoEnvio(models.TextChoices):
    PENDIENTE = "PE", "Pendiente"
    EN_TRANSITO = "TR", "En transito"
    ENTREGADO = "EN", "Entregado"
    DEVUELTO = "DV", "Devuelto"
    CANCELADO = "CA", "Cancelado"
