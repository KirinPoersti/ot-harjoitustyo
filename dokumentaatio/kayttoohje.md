# Käyttöohje

Lataa projektin viimeisimmän [releasen]( https://github.com/KirinPoersti/ot-harjoitustyo/releases) lähdekoodi valitsemalla _Assets_-osion alta _Source code_.

## Pelin käynnistäminen

Ennen ohjelman käynnistämistä, asenna riippuvuudet komennolla:

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
## Pelaaminen

Peli käynnistyy main menuun:

![](https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/kayttoohje-pelin%20aloitus.PNG)

Voit vapaasti valita haluamasi pelitilan, mikäli et jaksa pelata peliä enää, klikkaa vain "Exit".
## Long Jump
Sanotaan, että jos halusit pelata long jumpia, klikkaamalla ”Long Jump” avautuu uusi ikkuna, ja nyt olet long jump -valikossa. Klikkaamalla "Play" saat pelin alustettua. 

![](https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/kayttoohje-longjump.PNG)

#### Long Jump – Pelisäännöt
* Ennen varsinaista hyppyä pelaajalla on 5 sekuntia aikaa painaa ← ja → mahdollisimman paljon. Onnistuneen ← ja → painatus muodostaa yhden setin, jonka perusteella peli laskee suorituksesi hypyn jälkeen.
* 5 sekunnin jälkeen kun pelaaja on juostu pylvään asti, paina "Space" niin saat hahmosi hyppäämään, saat sen jälkeen tuloksesi näkyviin.
* Jokaisella pelikerralla saat 3 suorituskertaa, jonka jälkeen näet kaikki suorituksesi ikkunan oikealla yläkulmalla.
* Kolmen suorituskerran jälkeen sinun on kirjoitettava nimesi tallentaaksesi parhaan tuloksesi kaikista kolmesta yrityksestä. ja seuraavan kerran kun astut peliin, voit nähdä sen tulostaulukossa kilkkamalla ”Leaderboard” tai nimen syötön jälkeen pelikulkun lopussa (jos onnistut pysymään koko ajan kärjessä). Tulostaulu on oletusarvoisesti tyhjä.

## Pong
Sanotaan, että jos halusit pelata pong:a, klikkaamalla ”Pong” avautuu uusi ikkuna, ja nyt olet Pong -valikossa. Klikkaamalla "Practice" tai ”PvP” saat pelin alustettua. 

![](https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/kayttoohje-pong.PNG)

#### Pong– Pelisäännöt
Pracetice-mode:
* Voit harjoitella pallon kiinni ottoa liikkumalla "w" ja "s"
*  Harjoittelu-tilassa toimii myös stamina systeemi, josta kerrotaan seuraavassa osassa tarkemmin. 

PvP: 
* Voit toisen ystäväsi kanssa pelata kahdestaan tässä tilassa.
*  Se joka saa ensimmäisenä 10 pistettä voittaa pelin.
*  Pelaaja 1 liikkuu "w" ja "s" näppäimellä ja "L Shift":llä pystyy syöksyä pallon kimppuun.
*   Pelaaja 2 liikkuu "↑" ja "↓" näppäimellä ja "R Shift":llä pystyy syöksyä pallon kimppuun.
*    Stamina systeemi toimii niin, että kun Shiftit ovat painettu, pelaaja kuluttaa sillä hetkellä kerättyä stamina-arvoa.
*    Stamina-arvot saa ajan myötä takaisin, ja stamina-arvon maksimi on 5.
