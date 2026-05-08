from rest_framework import serializers

from clientes.models import Cliente
from rutas.models import Ruta

from .models import Empleado, Encomienda, HistorialEstado


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Cliente
        fields = [
            "id",
            "tipo_doc",
            "nro_doc",
            "nombres",
            "apellidos",
            "nombre_completo",
            "telefono",
            "email",
            "direccion",
            "estado",
            "activo",
        ]


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = [
            "id",
            "codigo",
            "origen",
            "destino",
            "descripcion",
            "precio_base",
            "dias_entrega",
            "estado",
            "distancia_km",
            "activa",
        ]


class HistorialEstadoSerializer(serializers.ModelSerializer):
    empleado = serializers.StringRelatedField()

    class Meta:
        model = HistorialEstado
        fields = [
            "id",
            "estado_anterior",
            "estado_nuevo",
            "observacion",
            "empleado",
            "fecha_cambio",
        ]


class EncomiendaSerializer(serializers.ModelSerializer):
    esta_entregada = serializers.ReadOnlyField()
    tiene_retraso = serializers.ReadOnlyField()
    dias_en_transito = serializers.ReadOnlyField()
    descripcion_corta = serializers.ReadOnlyField()
    estado_display = serializers.SerializerMethodField()

    class Meta:
        model = Encomienda
        fields = [
            "id",
            "codigo",
            "descripcion",
            "descripcion_corta",
            "peso_kg",
            "volumen_cm3",
            "costo_envio",
            "remitente",
            "destinatario",
            "ruta",
            "empleado_registro",
            "estado",
            "estado_display",
            "fecha_registro",
            "fecha_entrega_est",
            "fecha_entrega_real",
            "esta_entregada",
            "tiene_retraso",
            "dias_en_transito",
            "observaciones",
        ]
        read_only_fields = ["fecha_registro", "fecha_entrega_real", "empleado_registro"]

    def get_estado_display(self, obj):
        return obj.get_estado_display()


class EncomiendaDetailSerializer(EncomiendaSerializer):
    historial = HistorialEstadoSerializer(many=True, read_only=True)
    remitente_data = ClienteSerializer(source="remitente", read_only=True)
    destinatario_data = ClienteSerializer(source="destinatario", read_only=True)
    ruta_data = RutaSerializer(source="ruta", read_only=True)
    empleado_registro_data = serializers.StringRelatedField(source="empleado_registro", read_only=True)

    class Meta(EncomiendaSerializer.Meta):
        fields = EncomiendaSerializer.Meta.fields + [
            "historial",
            "remitente_data",
            "destinatario_data",
            "ruta_data",
            "empleado_registro_data",
        ]
