#!/usr/bin/env python3
"""Genera in drive/ i CSV caricati su Google Drive.

- `obsidian_vs_biblioteca.csv`: una riga per ogni titolo delle note Obsidian,
  con l'esito del confronto col catalogo (da `verdetto_obsidian.json`).
- `parte1..8.csv`: il catalogo estratto, spezzato perché ogni file possa essere
  caricato singolarmente (da `fumetti_ragionieri.json`).
"""
import csv
import json
import os
import re
import unicodedata

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drive")
PARTI = 8


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip() + " "


def e_fumetto(coll):
    """Collocazioni della sezione fumetti: F|..., FT|741.59..., 741.5..."""
    c = coll.upper()
    return (c.startswith("F|") or c.startswith("FT|741")
            or "741.5" in c or "741,5" in c)


def esempio(record):
    """Preferisce un record a fumetti: il primo della lista può essere il DVD."""
    for r in record:
        if any(e_fumetto(c) for c in r["collocazioni"]):
            return r
    return record[0]


def altro_dello_stesso_autore(voce, catalogo):
    """Per i titoli assenti: cos'altro di quell'autore c'è a scaffale."""
    cognomi = [p for p in re.split(r"[&,]", voce["autore"])[0].split()
               if len(p) > 3 and not p.endswith(".")]
    if not cognomi:
        return ""
    ago = " " + norm(cognomi[-1]).strip() + " "
    trovati = [r["titolo"][:44] for r in catalogo
               if ago in norm(r["descrizione"])
               and any(e_fumetto(c) for c in r["collocazioni"])]
    return "; ".join(dict.fromkeys(trovati))[:180]


def scrivi(nome, intestazione, righe):
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(intestazione)
        w.writerows(righe)
    print(f"  {nome}: {len(righe)} righe")


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(OUT, exist_ok=True)
    catalogo = json.load(open(os.path.join(base, "fumetti_ragionieri.json"), encoding="utf-8"))
    verdetto = json.load(open(os.path.join(base, "verdetto_obsidian.json"), encoding="utf-8"))

    righe = []
    for esito, chiave in (("IN BIBLIOTECA", "in_biblioteca"), ("DA VERIFICARE", "da_verificare")):
        for x in verdetto[chiave]:
            v, r = x["voce"], esempio(x["record"])
            righe.append([esito, v["nota"], v["titolo"], v["autore"], len(x["record"]),
                          r["titolo"], r["anno"], (r["collocazioni"] or ["-"])[0], r["url"], ""])
    for v in verdetto["assenti"]:
        righe.append(["ASSENTE", v["nota"], v["titolo"], v["autore"], 0,
                      v.get("motivo_declassamento", ""), "", "", "",
                      altro_dello_stesso_autore(v, catalogo)])
    scrivi("obsidian_vs_biblioteca.csv",
           ["Esito", "Nota Obsidian", "Titolo", "Autore", "N. record",
            "Record in catalogo", "Anno", "Collocazione", "Link",
            "Altro dello stesso autore"], righe)

    colonne = ["codice", "titolo", "editore_norm", "anno", "collocazioni"]
    testata = ["Codice", "Titolo", "Editore", "Anno", "Collocazione"]
    tutte = [["; ".join(r[c]) if isinstance(r[c], list) else str(r[c]) for c in colonne]
             for r in catalogo]
    per_parte = -(-len(tutte) // PARTI)
    for i in range(PARTI):
        blocco = tutte[i * per_parte:(i + 1) * per_parte]
        if blocco:
            scrivi(f"parte{i + 1}.csv", testata, blocco)


if __name__ == "__main__":
    main()
