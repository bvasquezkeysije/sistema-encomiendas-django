from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from clientes.models import Cliente
from rutas.models import Ruta

from .serializers import ClienteSerializer, RutaSerializer


class ClienteListAPIView(generics.ListAPIView):
    queryset = Cliente.objects.activos().order_by("apellidos", "nombres")
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["tipo_doc", "estado"]
    search_fields = ["nombres", "apellidos", "nro_doc"]


class RutaListAPIView(generics.ListAPIView):
    queryset = Ruta.objects.activas().order_by("origen", "destino")
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["estado", "origen", "destino"]
    search_fields = ["codigo", "origen", "destino"]
