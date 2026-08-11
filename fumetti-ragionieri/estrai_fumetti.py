#!/usr/bin/env python3
"""Estrae dal catalogo OPAC della Biblioteca Comunale "Ernesto Ragionieri" di
Sesto Fiorentino tutti i fumetti posseduti, e li esporta in CSV + JSON.

Il catalogo gira su OPAC Nexus NOW (rete SDIAF). La pagina di ricerca avanzata
accetta i parametri via GET, quindi si possono interrogare i singoli campi e
paginare con `start` / `step`.

Nessun singolo filtro copre tutto il posseduto: il codice di genere SBN
"Vignette o Fumetti" è stato applicato solo alla catalogazione più recente,
mentre i record più vecchi si trovano solo per soggetto o per classificazione
Dewey. Lo script quindi unisce più criteri e per ogni record registra quali
filtri l'hanno intercettato (colonna `criteri`).

Uso:
    python3 estrai_fumetti.py [cartella_output]

Le pagine HTML scaricate vengono messe in cache in `.cache/`, così una seconda
esecuzione non ricarica il server.
"""

import csv
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://opac.comune.firenze.it/it/now/biblioteca-ragionieri-sesto/ricerca"
RECORD_URL = "https://opac.comune.firenze.it/it/now/biblioteca-ragionieri-sesto/record/"
BIBLIOTECA = "Biblioteca Comunale Ernesto Ragionieri - Sesto Fiorentino"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")
STEP = 200        # record per pagina
PAUSA = 1.5       # secondi fra una richiesta e l'altra

# Criteri di ricerca uniti fra loro. L'ordine determina l'ordine in `criteri`.
CRITERI = [
    ("genere:Vignette o Fumetti", {"genere_sbn": "Vignette o Fumetti"}),
    ("soggetto:Fumetti",          {"soggetto": "Fumetti"}),
    ("dewey:741.5",               {"classificazione_dewey": "741.5"}),
    ("soggetto:Manga",            {"soggetto": "Manga"}),
    ("soggetto:Fumetto",          {"soggetto": "Fumetto"}),
    ("soggetto:Graphic novel",    {"soggetto": "Graphic novel"}),
]

COLONNE = ["codice", "titolo", "autore", "editore", "editore_norm", "anno",
           "genere", "tipologia", "copie_ragionieri", "collocazioni",
           "inventari", "prestito", "criteri", "descrizione", "url"]

EDITORI_NORM = {
    "planet manga": "Planet Manga", "star comics": "Star Comics",
    "panini comics": "Panini Comics", "bao": "Bao Publishing",
    "bao publishing": "Bao Publishing", "coconino press": "Coconino Press",
    "rizzoli lizard": "Rizzoli Lizard", "j-pop": "J-Pop", "jpop": "J-Pop",
    "gruppo editoriale l'espresso": "Gruppo Editoriale L'Espresso",
    "sergio bonelli editore": "Sergio Bonelli Editore",
    "bonelli": "Sergio Bonelli Editore", "tunué": "Tunué",
    "saldapress": "SaldaPress",
}


# --------------------------------------------------------------------------- #
# download
# --------------------------------------------------------------------------- #

def scarica(params, cache_path):
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 5000:
        return open(cache_path, encoding="utf-8", errors="replace").read()
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = resp.read().decode("utf-8", "replace")
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    open(cache_path, "w", encoding="utf-8").write(body)
    time.sleep(PAUSA)
    return body


def interroga(tag, filtri, cache_dir):
    """Esegue una ricerca e restituisce tutti i record, paginando."""
    sotto = os.path.join(cache_dir, re.sub(r"\W+", "_", tag))
    base = dict(filtri, isPostBack="1", result_type="list",
                step=str(STEP), orderby="titolo")
    record, visti, totale, start = [], set(), None, 0
    while True:
        params = dict(base)
        if start:
            params["start"] = str(start)
        pagina = scarica(params, os.path.join(sotto, f"p{start:05d}.html"))
        if totale is None:
            m = re.search(r"Risultati:\s*\d+-\d+ su (\d+)", pagina)
            totale = int(m.group(1)) if m else 0
        for r in estrai_record(pagina):
            if r["codice"] not in visti:
                visti.add(r["codice"])
                record.append(r)
        start += STEP
        if start >= totale:
            break
    print(f"  {tag:30s} {totale:5d} dichiarati -> {len(record):5d} estratti")
    return record


# --------------------------------------------------------------------------- #
# parsing
# --------------------------------------------------------------------------- #

SEPARATORE = re.compile(r'<div class="shop-list product-item')


def testo(frammento):
    ripulito = re.sub(r"<[^>]+>", " ", frammento)
    return re.sub(r"\s+", " ", html.unescape(ripulito)).strip()


