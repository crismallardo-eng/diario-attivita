#!/usr/bin/env python3
"""Filtra i risultati della ricerca live: tiene solo i record che sono davvero
fumetti (collocazione della sezione fumetti) e dell'autore giusto."""
import json, re, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip() + " "

def e_fumetto(coll):
    """La sezione fumetti della Ragionieri: F|..., FT|741.59..., 741.5..."""
    c = coll.upper()
    return (c.startswith("F|") or c.startswith("FT|741") or "741.5" in c
            or "741,5" in c or c.startswith("F ") or c.startswith("F|741"))

def cognomi(autore):
    out = []
    for pezzo in re.split(r"[&,]", autore):
        parole = [p for p in pezzo.split() if len(p) > 3 and not p.endswith(".")]
        if parole:
            out.append(norm(parole[-1]).strip())
    return out

voci = json.load(open("obsidian_in_biblioteca.json", encoding="utf-8"))
si, forse, no = [], [], []
for v in voci:
    cogn = cognomi(v["autore"])
    buoni = []
    for r in v["record"]:
        campo = norm(r["titolo"])
        autore_ok = bool(cogn) and any(c in campo for c in cogn)
        coll_ok = any(e_fumetto(c) for c in r["collocazioni"])
        if autore_ok:
            # l'autore compare nel record: riscontro certo, anche se sta in magazzino
            buoni.append(r)
        elif coll_ok:
            # collocazione da fumetti ma autore non confermato: dubbio
            buoni.append(dict(r, _dubbio=True))
    certi = [r for r in buoni if not r.get("_dubbio")]
    if certi:
        si.append((v, certi))
    elif buoni:
        forse.append((v, buoni))
    else:
        no.append(v)

print(f"IN BIBLIOTECA: {len(si)}   DA VERIFICARE: {len(forse)}   ASSENTI: {len(no)}\n")
print("=" * 78, "\n### IN BIBLIOTECA\n")
for v, rs in si:
    r = rs[0]
    print(f"- {v['titolo']} — {v['autore']}")
    print(f"    {len(rs)} record · es. \"{r['titolo'][:60]}\" ({r['anno']}) · {r['collocazioni'][0]}")
print("\n" + "=" * 78, "\n### DA VERIFICARE (collocazione da fumetti ma autore non confermato)\n")
for v, rs in forse:
    print(f"- {v['titolo']} — {v['autore']}  ->  \"{rs[0]['titolo'][:60]}\" {rs[0]['collocazioni'][0]}")
print("\n" + "=" * 78, "\n### NON IN CATALOGO\n")
for v in no:
    print(f"- {v['titolo']} — {v['autore']}"
          + (f"   [dell'autore ci sono {v['autore_in_catalogo']} record]" if v["autore_in_catalogo"] else ""))

json.dump({"in_biblioteca": [{"voce": v, "record": rs} for v, rs in si],
           "da_verificare": [{"voce": v, "record": rs} for v, rs in forse],
           "assenti": no},
          open("verdetto_obsidian.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
