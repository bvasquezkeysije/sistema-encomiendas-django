from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Empleado, Encomienda
from .serializers import EncomiendaDetailSerializer, EncomiendaSerializer


class EncomiendaViewSet(viewsets.ModelViewSet):
    queryset = Encomienda.objects.con_relaciones()
    serializer_class = EncomiendaSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["estado", "ruta", "remitente", "destinatario"]
    search_fields = ["codigo", "descripcion", "remitente__apellidos", "destinatario__apellidos"]
    ordering_fields = ["fecha_registro", "fecha_entrega_est", "costo_envio", "peso_kg"]
    ordering = ["-fecha_registro"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EncomiendaDetailSerializer
        return EncomiendaSerializer

    def perform_create(self, serializer):
        empleado = Empleado.objects.filter(email=self.request.user.email).first()
        if not empleado:
            raise ValidationError(
                "No existe un empleado activo asociado al email del usuario autenticado."
            )
        serializer.save(empleado_registro=empleado)

    @action(detail=True, methods=["post"], url_path="cambiar_estado")
    def cambiar_estado(self, request, pk=None):
        enc = self.get_object()
        nuevo_estado = request.data.get("estado")
        observacion = request.data.get("observacion", "")

        if not nuevo_estado:
            return Response(
                {"error": "El campo estado es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            empleado = Empleado.objects.filter(email=request.user.email).first()
            if not empleado:
                return Response(
                    {"error": "No existe un empleado asociado al usuario autenticado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            enc.cambiar_estado(nuevo_estado, empleado, observacion)
            return Response(EncomiendaSerializer(enc).data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="con_retraso")
    def con_retraso(self, request):
        qs = Encomienda.objects.con_retraso().con_relaciones()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="pendientes")
    def pendientes(self, request):
        qs = Encomienda.objects.pendientes().con_relaciones()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
