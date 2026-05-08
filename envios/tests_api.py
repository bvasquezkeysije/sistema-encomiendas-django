from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from clientes.models import Cliente
from config.choices import EstadoGeneral, TipoDocumento
from envios.models import Empleado, Encomienda
from rutas.models import Ruta


class EncomiendaApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="apiuser",
            email="apiuser@encomiendas.local",
            password="ApiPass123!",
        )
        self.empleado = Empleado.objects.create(
            codigo="EMPAPI",
            nombres="Api",
            apellidos="User",
            email="apiuser@encomiendas.local",
            estado=EstadoGeneral.ACTIVO,
            fecha_ingreso=date.today(),
        )
        self.remitente = Cliente.objects.create(
            tipo_doc=TipoDocumento.DNI,
            nro_doc="12312312",
            nombres="Carlos",
            apellidos="Remitente",
            estado=EstadoGeneral.ACTIVO,
        )
        self.destinatario = Cliente.objects.create(
            tipo_doc=TipoDocumento.DNI,
            nro_doc="32132132",
            nombres="Ana",
            apellidos="Destinatario",
            estado=EstadoGeneral.ACTIVO,
        )
        self.ruta = Ruta.objects.create(
            codigo="LIM-ARE",
            origen="Lima",
            destino="Arequipa",
            precio_base=Decimal("25.00"),
            dias_entrega=2,
            estado=EstadoGeneral.ACTIVO,
            distancia_km=1000,
            activa=True,
        )

    def _auth(self):
        token_url = reverse("token_obtain")
        response = self.client.post(token_url, {"username": "apiuser", "password": "ApiPass123!"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_token_obtain(self):
        response = self.client.post(reverse("token_obtain"), {"username": "apiuser", "password": "ApiPass123!"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_create_encomienda(self):
        self._auth()
        url = reverse("encomienda-list")
        payload = {
            "codigo": "ENC-2026-9901",
            "descripcion": "Paquete API",
            "peso_kg": "2.50",
            "volumen_cm3": "10000",
            "costo_envio": "25.00",
            "remitente": self.remitente.id,
            "destinatario": self.destinatario.id,
            "ruta": self.ruta.id,
            "estado": "PE",
            "fecha_entrega_est": "2026-05-10",
            "observaciones": "prueba api",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Encomienda.objects.count(), 1)
