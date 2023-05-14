# Sports-Rally

Kyseessä olisi urheilurallia kuvaava peli, jossa on kolme mini-peliä:
* Pong
* Pituushyppy
* "Kaksi-miestä-kolme-jalkaa" (Laji, jossa kaksi pelajaa yrittävät juosta yhksi heidän jaloista kiinnitettynä mahdollisimman nopeasti)

# Huomio Python-versiosta

Sovelluksen toiminta on testattu Python-versiolla 3.10 ja pygame 2.3.0. Etenkin vanhempien Python-versioiden kanssa saattaa ilmentyä ongelmia.

# Dokumentaatio
- [Käyttöohje](dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentti](dokumentaatio/testaus.md)
- [Changelog](dokumentaatio/changelog.md)
- [Tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Loppupalautus](https://github.com/KirinPoersti/ot-harjoitustyo/releases/tag/Loppupalautus)

# Pelin suorittaminen 
Ennen pelin suorittamista pitää suorittaa Sports-Rally kansion alla:
```bash
poetry install
```
Peliä pystyy suorittamaan komennolla Sports-Rally kansion alla:
```bash
poetry run invoke start
```
