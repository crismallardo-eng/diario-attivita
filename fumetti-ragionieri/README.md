# Fumetti della Biblioteca Ragionieri (Sesto Fiorentino)

Estrazione completa dei fumetti posseduti dalla Biblioteca Comunale "Ernesto
Ragionieri" di Sesto Fiorentino, ricavata dal catalogo online OPAC SDIAF
(Sistema Documentario Integrato dell'Area Fiorentina).

Fonte: <https://opac.comune.firenze.it/it/now/biblioteca-ragionieri-sesto/ricerca>
Data estrazione: 2026-08-11

## Contenuto

| File | Descrizione |
|---|---|
| `fumetti_ragionieri.csv` | 3.630 titoli, un record per riga (apribile in Excel/LibreOffice) |
| `fumetti_ragionieri.json` | gli stessi dati in JSON |
| `estrai_fumetti.py` | script che rigenera i due file interrogando il catalogo |

## Numeri

- **3.630 titoli** distinti, per **3.766 copie fisiche** in biblioteca
- 3.627 monografie + 3 videoregistrazioni
- Per decennio di pubblicazione: 2020+ → 1.166 · 2010 → 1.068 · 2000 → 885 ·
  1990 → 424 · 1980 → 55 · precedenti → 27
- Editori principali: Planet Manga (763), Star Comics (754), Panini Comics (172),
  Gruppo Editoriale L'Espresso (108), Bao Publishing (99), BD (56),
  SaldaPress (53), Mondadori (43), Coconino Press (42), Rizzoli Lizard (35)
- Prestito: 3.320 ammessi al prestito, 285 solo prestito locale, 3 esclusi
- Collocazione prevalente: `741.595` (manga, 2.296 copie) e sezione `F` (1.201)

## Come è stata fatta la ricerca

Il catalogo gira su OPAC Nexus NOW: la ricerca avanzata accetta i parametri via
GET, quindi si può interrogare campo per campo e paginare con `start`/`step`.

Nessun filtro singolo copre tutto il posseduto, perché il codice di genere SBN
"Vignette o Fumetti" è stato applicato solo alla catalogazione più recente,
mentre i record più vecchi (Bonelli, Disney, manga anni '90-2000, Pratt, Staino…)
sono raggiungibili solo per soggetto o per classificazione Dewey. L'estrazione
unisce quindi sei ricerche:

| Criterio | Record |
|---|---|
| Genere SBN = "Vignette o Fumetti" | 1.783 |
| Soggetto = "Fumetti" | 1.719 |
| Classificazione Dewey = 741.5 | 339 |
| Soggetto = "Manga" | 28 |
| Soggetto = "Fumetto" | 19 |
| Soggetto = "Graphic novel" | 7 |
| **Unione (record unici)** | **3.630** |

La colonna `criteri` di ogni record indica da quale/i ricerca/e proviene: 1.645
titoli si trovano solo per genere, 1.561 solo per soggetto, 153 solo per Dewey.

Tutti i 3.630 record hanno almeno una copia posseduta dalla Biblioteca
Ragionieri: la ricerca parte dal portale della biblioteca ed è già filtrata sul
suo posseduto, anche se la scheda delle copie mostra pure gli esemplari delle
altre biblioteche SDIAF (che infatti vengono scartati in fase di parsing).

## Colonne

| Colonna | Significato |
|---|---|
| `codice` | codice record SBN (chiave univoca) |
| `titolo` | titolo come da catalogo, con le indicazioni di responsabilità |
| `autore` | autore, quando la descrizione lo riporta separatamente |
| `editore` / `editore_norm` | editore grezzo e versione normalizzata (maiuscole/varianti) |
| `anno` | anno di pubblicazione |
| `genere` / `tipologia` | genere SBN e tipo di materiale |
| `copie_ragionieri` | numero di copie possedute dalla Ragionieri |
| `collocazioni` / `inventari` | collocazioni e numeri di inventario (separati da `;`) |
| `prestito` | condizioni di prestito |
| `criteri` | ricerche che hanno intercettato il record |
| `descrizione` | descrizione bibliografica completa |
| `url` | link alla scheda nel catalogo |

## Rigenerare i dati

```bash
python3 estrai_fumetti.py
```

Lo script scarica ~23 pagine con una pausa di 1,5 s fra una richiesta e l'altra e
mette in cache l'HTML in `.cache/` (non versionata), così una seconda esecuzione
non ricarica il server. Per un aggiornamento reale, cancellare `.cache/` prima.

## Avvertenze

- Il conteggio riflette i **record di catalogo**, non i singoli volumi di una
  serie quando questi sono descritti in un unico record.
- Il set per soggetto include qualche saggio *sui* fumetti (storia, critica)
  oltre ai fumetti veri e propri; filtrando su `criteri` si possono isolare.
- `autore` ed `editore` sono ricavati per pattern dalla descrizione
  bibliografica: in circa un record su cinque l'editore resta vuoto perché la
  descrizione non segue lo schema `Luogo : Editore, anno`.
