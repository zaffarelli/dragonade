from django.test import TestCase
from main.models.incantessimi import Incantessimo, DragonadeEmanation, DragonadeHour, DragonadeGround


class IncantessimoTestCase(TestCase):
    def setUp(self):
        Incantessimo.objects.create(name="Barque de Rêve", category=1, path=1, ground_charge=DragonadeGround.LAKE, hour_charge=DragonadeHour.SHIP,
                                    emanation_charge=DragonadeEmanation.FLUENT)

    def test_creation(self):
        i = Incantessimo.objects.get(name="Barque de Rêve")
        self.assertEqual(i.rid, "BAR_DE_REV_014")

    def test_power(self):
        i = Incantessimo.objects.get(name="Barque de Rêve")
        self.assertEqual(i.power, 9)