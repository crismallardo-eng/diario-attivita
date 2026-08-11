#!/usr/bin/env python3
"""Incrocia i titoli delle note Obsidian "Fumetti" e "Graphic Novel"
con il catalogo della Biblioteca Ragionieri."""
import json, re, unicodedata, sys

FUMETTI = """Avventura & Bonelli|Tex|Gian Luigi Bonelli & Aurelio Galleppini
Avventura & Bonelli|Zagor|Guido Nolitta & Gallieno Ferri
Avventura & Bonelli|Mister No|Guido Nolitta
Avventura & Bonelli|Dylan Dog|Tiziano Sclavi
Avventura & Bonelli|Martin Mystère|Alfredo Castelli
Avventura & Bonelli|Nathan Never|Medda, Serra & Vigna
Avventura & Bonelli|Dampyr|Mauro Boselli & Maurizio Colombo
Avventura & Bonelli|Julia|Giancarlo Berardi
Avventura & Bonelli|Ken Parker|Giancarlo Berardi & Ivo Milazzo
Avventura & Bonelli|Corto Maltese|Hugo Pratt
Nero & noir|Diabolik|Angela & Luciana Giussani
Umoristici IT|Alan Ford|Max Bunker & Magnus
Umoristici IT|Sturmtruppen|Bonvi
Umoristici IT|Cattivik|Bonvi & Silver
Umoristici IT|Lupo Alberto|Silver
Umoristici IT|Rat-Man|Leo Ortolani
Umoristici IT|Il Signor Bonaventura|Sto Sergio Tofano
Umoristici IT|Quasi signorina|
Autoriali IT|Zanardi|Andrea Pazienza
Autoriali IT|Le straordinarie avventure di Pentothal|Andrea Pazienza
Autoriali IT|La Dottrina|Alessandro Bilotta & Carmine Di Giandomenico
Autoriali IT|Valter Buio|Alessandro Bilotta
Autoriali IT|Cinque allegri ragazzi morti|Davide Toffolo
Autoriali IT|Squeak the Mouse|Massimo Mattioli
Autoriali IT|Il Commissario Spada|Gianni De Luca
Ragazzi IT|Topolino|Disney
Franco-belgi|Tintin|Hergé
Franco-belgi|Blake et Mortimer|Edgar P. Jacobs
Franco-belgi|Blueberry|Charlier & Giraud
Franco-belgi|Thorgal|Van Hamme & Rosinski
Franco-belgi|XIII|Van Hamme & Vance
Franco-belgi|Largo Winch|Van Hamme & Francq
Franco-belgi|Blacksad|Díaz Canales & Guarnido
Franco-belgi|Les Cités Obscures|Schuiten & Peeters
Franco-belgi|Valérian|Christin & Mézières
Franco-belgi|Lanfeust de Troy|Arleston & Tarquin
Franco-belgi|Asterix|Goscinny & Uderzo
Franco-belgi|Lucky Luke|Morris & Goscinny
Franco-belgi|Iznogoud|Goscinny & Tabary
Franco-belgi|Gaston Lagaffe|Franquin
Franco-belgi|Spirou et Fantasio|Franquin
Franco-belgi|Achille Talon|Greg
Franco-belgi|I Puffi|Peyo
Franco-belgi|Titeuf|Zep
Anglofoni|Transmetropolitan|Warren Ellis & Darick Robertson
Anglofoni|Watchmen|Alan Moore & Dave Gibbons
Anglofoni|V for Vendetta|Alan Moore & David Lloyd
Anglofoni|Swamp Thing|Alan Moore
Anglofoni|From Hell|Alan Moore & Eddie Campbell
Anglofoni|The Dark Knight Returns|Frank Miller
Anglofoni|Batman: Year One|Frank Miller & David Mazzucchelli
Anglofoni|Sin City|Frank Miller
Anglofoni|The Sandman|Neil Gaiman
Anglofoni|Spawn|Todd McFarlane
Anglofoni|Bone|Jeff Smith
Anglofoni|Hellboy|Mike Mignola
Anglofoni|Usagi Yojimbo|Stan Sakai
Anglofoni|Groo the Wanderer|Sergio Aragonés
Anglofoni|Saga|Brian K. Vaughan & Fiona Staples
Anglofoni|Fables|Bill Willingham
Anglofoni|Preacher|Garth Ennis & Steve Dillon
Anglofoni|Y: The Last Man|Brian K. Vaughan & Pia Guerra
Anglofoni|The Walking Dead|Robert Kirkman
Anglofoni|100 Bullets|Brian Azzarello & Eduardo Risso
Anglofoni|Locke & Key|Joe Hill & Gabriel Rodríguez
Anglofoni|Love and Rockets|Los Bros Hernandez
Anglofoni|Cerebus|Dave Sim
Anglofoni|Hate|Peter Bagge
Anglofoni|Stray Bullets|David Lapham
Anglofoni|The Maxx|Sam Kieth
Anglofoni|Strangers in Paradise|Terry Moore
Anglofoni|Tank Girl|Alan Martin & Jamie Hewlett
Anglofoni|Akiko|Mark Crilley
Anglofoni|Scary Godmother|Jill Thompson
Latinoamericani|El Eternauta|Oesterheld & Solano López
Latinoamericani|Mafalda|Quino"""

