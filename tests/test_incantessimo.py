from unittest import skip

from django.test import TestCase
from main.models.incantessimi import Incantessimo, IncantessimoEmanation, IncantessimoHour, IncantessimoGround


class IncantessimoTestCase(TestCase):
    def setUp(self):
        Incantessimo.objects.create(name="Barque de Rêve", category=1, path=1, ground_charge=IncantessimoGround.LAKE, hour_charge=IncantessimoHour.SHIP,
                                    emanation_charge=IncantessimoEmanation.FLUENT)

    def test_creation(self):
        i = Incantessimo.objects.get(name="Barque de Rêve")
        self.assertEqual(i.rid, "BAR_DE_REV_014")

    @skip("Spells to be fixed")
    def test_power(self):
        i = Incantessimo.objects.get(name="Barque de Rêve")
        self.assertEqual(i.power, 8)