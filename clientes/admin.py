from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombres", "apellidos", "nro_doc", "activo")
    list_filter = ("activo", "tipo_doc")
    search_fields = ("nombres", "apellidos", "nro_doc")
