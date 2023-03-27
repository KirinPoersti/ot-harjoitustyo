import unittest

from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_kortin_saldo_alussa_oikein(self):
        self.kortti = Maksukortti(1000)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10.00 euroa")
    
    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.kortti = Maksukortti(1000)
        self.kortti.lataa_rahaa(2000)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 30.00 euroa")
    
    def test_rahan_ottaminen_toimii1(self):
        #Saldo vähenee oikein, jos rahaa on tarpeeksi
        self.kortti = Maksukortti(1000)
        self.kortti.ota_rahaa(500)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 5.00 euroa")

    def test_rahan_ottaminen_toimii2(self):
        #Saldo ei muutu, jos rahaa ei ole tarpeeksi
        self.kortti = Maksukortti(300)
        self.kortti.ota_rahaa(400)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 3.00 euroa")

    def test_rahan_ottaminen_toimii3_riittävä(self):
        #Metodi palauttaa True, jos rahat riittivät ja muuten False
        self.kortti = Maksukortti(300)
        vastaus = Maksukortti.ota_rahaa(self.kortti,200)

        self.assertEqual(str(vastaus), "True")
    
    def test_rahan_ottaminen_toimii3_ei_riittävä(self):
        #Metodi palauttaa False, jos rahat eivät riittää
        self.kortti = Maksukortti(300)
        vastaus = Maksukortti.ota_rahaa(self.kortti,400)

        self.assertEqual(str(vastaus), "False")
    

    
    