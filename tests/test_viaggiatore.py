from django.test import TestCase

from main.models.incantessimi import Incantessimo
from main.models.viaggiatori import Viaggiatore


class ViaggiatoreTestCase(TestCase):
    def setUp(self):
        Incantessimo.objects.create(name="Barque de Rêve", category=1,path=1)
        Viaggiatore.objects.create(name="John Doe", spells="BAR_DE_REV_014")


    def test_creation(self):
        c = Viaggiatore.objects.get(name="John Doe")
        self.assertEqual(c.sogni, "DEF")

    def test_rid(self):
        c = Viaggiatore.objects.get(name="John Doe")
        self.assertEqual(c.rid, "VIA_JOH_DOE_008")

    def test_type(self):
        c = Viaggiatore.objects.get(name="John Doe")
        self.assertEqual(c.type, "Viaggiatore")

    def test_spells(self):
        c = Viaggiatore.objects.get(name="John Doe")
        t = c.spells_analysis()
        self.assertEqual(t,6)