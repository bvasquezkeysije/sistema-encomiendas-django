import re
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError


def validar_peso_positivo(value: Decimal) -> None:
    if value <= 0:
        raise ValidationError(f"El peso debe ser mayor a 0. Recibio: {value} kg")


def validar_codigo_encomienda(value: str) -> None:
    if not (value or "").startswith("ENC-"):
        raise ValidationError("El codigo de encomienda debe comenzar con ENC-.")
    if not re.fullmatch(r"ENC-[A-Za-z0-9\-]+", value or ""):
        raise ValidationError("El codigo de encomienda contiene caracteres invalidos.")


def validar_nro_doc_dni(value: str) -> None:
    if not value.isdigit() or len(value) != 8:
        raise ValidationError("El DNI debe contener exactamente 8 digitos numericos.")


def validar_peso_kg(value: Decimal) -> None:
    validar_peso_positivo(value)


def validar_fecha_no_pasada(value: date) -> None:
    if value is not None and value < date.today():
        raise ValidationError("La fecha no puede estar en el pasado.")
