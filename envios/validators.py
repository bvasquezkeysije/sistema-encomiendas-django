import re
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError


def validar_codigo_encomienda(value: str) -> None:
    if not re.fullmatch(r"ENC-\d{4}-\d{3,6}", value or ""):
        raise ValidationError("El codigo debe tener formato ENC-YYYY-NNN.")


def validar_peso_kg(value: Decimal) -> None:
    if value is None or value <= 0:
        raise ValidationError("El peso debe ser mayor a 0 kg.")


def validar_fecha_no_pasada(value: date) -> None:
    if value is not None and value < date.today():
        raise ValidationError("La fecha no puede estar en el pasado.")