GRAPHIC = """Nordamericani|A Contract with God|Will Eisner
Nordamericani|Binky Brown Meets the Holy Virgin Mary|Justin Green
Nordamericani|Maus|Art Spiegelman
Nordamericani|Jimmy Corrigan|Chris Ware
Nordamericani|Building Stories|Chris Ware
Nordamericani|Fun Home|Alison Bechdel
Nordamericani|Black Hole|Charles Burns
Nordamericani|Ghost World|Daniel Clowes
Nordamericani|Here|Richard McGuire
Nordamericani|Asterios Polyp|David Mazzucchelli
Nordamericani|Blankets|Craig Thompson
Nordamericani|Stitches|David Small
Nordamericani|My Favorite Thing Is Monsters|Emil Ferris
Nordamericani|Sabrina|Nick Drnaso
Nordamericani|Stuck Rubber Baby|Howard Cruse
Nordamericani|Berlin|Jason Lutes
Nordamericani|Palestine|Joe Sacco
Nordamericani|Shortcomings|Adrian Tomine
Nordamericani|American Born Chinese|Gene Luen Yang
Nordamericani|Fax da Sarajevo|Joe Kubert
Nordamericani|Fahrenheit 451|Tim Hamilton
Nordamericani|It's a Good Life, If You Don't Weaken|Seth
Nordamericani|Louis Riel|Chester Brown
Nordamericani|Essex County|Jeff Lemire
Nordamericani|Ducks|Kate Beaton
Nordamericani|E la chiamano estate|Mariko & Jillian Tamaki
Nordamericani|This One Summer|Mariko & Jillian Tamaki
Nordamericani|Can't We Talk About Something More Pleasant?|Roz Chast
Nordamericani|Pyongyang|Guy Delisle
Britannici|When the Wind Blows|Raymond Briggs
Britannici|Ethel & Ernest|Raymond Briggs
Britannici|Gemma Bovery|Posy Simmonds
Britannici|The Arrival|Shaun Tan
Britannici|L'approdo|Shaun Tan
Britannici|Alice in Sunderland|Bryan Talbot
Franco-belgi|Persepolis|Marjane Satrapi
Franco-belgi|Il grande male|David B.
Franco-belgi|Pillole blu|Frederik Peeters
Franco-belgi|Il combattimento ordinario|Manu Larcenet
Franco-belgi|La guerra di Alan|Emmanuel Guibert
Franco-belgi|Il fotografo|Guibert, Lefèvre & Lemercier
Franco-belgi|Polina|Bastien Vivès
Franco-belgi|Portugal|Cyril Pedrosa
Franco-belgi|Aya de Yopougon|Marguerite Abouet & Clément Oubrerie
Franco-belgi|Il blu è un colore caldo|Jul Maroh
Franco-belgi|Un printemps à Tchernobyl|Emmanuel Lepage
Franco-belgi|Deogratias|Jean-Philippe Stassen
Franco-belgi|L'Arabo del futuro|Riad Sattouf
Franco-belgi|Il gatto del rabbino|Joann Sfar
Franco-belgi|Quai d'Orsay|Christophe Blain & Abel Lanzac
Franco-belgi|Cronache di Gerusalemme|Guy Delisle
Altri europei|Rughe|Paco Roca
Altri europei|Arrugas|Paco Roca
Altri europei|Paracuellos|Carlos Giménez
Altri europei|Heimat|Nora Krug
Altri europei|Logicomix|Doxiadis & Papadimitriou
Italiani|Una ballata del mare salato|Hugo Pratt
Italiani|La rivolta dei racchi|Guido Buzzelli
Italiani|Poema a fumetti|Dino Buzzati
Italiani|Gli ultimi giorni di Pompeo|Andrea Pazienza
Italiani|Fuochi|Lorenzo Mattotti
Italiani|Stigmate|Mattotti & Piersanti
Italiani|5 è il numero perfetto|Igort
Italiani|Appunti per una storia di guerra|Gipi
Italiani|Unastoria|Gipi
Italiani|La mia vita disegnata male|Gipi
Italiani|Cinquemila chilometri al secondo|Manuele Fior
Italiani|Kobane Calling|Zerocalcare
Italiani|Quaderni ucraini|Igort
Italiani|Sputa tre volte|Davide Reviati
Italiani|Il porto proibito|Radice & Turconi
Giapponesi|In una lontana città|Jiro Taniguchi
Giapponesi|Quartier lointain|Jiro Taniguchi
Giapponesi|Una vita tra i margini|Yoshihiro Tatsumi
Giapponesi|NonNonBa|Shigeru Mizuki
Giapponesi|L'uomo senza talento|Yoshiharu Tsuge
Resto del mondo|Exit Wounds|Rutu Modan"""

