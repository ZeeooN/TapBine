# TapBine
1. Praktiskais darbs mācibu priekšmetā 'Mākslīgā intelekta pamati'

## Spēles palaišana
Lai palaistu un spēlētu spēli vajag pieinstalēt divas Python pakotnes.

 1. [Pygame](https://www.pygame.org/news)
```
python -m pip install -U pygame==2.3.0 --user
```
 2. [Anytree](https://github.com/c0fec0de/anytree)
```
python -m pip install anytree --user
``` 
 Pēc pakotņu pieinstalēšanas var palaist `main.py` failu un spēle atvērsies.
 
 ## Par spēli 'TapBine'
Šī ir divspēlētāju spēle, kuras mērķis ir apvienot divas uz lauka esošas figūras kamēr paliek tikai divas no tām. Šajā gadījuma spēlē spēlētājs pret datoru. Pieejamās figūras ir aplis un kvadrāts. Spēle sākas ar 5 pēc gadijuma izvēlētam figurām. Spēlētājiem jāizvēlas viena no dotajām figūrām, tiklīdz kāda ir izvēlēta tā tiek apvienota ar figūru, kas tai ir pa labi un atkarībā no figūru kombinācijas tās tiek aizstātas ar attiecīgo kombinācijas rezultāta figūru. Kad uz lauka ir palikušas tikai divas figūras tiek paziņots uzvarētājs atkarībā no tā kāda figūra ir pirmajā vietā, piemēram, ja spēles beigās pirmajā vietā ir aplis, tad uzvar tas spēlētājs kurš uzsāka spēli, bet ja primajā vietā ir kvadrāts, tad uzvar otrs spēlētājs.

## Figūru kombinācijas
 Aplis + Kvadrāts = Aplis
 ``⬤ + ∎ -> ⬤``
 Aplis + Aplis = Kvadrāts
 ``⬤ + ⬤ -> ∎``
 Kvadrāts + Aplis = Kvadrāts
 ``∎ + ⬤ -> ∎``
 Kvadrāts + Kvadrāts = Aplis
 ``∎ + ∎ -> ⬤``