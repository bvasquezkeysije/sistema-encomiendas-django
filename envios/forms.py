from django import forms

from clientes.models import Cliente
from config.choices import EstadoGeneral
from rutas.models import Ruta

from .models import Encomienda


class EncomiendaForm(forms.ModelForm):
    class Meta:
        model = Encomienda
        fields = [
            "codigo",
            "descripcion",
            "peso_kg",
            "volumen_cm3",
            "remitente",
            "destinatario",
            "ruta",
            "empleado_registro",
            "estado",
            "fecha_entrega_est",
            "observaciones",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "peso_kg": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "volumen_cm3": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "remitente": forms.Select(attrs={"class": "form-select"}),
            "destinatario": forms.Select(attrs={"class": "form-select"}),
            "ruta": forms.Select(attrs={"class": "form-select"}),
            "empleado_registro": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "fecha_entrega_est": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remitente"].queryset = Cliente.objects.filter(estado=EstadoGeneral.ACTIVO)
        self.fields["destinatario"].queryset = Cliente.objects.filter(estado=EstadoGeneral.ACTIVO)
        self.fields["ruta"].queryset = Ruta.objects.filter(estado=EstadoGeneral.ACTIVO)
