from django.test import TestCase

from config.choices import EstadoGeneral
from rutas.models import Ruta


class RutaModelTests(TestCase):
    def test_manager_activas_y_por_origen(self):
        Ruta.objects.create(
            codigo="LIM-ARE",
            origen="Lima",
            destino="Arequipa",
            precio_base=35,
            dias_entrega=3,
            estado=EstadoGeneral.ACTIVO,
            distancia_km=1000,
            activa=True,
        )
        Ruta.objects.create(
            codigo="TRU-PIU",
            origen="Trujillo",
            destino="Piura",
            precio_base=20,
            dias_entrega=2,
            estado=EstadoGeneral.DE_BAJA,
            distancia_km=500,
            activa=False,
        )

        self.assertEqual(Ruta.objects.activas().count(), 1)
        self.assertEqual(Ruta.objects.por_origen("lim").count(), 1)
