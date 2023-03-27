import unittest

from kassapaate import Kassapaate
from maksukortti import Maksukortti as kortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def test_saldo_alussa(self):
        kassapaate = Kassapaate()
        self.assertEqual(kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kassapaate.edulliset, 0)
        self.assertEqual(kassapaate.maukkaat, 0)

    def test_kassa_rahaa(self):
        self.assertEqual(str(self.kassassa_rahaa), '100000')

    def test_edulliset(self):
        self.assertEqual(str(self.edulliset), '0')
    
    def test_maukkaat(self):
        self.assertEqual(str(self.maukkaat), '0')

    def test_tilanteet_alussa_kassa(self):
        #alku-tilanteen tarkastus
        self.assertEqual(str(self.kassassa_rahaa), '100000')
    
    def test_tilanteet_alussa_edulliset(self):
        #alku-tilanteen tarkastus
        self.assertEqual(str(self.edulliset), '0')
        
    def test_tilanteet_alussa_maukkaat(self):
        #alku-tilanteen tarkastus
        self.assertEqual(str(self.maukkaat), '0')
   
    def test_käteisosto_edulliset_yli_vaihtoraha(self):
        #maksaa enemmän kuin edullisen lounaan hintaa
        vastaus = Kassapaate.syo_edullisesti_kateisella(self, 250)
        
        self.assertEqual(str(vastaus), '10')
    
    def test_käteisosto_edulliset_yli_myynti(self):
        #maksaa enemmän kuin edullisen lounaan hintaa
        Kassapaate.syo_edullisesti_kateisella(self, 250)
        edulliset = self.edulliset
        
        self.assertEqual(str(edulliset), '1')
    
    def test_käteisosto_edulliset_yli_kassa(self):
        #maksaa enemmän kuin edullisen lounaan hintaa
        Kassapaate.syo_edullisesti_kateisella(self, 250)
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(kassa), '100240')
    
    def test_käteisosto_edulliset_riitävä_vaihtoraha(self):
        #maksaa saman verran kuin edullisen lounaan hintaa
        vastaus = Kassapaate.syo_edullisesti_kateisella(self, 240)
        
        self.assertEqual(str(vastaus), '0')

    def test_käteisosto_edulliset_riitävä_myynti(self):
        #maksaa saman verran kuin edullisen lounaan hintaa
        Kassapaate.syo_edullisesti_kateisella(self, 240)
        edulliset = self.edulliset
        
        self.assertEqual(str(edulliset), '1')
    
    def test_käteisosto_edulliset_riitävä_kassa(self):
        #maksaa saman verran kuin edullisen lounaan hintaa
        Kassapaate.syo_edullisesti_kateisella(self, 240)
        kassa = self.kassassa_rahaa

        self.assertEqual(str(kassa), '100240')

    def test_käteisosto_edulliset_ei_riitävä_vaihtoraha(self):
        #maksaa vähemmän kuin edullisen lounaan hintaa
        vastaus = Kassapaate.syo_edullisesti_kateisella(self, 230)

        self.assertEqual(str(vastaus), '230')

    def test_käteisosto_edulliset_ei_riitävä_myynti(self):
        #maksaa vähemmän kuin edullisen lounaan hintaa
        Kassapaate.syo_edullisesti_kateisella(self, 230)
        edulliset = self.edulliset

        self.assertEqual(str(edulliset), '0')

    def test_käteisosto_edulliset_ei_riitävä_kassa(self):
        #maksaa vähemmän kuin edullisen lounaan hintaa
        Kassapaate.syo_edullisesti_kateisella(self, 230)
        kassa = self.kassassa_rahaa
    
        self.assertEqual(str(kassa), '100000')

    def test_korttiosto_edulliset_riitäv_veloitus(self):
        #kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
        vastaus = Kassapaate.syo_edullisesti_kortilla(self, kortti(1000))
 
        self.assertEqual(str(vastaus), 'True')
    
    def test_korttiosto_edulliset_riitäv_myynti(self):
        #kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
        vastaus = Kassapaate.syo_edullisesti_kortilla(self, kortti(1000))
        edulliset = self.edulliset

        self.assertEqual(str(vastaus), 'True')
        self.assertEqual(str(edulliset), '1')
    
    def test_korttiosto_edulliset_riitäv_kassa(self):
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        #kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu
        Kassapaate.syo_edullisesti_kortilla(self, kortti(1000))

        self.assertEqual(str(self.kassassa_rahaa), '100000')
        self.assertEqual(str(kortti(230)), 'Kortilla on rahaa 2.30 euroa')

    def test_korttiosto_edulliset_ei_riitävä(self):
        self.assertEqual(str(self.edulliset), '0')
        self.assertEqual(str(Kassapaate.syo_edullisesti_kortilla(self, kortti(230))), 'False')
        self.assertEqual(str(self.kassassa_rahaa), '100000')

    def test_korttiosto_maukkaat_riitävä_veloitus(self):
        #kortilla on tarpeeksi rahaa, veloitetaan summa kortilta
        Kassapaate.syo_maukkaasti_kortilla(self, kortti(1000))
        saldo = kortti(1000-400)

        self.assertEqual(str(saldo), 'Kortilla on rahaa 6.00 euroa')

    def test_korttiosto_maukkaat_riitävä_myynti(self):
        #kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
        Kassapaate.syo_maukkaasti_kortilla(self, kortti(1000))
        maukkaat = self.maukkaat

        self.assertEqual(str(maukkaat), '1')
    
    def test_korttiosto_maukkaat_riitävä_palautus(self):
        #palautetaan True
        vastaus = Kassapaate.syo_maukkaasti_kortilla(self, kortti(1000))
        
        self.assertEqual(str(vastaus), 'True')
    
    def test_korttiosto_maukkaat_riitävä_kassa(self):
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        Kassapaate.syo_maukkaasti_kortilla(self, kortti(1000))
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(kassa), '100000')
    
    def test_korttiosto_edulliset_ei_riitävä_veloitus(self):
        #kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu
        Kassapaate.syo_maukkaasti_kortilla(self, kortti(300))
        saldo = kortti(300)

        self.assertEqual(str(saldo), 'Kortilla on rahaa 3.00 euroa')
    
    def test_korttiosto_edulliset_ei_riitävä_myynti(self):
        #myytyjen lounaiden määrä muuttumaton
        Kassapaate.syo_maukkaasti_kortilla(self, kortti(300))
        maukkaat = self.maukkaat

        self.assertEqual(str(maukkaat), '0')

    def test_korttiosto_edulliset_ei_riitävä_palautus(self):
        #palautetaan False
        vastaus = Kassapaate.syo_maukkaasti_kortilla(self, kortti(300))

        self.assertEqual(str(vastaus), 'False')
    
    def test_korttiosto_edulliset_ei_riitävä_kassa(self):
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        Kassapaate.syo_maukkaasti_kortilla(self, kortti(300))
        kassa = self.kassassa_rahaa

        self.assertEqual(str(kassa), '100000')
    
    def test_kortille_lataaminen_saldo(self):
        #kortille rahaa ladattaessa kortin saldo muuttuu
        Kassapaate.lataa_rahaa_kortille(self, kortti(0), 400)
        saldo = kortti(400)
        
        self.assertEqual(str(saldo), 'Kortilla on rahaa 4.00 euroa')
    
    def test_kortille_lataaminen_kassa(self):
        #kassassa oleva rahamäärä kasvaa ladatulla summalla
        Kassapaate.lataa_rahaa_kortille(self, kortti(0), 400)
        kassa = self.kassassa_rahaa

        self.assertEqual(str(kassa), '100400')

    def test_käteisosto_maukkaat_ei_riitävä_vaihtoraha(self):
        #maksaa vähemmän kuin maukkaan lounaan hintaa
        vastaus = Kassapaate.syo_maukkaasti_kateisella(self, 350)

        self.assertEqual(str(vastaus), '350')

    def test_käteisosto_maukkaat_ei_riitävä_myynti(self):
        #maksaa vähemmän kuin maukkaan lounaan hintaa
        Kassapaate.syo_maukkaasti_kateisella(self, 350)
        maukkaat = self.maukkaat

        self.assertEqual(str(maukkaat), '0')

    def test_käteisosto_maukkaat_ei_riitävä_kassa(self):
        #maksaa vähemmän kuin maukkaan lounaan hintaa
        Kassapaate.syo_maukkaasti_kateisella(self, 350)
        kassa = self.kassassa_rahaa

        self.assertEqual(str(kassa), '100000')

    def test_käteisosto_maukkaat_riitävä_vaihtoraha(self):
        #maksaa enemmän kuin maukkaan lounaan hintaa
        vastaus = Kassapaate.syo_maukkaasti_kateisella(self, 450)
        
        self.assertEqual(str(vastaus), '50')
    
    def test_käteisosto_maukkaat_riitävä_myynti(self):
        #maksaa enemmän kuin maukkaan lounaan hintaa
        Kassapaate.syo_maukkaasti_kateisella(self, 450)
        maukkaat = self.maukkaat
        
        self.assertEqual(str(maukkaat), '1')
    
    def test_käteisosto_maukkaat_riitävä_kassa(self):
        #maksaa enemmän kuin maukkaan lounaan hintaa
        Kassapaate.syo_maukkaasti_kateisella(self, 450)
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(kassa), '100400')


    def test_kortille_lataaminen_negatiivinen_summa(self):
        kortti_s = kortti(100)
        Kassapaate.lataa_rahaa_kortille(self, kortti_s, -10)
        saldo = kortti(100)

        self.assertEqual(str(saldo), 'Kortilla on rahaa 1.00 euroa')
        self.assertEqual(str(self.kassassa_rahaa), '100000')


