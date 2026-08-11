#!/usr/bin/env python3
"""Interroga il catalogo live titolo per titolo per le voci delle note Obsidian."""
import json, os, re, time, urllib.parse, urllib.request, sys
sys.path.insert(0, ".")
from estrai_fumetti import estrai_record, BASE, UA

CACHE = ".cache_verifica"
os.makedirs(CACHE, exist_ok=True)

# titoli alternativi/italiani da provare se il primo tentativo non trova nulla
ALIAS = {
    "The Dark Knight Returns": ["ritorno del cavaliere oscuro"],
    "Batman: Year One": ["Batman anno uno"],
    "A Contract with God": ["Contratto con Dio"],
    "Palestine": ["Palestina"], "El Eternauta": ["eternauta"],
    "The Arrival": ["approdo"], "L'approdo": ["approdo"],
    "Quartier lointain": ["In una lontana città"], "Arrugas": ["Rughe"],
    "Il grande male": ["grande male", "Ascension du Haut Mal"],
    "This One Summer": ["E la chiamano estate"],
    "Y: The Last Man": ["ultimo uomo"], "The Sandman": ["Sandman"],
    "Un printemps à Tchernobyl": ["Cernobyl", "Chernobyl"],
    "Gaston Lagaffe": ["Gaston"], "Spirou et Fantasio": ["Spirou"],
    "Les Cités Obscures": ["città oscure"], "Lanfeust de Troy": ["Lanfeust"],
    "Blake et Mortimer": ["Blake e Mortimer", "Blake"],
    "Groo the Wanderer": ["Groo"], "The Maxx": ["Maxx"],
    "When the Wind Blows": ["Quando soffia il vento"],
    "My Favorite Thing Is Monsters": ["cosa preferita sono i mostri"],
    "Ethel & Ernest": ["Ethel"], "Aya de Yopougon": ["Aya"],
    "L'Arabo del futuro": ["Arabo del futuro"],
    "Il Signor Bonaventura": ["Bonaventura"],
    "It's a Good Life, If You Don't Weaken": ["Good Life"],
    "Can't We Talk About Something More Pleasant?": ["Roz Chast"],
    "Locke & Key": ["Locke"], "Ken Parker": ["Ken Parker"],
    "Le straordinarie avventure di Pentothal": ["Pentothal"],
    "Cinque allegri ragazzi morti": ["allegri ragazzi morti"],
    "Una ballata del mare salato": ["ballata del mare salato"],
    "Il blu è un colore caldo": ["blu è un colore caldo"],
    "In una lontana città": ["lontana città"],
}


def cerca(campo, valore):
    fn = os.path.join(CACHE, re.sub(r"\W+", "_", f"{campo}_{valore}")[:120] + ".html")
    if os.path.exists(fn) and os.path.getsize(fn) > 5000:
        body = open(fn, encoding="utf-8", errors="replace").read()
    else:
        p = {"isPostBack": "1", campo: valore, "result_type": "list", "step": "50"}
        req = urllib.request.Request(BASE + "?" + urllib.parse.urlencode(p),
                                     headers={"User-Agent": UA})
        body = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
        open(fn, "w", encoding="utf-8").write(body)
        time.sleep(1.0)
    m = re.search(r"Risultati:\s*\d+-\d+ su (\d+)", body)
    tot = int(m.group(1)) if m else 0
    return tot, estrai_record(body)


voci = json.load(open("match.json", encoding="utf-8"))
esiti = []
for i, v in enumerate(voci, 1):
    titolo = v["titolo"]
    tentativi = [titolo] + ALIAS.get(titolo, [])
    tot, rec, usato = 0, [], titolo
    for t in tentativi:
        tot, rec = cerca("titolo", t)
        usato = t
        if tot:
            break
    # se il titolo non dà nulla, controllo almeno se l'autore è in catalogo
    autori_tot = 0
    if not tot and v["autore"]:
        cognome = [p for p in re.split(r"[&,]", v["autore"])[0].split() if len(p) > 3]
        if cognome:
            autori_tot, _ = cerca("autore", cognome[-1])
    esiti.append({**{k: v[k] for k in ("nota", "sezione", "titolo", "autore")},
                  "trovati": tot, "query_usata": usato, "autore_in_catalogo": autori_tot,
                  "record": [{k: r[k] for k in ("titolo", "anno", "editore_norm",
                                                "collocazioni", "copie_ragionieri", "url")}
                             for r in rec[:12]]})
    print(f"{i:3d}/{len(voci)} {tot:4d}  {titolo[:46]}", flush=True)

json.dump(esiti, open("obsidian_in_biblioteca.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nscritto obsidian_in_biblioteca.json")
