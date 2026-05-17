# Diario attività

## File di dati
`diario_attivita.json` nella stessa cartella di questo file.

## Comportamento principale
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
- **Tempo misero:** Palestra/Attività fisica, Concorsi, Casa

## Categorie e sottocategorie
| Categoria | Sottocategorie |
|---|---|
| Letture | Libro, Graphic Novel, Fumetto, Manga, Altro |
| Visioni | Film, Serie TV, Cartone, Anime, Documentario, Altro |
| Outdoor | Passeggiata, Biblioteca, Museo/Mostra, Bar/Caffè/Pub, Gelataio/Pasticceria, Ristoranti, Parchi, Mercati, Cinema, Concerti, Altro |
| Approfondimenti | Storia uomo, Storia arte, Storia musica, Storia letteratura, Storia terra, Storia spazio, Decennio musicale, Gruppo/Artista, Teoria musicale, Altro |
| Clarinetto | Lezione, Esercizi, Teoria |
| Palestra/Attività fisica | Upper, Lower, Total, Corsa |
| Concorsi | Scrittura appunti, Risistemazione appunti, Ripasso appunti, Studio/sottolineatura manuale, Quiz |
| Musica | Riascolti, Nuovi ascolti, Per approfondimenti |
| Casa | Pulizie, Spesa, Commissioni, Burocrazia, Cucina, Altro |
| Videogiochi | Indie, RPG, Avventura, Platform, Strategia, Altro |

## Obiettivi (per riferimento, non tracciarli qui)
**Settimanali:** Film ≥1/sett · Palestra ≥2/sett · Corsa ≥1/sett
**Mensili:** Ristorante, Mercato ortofrutticolo (sabato), Concerto, Cinema, Biblioteca, Ricetta ≥1/mese

## Riepilogo rapido
Se l'utente chiede "cosa ho fatto oggi/questa settimana/questo mese", leggere il JSON e rispondere in testo semplice — non generare report HTML (quello si fa sul PC).
