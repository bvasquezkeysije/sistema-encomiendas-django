from django.contrib import admin

from .models import Empleado, Encomienda, HistorialEstado


@admin.register(Encomienda)
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "estado",
        "remitente",
        "destinatario",
        "ruta",
        "empleado_registro",
        "fecha_registro",
    )
    list_filter = ("estado", "ruta")
    search_fields = ("codigo", "descripcion", "remitente__nro_doc", "destinatario__nro_doc")


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombres", "apellidos", "nro_doc", "activo")
    list_filter = ("activo",)
    search_fields = ("nombres", "apellidos", "nro_doc")


@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ("id", "encomienda", "estado_anterior", "estado_nuevo", "fecha", "empleado")
    list_filter = ("estado_nuevo", "fecha")
    search_fields = ("encomienda__codigo", "observacion")