def estrai_copie(blocco):
    copie = []
    for m in re.finditer(
            r"<!-- Biblioteca -->(.*?)<!-- Collocazione -->(.*?)<!-- Serie -->"
            r"(.*?)<!-- Inventario -->(.*?)<!-- Prestito -->(.*?)<!-- Disponibilit",
            blocco, re.S):
        copie.append({
            "biblioteca": testo(m.group(1)),
            "collocazione": testo(m.group(2)),
            "inventario": testo(m.group(4)),
            "prestito": testo(m.group(5)),
        })
    return copie


def normalizza_editore(nome):
    nome = re.sub(r"\s+", " ", nome).strip().strip(".").strip()
    if not nome:
        return ""
    return EDITORI_NORM.get(nome.lower(), nome[0].upper() + nome[1:])


def estrai_record(pagina):
    parti = pagina.split("<!-- RISULTATI list-view -->", 1)
    if len(parti) < 2:
        return []
    lista = parti[1].split("<!-- RISULTATI flist-view -->", 1)[0]

    record = []
    for blocco in SEPARATORE.split(lista)[1:]:
        m = re.search(r'<h2>\s*<a href="record/([^"]+)"[^>]*>(.*?)</a>', blocco, re.S)
        if not m:
            continue
        r = {"codice": m.group(1), "titolo": testo(m.group(2))}

        m = re.search(r"Codice record:</span>\s*([A-Z0-9]+)", blocco)
        if m:
            r["codice"] = m.group(1)
        m = re.search(r'<p class="brand-name">(.*?)</p>', blocco, re.S)
        r["tipologia"] = testo(m.group(1)) if m else ""
        m = re.search(r"Genere:</span>(.*?)</p>", blocco, re.S)
        r["genere"] = testo(m.group(1)).strip("; ") if m else ""
        m = re.search(r"Descrizione:</span>(.*?)</p>", blocco, re.S)
        descrizione = testo(m.group(1)) if m else ""
        r["descrizione"] = descrizione

        # nella descrizione l'autore, quando presente, precede il titolo
        r["autore"] = ""
        taglio = descrizione.find(r["titolo"][:40])
        if taglio > 0:
            autore = descrizione[:taglio].strip().rstrip(".").strip()
            if 0 < len(autore) <= 90:
                r["autore"] = autore

        # "- Luogo : Editore, anno."
        m = re.search(r"-\s*[^:.]{2,40}?\s*:\s*([^,;]{2,60}?),\s*"
                      r"(?:1[5-9]\d{2}|20[0-2]\d|\[)", descrizione)
        r["editore"] = m.group(1).strip() if m else ""
        r["editore_norm"] = normalizza_editore(r["editore"])
        anni = re.findall(r"(1[5-9]\d{2}|20[0-2]\d)", descrizione)
        r["anno"] = anni[-1] if anni else ""

        copie = estrai_copie(blocco)
        nostre = [c for c in copie if c["biblioteca"] == BIBLIOTECA]
        r["copie_ragionieri"] = len(nostre)
        r["copie_sdiaf_totali"] = len(copie)
        r["collocazioni"] = sorted({c["collocazione"] for c in nostre if c["collocazione"]})
        r["inventari"] = sorted({c["inventario"] for c in nostre if c["inventario"]})
        r["prestito"] = "; ".join(sorted({c["prestito"] for c in nostre if c["prestito"]}))
        r["url"] = RECORD_URL + r["codice"]
        record.append(r)
    return record


# --------------------------------------------------------------------------- #

def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(out_dir, ".cache")

    print("Interrogazione del catalogo OPAC SDIAF (portale Biblioteca Ragionieri):")
    unione = {}
    for tag, filtri in CRITERI:
        for r in interroga(tag, filtri, cache_dir):
            corrente = unione.setdefault(r["codice"], dict(r, criteri=[]))
            if tag not in corrente["criteri"]:
                corrente["criteri"].append(tag)

    record = sorted(unione.values(), key=lambda r: (r["titolo"].lower(), r["codice"]))
    for r in record:
        r["criteri"] = ", ".join(r["criteri"])

    print(f"\nRecord unici: {len(record)}")
    print(f"Copie fisiche a Ragionieri: {sum(r['copie_ragionieri'] for r in record)}")

    with open(os.path.join(out_dir, "fumetti_ragionieri.json"), "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, "fumetti_ragionieri.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLONNE)
        for r in record:
            w.writerow(["; ".join(r[c]) if isinstance(r[c], list) else r[c] for c in COLONNE])
    print("Scritti fumetti_ragionieri.csv e fumetti_ragionieri.json")


if __name__ == "__main__":
    main()
