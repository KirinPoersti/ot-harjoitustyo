class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def syo_edullisesti_kateisella(self, maksu):
        if maksu < 240:
            return maksu
        self.kassassa_rahaa += 240
        self.edulliset += 1
        return maksu - 240

    def syo_maukkaasti_kateisella(self, maksu):
        if maksu < 400:
            return maksu
        self.kassassa_rahaa += 400
        self.maukkaat += 1
        return maksu - 400

    def syo_edullisesti_kortilla(self, kortti):
        if kortti.saldo < 240:
            return False
        kortti.ota_rahaa(240)
        self.edulliset += 1
        return True

    def syo_maukkaasti_kortilla(self, kortti):
        if kortti.saldo < 400:
            return False
        kortti.ota_rahaa(400)
        self.maukkaat += 1
        return True

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa < 0:
            return
        kortti.lataa_rahaa(summa)
        self.kassassa_rahaa += summa