# titoli generici: richiedono anche il riscontro sull'autore
AMBIGUI = {"here", "berlin", "saga", "bone", "hate", "maus", "polina", "portugal",
           "fuochi", "julia", "sabrina", "greg", "spawn", "heimat", "ducks",
           "stitches", "blankets", "preacher", "tex", "xiii", "topolino"}


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip() + " "


def cognomi(autore):
    fuori = []
    for pezzo in re.split(r"[&,]", autore):
        pezzo = pezzo.strip()
        if not pezzo:
            continue
        parole = [p for p in pezzo.split() if len(p) > 2 and not p.endswith(".")]
        if parole:
            fuori.append(norm(parole[-1]).strip())
    return [c for c in fuori if len(c) > 3]


catalogo = json.load(open("fumetti_ragionieri.json", encoding="utf-8"))
for r in catalogo:
    r["_t"] = norm(r["titolo"])
    r["_d"] = norm(r["descrizione"])
    r["_c"] = norm(" ".join(r["collocazioni"]))

righe = [("Fumetti", l) for l in FUMETTI.splitlines()] + \
        [("Graphic Novel", l) for l in GRAPHIC.splitlines()]

risultati = []
for nota, riga in righe:
    sez, titolo, autore = (riga.split("|") + ["", ""])[:3]
    q = norm(titolo)
    surnames = cognomi(autore)
    hits = []
    for r in catalogo:
        campo = r["_t"] + "|" + r["_d"]
        if q not in campo:
            continue
        if norm(titolo).strip() in AMBIGUI:
            # titolo generico: pretendo anche l'autore
            if not any(s in campo for s in surnames):
                continue
        hits.append(r)
    # ripiego: l'autore c'è in catalogo, ma con altri titoli
    solo_autore = []
    if not hits and surnames:
        for r in catalogo:
            campo = r["_t"] + "|" + r["_d"]
            if any(" " + s + " " in campo for s in surnames):
                solo_autore.append(r)
    risultati.append({"nota": nota, "sezione": sez, "titolo": titolo,
                      "autore": autore, "hits": hits, "solo_autore": solo_autore})

def snella(h):
    return {k: h[k] for k in ("titolo","anno","editore_norm","collocazioni","url")}
json.dump([{"nota":r["nota"],"sezione":r["sezione"],"titolo":r["titolo"],"autore":r["autore"],
            "hits":[snella(h) for h in r["hits"]],
            "solo_autore":[snella(h) for h in r["solo_autore"]]} for r in risultati],
          open("match.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

t=[r for r in risultati if r["hits"]]
a=[r for r in risultati if not r["hits"] and r["solo_autore"]]
n=[r for r in risultati if not r["hits"] and not r["solo_autore"]]
print(f"voci: {len(risultati)} | titolo in catalogo: {len(t)} | solo autore: {len(a)} | assenti: {len(n)}")
print("\n### TITOLO PRESENTE")
for r in t:
    ess=r["hits"][0]
    coll=ess["collocazioni"][0] if ess["collocazioni"] else "-"
    print(f"{len(r['hits']):4d}v  {r['titolo'][:40]:40s} | es: {ess['titolo'][:52]:52s} | {coll}")
print("\n### SOLO AUTORE (altri titoli suoi)")
for r in a:
    print(f"{len(r['solo_autore']):4d}   {r['titolo'][:40]:40s} | {'; '.join(x['titolo'][:34] for x in r['solo_autore'][:3])}")
print("\n### ASSENTI")
for r in n: print("   -   ", r["titolo"], "—", r["autore"])
