from datetime import timedelta
from decimal import Decimal
from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clientes.models import Cliente
from config.choices import EstadoEnvio, EstadoGeneral, TipoDocumento
from envios.models import Empleado, Encomienda, HistorialEstado
from rutas.models import Ruta


class EnviosSmokeTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="secret123")

    def test_home_redirects_if_not_authenticated(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_home_returns_200_when_authenticated(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class EncomiendaModelTests(TestCase):
    def setUp(self):
        self.remitente = Cliente.objects.create(
            nombres="Carlos",
            apellidos="Perez",
            tipo_doc=TipoDocumento.DNI,
            nro_doc="12345678",
            estado=EstadoGeneral.ACTIVO,
        )
        self.destinatario = Cliente.objects.create(
            nombres="Ana",
            apellidos="Lopez",
            tipo_doc=TipoDocumento.DNI,
            nro_doc="87654321",
            estado=EstadoGeneral.ACTIVO,
        )
        self.ruta = Ruta.objects.create(
            codigo="LIM-TRU",
            origen="Lima",
            destino="Trujillo",
            precio_base=25,
            dias_entrega=2,
            estado=EstadoGeneral.ACTIVO,
            distancia_km=560,
            activa=True,
        )
        self.empleado = Empleado.objects.create(
            codigo="EMP001",
            nombres="Luis",
            apellidos="Gomez",
            cargo="Operador de envios",
            email="luis@encomiendas.pe",
            estado=EstadoGeneral.ACTIVO,
            fecha_ingreso=date.today(),
        )

    def _crear_encomienda(self, **overrides):
        data = {
            "codigo": "ENC-2026-001",
            "remitente": self.remitente,
            "destinatario": self.destinatario,
            "ruta": self.ruta,
            "empleado_registro": self.empleado,
            "descripcion": "Caja de libros",
            "peso_kg": Decimal("4.5"),
            "costo_envio": Decimal("20.0"),
            "fecha_entrega_est": timezone.localdate() + timedelta(days=2),
        }
        data.update(overrides)
        return Encomienda.objects.create(**data)

    def test_validation_error_if_remitente_equal_destinatario(self):
        with self.assertRaises(ValidationError):
            self._crear_encomienda(destinatario=self.remitente)

    def test_cambiar_estado_generates_historial(self):
        encomienda = self._crear_encomienda()
        encomienda.cambiar_estado(
            EstadoEnvio.EN_TRANSITO, empleado=self.empleado, observacion="Salida de almacen"
        )
        self.assertEqual(encomienda.estado, EstadoEnvio.EN_TRANSITO)
        self.assertEqual(HistorialEstado.objects.count(), 1)

    def test_crear_con_costo_calculado(self):
        encomienda = Encomienda.crear_con_costo_calculado(
            remitente=self.remitente,
            destinatario=self.destinatario,
            ruta=self.ruta,
            empleado=self.empleado,
            descripcion="Paquete",
            peso_kg=Decimal("2.00"),
        )
        self.assertTrue(encomienda.costo_envio > 0)

    def test_queryset_helpers(self):
        enc1 = self._crear_encomienda(codigo="ENC-2026-003", estado=EstadoEnvio.PENDIENTE)
        enc2 = self._crear_encomienda(codigo="ENC-2026-004", estado=EstadoEnvio.EN_TRANSITO)
        self._crear_encomienda(codigo="ENC-2026-005", estado=EstadoEnvio.ENTREGADO)

        self.assertEqual(Encomienda.objects.pendientes().count(), 1)
        self.assertEqual(Encomienda.objects.activas().count(), 2)
        self.assertEqual(Encomienda.objects.en_transito_por_ruta(self.ruta).count(), 1)
        self.assertEqual(Encomienda.objects.activas().por_ruta(self.ruta).count(), 2)
        self.assertIn(enc1, Encomienda.objects.con_relaciones())
        self.assertIn(enc2, Encomienda.objects.con_relaciones())
