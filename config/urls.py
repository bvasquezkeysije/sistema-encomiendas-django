from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Sistema de Gestión de Encomiendas"
admin.site.site_title = "Encomiendas Admin"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("", include("envios.urls")),
]
