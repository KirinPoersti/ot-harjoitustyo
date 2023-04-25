# Sports-Rally

Kyseessä olisi urheilurallia kuvaava peli, jossa on kolme mini-peliä:
* Pong
* Pituushyppy
* "Kaksi-miestä-kolme-jalkaa" (Laji, jossa kaksi pelajaa yrittävät juosta yhksi heidän jaloista kiinnitettynä mahdollisimman nopeasti)

# Huomio Python-versiosta

Sovelluksen toiminta on testattu Python-versiolla 3.10 ja pygame 2.3.0. Etenkin vanhempien Python-versioiden kanssa saattaa ilmentyä ongelmia.

# Dokumentaatio

- [changelog](dokumentaatio/changelog.md)
- [tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)


# Pelin suorittaminen 
Peliä pystyy suorittamaan komennolla Sports-Rally kansion alla:
```bash
poetry run invoke start
```

# Pelisäännöt
- Long jump:
    - Ennen varsinaista hyppyä pelaajalla on 5 sekuntia aikaa painaa ← ja → mahdollisimman paljon. Onnistuneen ← ja → Painaus muodostaa yhden setin, jonka perusteella peli laskee suorituksesi hypyn jälkeen.
    - 5 sekunnin jälkeen kun pelaaja on juostu pylvään asti, paina "Space" niin saat hahmosi hyppämään, saat sen jälkeen tuloksesi näkyviin.
    - Jokaisella pelikerralla saat 3 suorituskertaa, jonka jälkeen näet kaikki suorituksesi ikkunan oikealla yläkulmalla.
- Pong:
    - Pracetice-mode:
        - Voit harijoitella pallon kiinni ottoa liikkumalla "w" ja "s"
    - PvP
        - Voit toisen ystäväsi kanssa pelata kahdestaan tässä modessa.
        - Se joka saa ensimmäisenä 10 pistettä voittaa pelin.
        - Pelaaja 1 liikkuu "w" ja "s" näppäimellä ja "L Shift":llä pystyy syöksyä pallon kimppuun.
        - Pelaaja 2 liikkuu "↑" ja "↓" näppäimellä ja "R Shift":llä pystyy syöksyä pallon kimppuun.
        - Stamina systeemi toimii niin, että kun Shiftit ovat painettu, pelaaja kuluttaa sillä hetkellä kerrättyä stamina-arvoa.
        - Stamina-arvot saa ajan myöttä takaisin, ja stamina-arvon maksimi on 5.
