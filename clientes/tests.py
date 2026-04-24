from django.test import TestCase

from clientes.models import Cliente
from config.choices import TipoDocumento
from envios.models import Empleado, Encomienda
from rutas.models import Ruta


class ClienteModelTests(TestCase):
    def setUp(self):
        self.remitente = Cliente.objects.create(
            nombres="Carlos",
            apellidos="Perez",
            tipo_doc=TipoDocumento.DNI,
            nro_doc="12345678",
            activo=True,
        )
        self.destinatario = Cliente.objects.create(
            nombres="Ana",
            apellidos="Lopez",
            tipo_doc=TipoDocumento.DNI,
            nro_doc="87654321",
            activo=False,
        )
        self.ruta = Ruta.objects.create(
            codigo="LIM-TRU",
            origen="Lima",
            destino="Trujillo",
            distancia_km=560,
            activa=True,
        )
        self.empleado = Empleado.objects.create(
            nombres="Juan",
            apellidos="Ruiz",
            nro_doc="44556677",
            activo=True,
        )

    def test_propiedades_cliente(self):
        self.assertEqual(self.remitente.nombre_completo, "Carlos Perez")
        self.assertTrue(self.remitente.esta_activo)

    def test_total_encomiendas_enviadas(self):
        Encomienda.objects.create(
            codigo="ENC-2026-001",
            remitente=self.remitente,
            destinatario=self.destinatario,
            ruta=self.ruta,
            empleado_registro=self.empleado,
            descripcion="Caja mediana",
            peso_kg=5,
            costo_envio=25,
        )
        self.assertEqual(self.remitente.total_encomiendas_enviadas, 1)

    def test_manager_activos_y_buscar(self):
        self.assertEqual(Cliente.objects.activos().count(), 1)
        self.assertEqual(Cliente.objects.buscar("car").count(), 1)
        self.assertEqual(Cliente.objects.buscar("8765").count(), 1)
