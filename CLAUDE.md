# Diario attività

## File di dati
`diario_attivita.json` nella stessa cartella di questo file.

## Comportamento principale
Scrivi e fai push **direttamente sul branch `master`** (niente branch di lavoro né pull request): il report su GitHub legge da `master`.

Quando l'utente menziona un'attività svolta, aggiungila **subito** al campo `log` del JSON senza chiedere conferma prima. Dopo averla scritta, mostra la voce inserita e basta.

Formato di ogni voce:
```json
{"data": "YYYY-MM-DD", "categoria": "...", "sottocategoria": "...", "note": "..."}
```
- Usa sempre la data di oggi salvo indicazione diversa ("ieri", "il 15", ecc.)
- Le note sono opzionali: usale per titoli, episodi, voti, dettagli utili
- Riconosci categoria e sottocategoria anche da input informali — "ho visto un film" → Visioni/Film, "sono andato a correre" → Palestra/Corsa, "ho cucinato" → Casa/Cucina
- Se la sottocategoria è davvero ambigua, chiedi — ma solo allora

## Macro-gruppi
- **Tempo libero:** Letture, Visioni, Outdoor, Approfondimenti, Clarinetto, Musica, Videogiochi
- **Tempo misero:** Palestra/Attività fisica, Concorsi, Casa, Salute

## Categorie e sottocategorie
| Categoria | Sottocategorie |
|---|---|
| Letture | Libro, Graphic Novel, Fumetto, Manga, Altro |
| Visioni | Film, Serie TV, Cartone, Anime, Documentario, Comedy show, Altro |
| Outdoor | Passeggiata, Biblioteca, Museo/Mostra, Bar/Caffè/Pub, Gelataio/Pasticceria, Ristoranti, Parchi, Mercati, Cinema, Concerti, Altro |
| Approfondimenti | Storia uomo, Storia arte, Storia musica, Storia letteratura, Storia terra, Storia spazio, Decennio musicale, Gruppo/Artista, Teoria musicale, Attualità/Politica, Altro |
| Clarinetto | Lezione, Esercizi, Teoria |
| Palestra/Attività fisica | Upper, Lower, Total, Corsa |
| Concorsi | Scrittura appunti, Risistemazione appunti, Ripasso appunti, Studio/sottolineatura manuale, Quiz |
| Musica | Riascolti, Nuovi ascolti, Per approfondimenti |
| Casa | Pulizie, Spesa, Commissioni, Burocrazia, Cucina, Altro |
| Videogiochi | Indie, RPG, Avventura, Platform, Strategia, Altro |
| Salute | Dieta, Esami medici, Visita, Altro |

## Priorità (definite il 2026-11-19)
**Fondamentali**
- **Concorsi:** almeno 1h di studio al giorno (aumentare se esce un bando)
- **Attività fisica:** palestra 3 volte/settimana + 1 corsetta
- **Dieta:** delineare la situazione il 27/11 (promemoria su Calendar)
- **Esami medici:** fare il punto il 01/12 per gli esami di dicembre/gennaio (promemoria su Calendar)

**Da coltivare**
- **Approfondimento arte fruita:** tema attuale = **jazz**, più contesto su film/letture fruiti
- **Attualità/temi sociopolitici:** un tema alla volta per 1–2 mesi (da scegliere)
- **Uscite/socialità:** tenere d'occhio gli eventi a Firenze
- **Clarinetto e teoria musicale:** da capire come ritagliare il tempo ed esercitarsi bene
- **Fruizione varia:** più film, cartoni, fumetti, graphic novel, documentari, comedy show (i formati facili come manga/serie vanno già da soli)

**Rinviato:** approfondimento materie (storia uomo/arte/letteratura ecc.)

Nei riepiloghi dare precedenza alle priorità fondamentali e segnalare da quanto non si fanno le attività "da coltivare".

## Obiettivi (per riferimento, non tracciarli qui — la fonte è il JSON)
**Settimanali:** Concorsi ≥7/sett (1h al giorno) · Palestra ≥3/sett · Corsa ≥1/sett
**Mensili:** Ristorante, Mercato ortofrutticolo (sabato), Concerto, Cinema, Biblioteca, Ricetta ≥1/mese · Film ≥2/mese · Cartone ≥1/mese · Graphic Novel ≥1/mese

## Riepilogo rapido
Se l'utente chiede "cosa ho fatto oggi/questa settimana/questo mese", leggere il JSON e rispondere in testo semplice — non generare report HTML (quello si fa sul PC).
