# Sports-Rally

Kyseessä olisi urheilurallia kuvaava peli, jossa on kaksi mini-peliä:
* Pong
* Pituushyppy

# Huomio Python-versiosta

Pelin toiminta on testattu Python-versiolla 3.10 ja pygame 2.3.0. Etenkin vanhempien Python-versioiden kanssa saattaa ilmentyä ongelmia.

# Dokumentaatio
- [Käyttöohje](dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentti](dokumentaatio/testaus.md)
- [Changelog](dokumentaatio/changelog.md)
- [Tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Loppupalautus](https://github.com/KirinPoersti/ot-harjoitustyo/releases/tag/Loppupalautus)

## Pelin käynnistäminen

Ennen ohjelman käynnistämistä, asenna riippuvuudet [`Sports Rally`](https://github.com/KirinPoersti/ot-harjoitustyo/tree/main/Sports-Rally) alla komennolla :

```bash
poetry install
```
Nyt ohjelman voi käynnistää komennolla:

```
poetry run invoke start
```
tai
```
poetry shell 
```
```
invoke start
```
