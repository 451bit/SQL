# Kapitel 3: Schwache Entitäten im ER-Diagramm

**Notation:** Chen-Notation  
**Thema:** Schwache Entitäten – Modellierung und Übertragung ins relationale Modell

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md)

---

## 1. Zum Einstieg – ein Problem mit gewöhnlichen Entitäten

Stell dir vor, du modellierst ein System für eine Schule. Eine Klasse hat mehrere Schüler. Jede Klasse hat außerdem mehrere **Sitzplätze**, die nummeriert sind (Platz 1, Platz 2, …).

Du möchtest festhalten, welcher Schüler auf welchem Sitzplatz sitzt.

Dein erste Idee: Eine Entität `Sitzplatz` mit dem Primärschlüssel `Platznummer`.

**Das Problem:** Die Platznummer 1 gibt es in *jeder* Klasse. Platz 1 in der 9a ist ein anderer Platz als Platz 1 in der 10b. Die Platznummer alleine identifiziert einen Sitzplatz **nicht eindeutig** – man braucht immer auch die Klasse dazu.

Ein `Sitzplatz` **existiert nur im Kontext einer Klasse** – ohne die zugehörige Klasse ergibt er keinen Sinn.

Solche Entitäten nennt man **schwache Entitäten**.

---

## 2. Was ist eine schwache Entität?

Eine **schwache Entität** ist eine Entität, die:

- **keinen eigenen, vollständigen Primärschlüssel** besitzt,
- zur eindeutigen Identifikation **zwingend eine andere Entität** (die **starke Entität** oder **Eigentümer-Entität**) benötigt,
- in ihrer Existenz **abhängig** von der starken Entität ist: Wird die starke Entität gelöscht, verlieren die schwachen Entitäten ihren Sinn (oder dürfen nicht mehr existieren).

Das Attribut, das die schwache Entität *innerhalb* ihrer starken Entität eindeutig macht, heißt **partieller Schlüssel** (oder Diskriminator).

| Begriff | Bedeutung |
|---|---|
| Schwache Entität | Entität ohne vollständigen eigenen Primärschlüssel |
| Starke Entität / Eigentümer | Die Entität, von der die schwache abhängt |
| Partieller Schlüssel | Attribut, das die schwache Entität *innerhalb* der starken identifiziert |
| Identifizierende Beziehung | Die Beziehung zwischen schwacher und starker Entität |

---

## 3. Darstellung in der Chen-Notation

In der Chen-Notation werden schwache Entitäten mit **doppelten Linien** dargestellt:

| Element | Darstellung in Chen |
|---|---|
| Starke Entität | Einfaches Rechteck `[ ]` |
| Schwache Entität | **Doppeltes** Rechteck `[[ ]]` |
| Identifizierende Beziehung | **Doppelte** Raute `<< >>` |
| Partieller Schlüssel | Attribut mit **gestrichelter** Unterstreichung |
| Primärschlüssel (stark) | Attribut mit **durchgezogener** Unterstreichung |

### Beispiel: Klasse und Sitzplatz

```
[Klasse] ----<<hat>>---- [[Sitzplatz]]
  |                           |
klasse_id (PK)         platznummer (partieller Schlüssel, gestrichelt unterstrichen)
bezeichnung            reihe
```

Textuell beschrieben (da Diagramme in Markdown nicht direkt gezeichnet werden können):

- `Klasse` ist die starke Entität mit Primärschlüssel `klasse_id`
- `Sitzplatz` ist die schwache Entität mit partiellem Schlüssel `platznummer`
- Die identifizierende Beziehung `hat` verbindet beide (dargestellt als **doppelte Raute**)
- Ein Sitzplatz wird vollständig identifiziert durch: `(klasse_id, platznummer)`

---

## 4. Übertragung ins relationale Modell

Beim Übertragen in das relationale Modell gilt für schwache Entitäten:

1. Die schwache Entität wird zur eigenen Tabelle.
2. Der **Primärschlüssel der starken Entität** wird als **Fremdschlüssel** in die Tabelle der schwachen Entität übernommen.
3. Der **zusammengesetzte Primärschlüssel** der schwachen Entität besteht aus: **Fremdschlüssel + partieller Schlüssel**.

### Beispiel: Klasse und Sitzplatz

**ER-Diagramm (textuell):**
```
[Klasse(klasse_id, bezeichnung)]  ----<<hat>>----  [[Sitzplatz(platznummer, reihe)]]
```

**Relationales Modell:**
```
Klasse(klasse_id, bezeichnung)
Sitzplatz(klasse_id, platznummer, reihe)
          ^^^^^^^^  ^^^^^^^^^^^
          FK→Klasse  partieller Schlüssel
          └──────── zusammen: Primärschlüssel ────────┘
```

In SQL:
```sql
CREATE TABLE Klasse (
    klasse_id   INTEGER PRIMARY KEY,
    bezeichnung TEXT NOT NULL
);

CREATE TABLE Sitzplatz (
    klasse_id   INTEGER REFERENCES Klasse(klasse_id),
    platznummer INTEGER NOT NULL,
    reihe       INTEGER,
    PRIMARY KEY (klasse_id, platznummer)
);
```

---

## 5. Wann ist eine schwache Entität sinnvoll?

Schwache Entitäten treten typischerweise auf, wenn:

- Dinge **nur innerhalb eines Kontexts** existieren und nummeriert sind (Stockwerke in Gebäuden, Kapitel in Büchern, Bestellpositionen in einer Bestellung, …)
- Die **Existenz** des Objekts ohne die übergeordnete Entität keinen Sinn ergibt
- Verschiedene Instanzen der starken Entität jeweils ihre eigene „Zählung" haben

**Gegenprobe – wann ist es *keine* schwache Entität?**  
Eine Entität ist stark, wenn sie einen globalen Primärschlüssel hat, der sie überall eindeutig identifiziert (z. B. eine Person über Personalausweisnummer, ein Produkt über EAN).

---

## 6. Übungsaufgaben

### Aufgabe 1 – Wohnung und Zimmer

Ein Vermieter verwaltet mehrere **Wohnungen**. Jede Wohnung hat mehrere **Zimmer**, die innerhalb der Wohnung nummeriert sind (Zimmer 1, Zimmer 2, …). Jedes Zimmer hat eine Größe in m².

**a)** Identifiziere die starke und die schwache Entität. Begründe, warum es sich um eine schwache Entität handelt.

**b)** Zeichne das ER-Diagramm in Chen-Notation. Kennzeichne schwache Entität, identifizierende Beziehung und partiellen Schlüssel korrekt.

**c)** Übertrage das Diagramm in das relationale Modell. Gib Primär- und Fremdschlüssel an.

<details>
<summary>Lösung</summary>

**a)** Starke Entität: `Wohnung` (hat eigene, eindeutige ID).  
Schwache Entität: `Zimmer` – die Zimmernummer ist nur innerhalb einer Wohnung eindeutig. Zimmer 1 in Wohnung 10 ist nicht dasselbe wie Zimmer 1 in Wohnung 11. Ohne die Wohnung ergibt ein Zimmer keinen Sinn.

**b)** ER-Diagramm (textuell):
```
[Wohnung] ----<<enthält>>---- [[Zimmer]]
  |                                |
wohnungs_id (PK)          zimmernr (partieller Schlüssel)
adresse                   groesse_qm
```

**c)** Relationales Modell:
```
Wohnung(wohnungs_id, adresse)
Zimmer(wohnungs_id, zimmernr, groesse_qm)
       ^^^^^^^^^^^ ^^^^^^^^^
       FK→Wohnung  partieller Schlüssel
       └──── gemeinsam: Primärschlüssel ────┘
```
</details>

---

### Aufgabe 2 – Buch und Kapitel

Ein **Buch** besteht aus mehreren **Kapiteln**. Jedes Kapitel hat eine Kapitelnummer (1, 2, 3, …) und einen Titel. Die Kapitelnummer ist nur innerhalb eines Buches eindeutig.

**a)** Warum ist `Kapitel` eine schwache Entität?

**b)** Zeichne das ER-Diagramm in Chen-Notation.

**c)** Übertrage das Diagramm in das relationale Modell.

<details>
<summary>Lösung</summary>

**a)** Kapitelnnummer 1 gibt es in jedem Buch. Ohne das Buch lässt sich ein Kapitel nicht eindeutig identifizieren. Die Existenz eines Kapitels ist direkt an ein Buch gebunden.

**b)** ER-Diagramm (textuell):
```
[Buch] ----<<besteht_aus>>---- [[Kapitel]]
  |                                  |
buch_id (PK)               kapitelnr (partieller Schlüssel)
titel                      kapitel_titel
isbn
```

**c)** Relationales Modell:
```
Buch(buch_id, titel, isbn)
Kapitel(buch_id, kapitelnr, kapitel_titel)
        ^^^^^^^  ^^^^^^^^^
        FK→Buch  partieller Schlüssel
        └──── gemeinsam: Primärschlüssel ────┘
```
</details>

---

### Aufgabe 3 – Bestellung und Bestellposition

Ein Online-Shop verwaltet **Bestellungen**. Jede Bestellung enthält mehrere **Bestellpositionen** (Position 1, Position 2, …). Jede Position enthält ein Produkt und eine Menge.

**a)** Begründe, warum `Bestellposition` eine schwache Entität ist.

**b)** Zeichne das vollständige ER-Diagramm. Beachte: Ein Produkt ist eine eigenständige starke Entität (`produkt_id`, `name`, `preis`). Die Bestellposition verknüpft Bestellung und Produkt.

**c)** Übertrage das Diagramm ins relationale Modell.

<details>
<summary>Lösung</summary>

**a)** Die Positionsnummer ist nur innerhalb einer Bestellung eindeutig. Position 1 in Bestellung 100 ist eine andere als Position 1 in Bestellung 200. Ohne die Bestellung hat eine Bestellposition keinen Sinn.

**b)** ER-Diagramm (textuell):
```
[Bestellung] ----<<enthält>>---- [[Bestellposition]] ----<betrifft>---- [Produkt]
     |                                   |                                   |
bestell_id (PK)               positionsnr (partieller Schlüssel)       produkt_id (PK)
datum                         menge                                    name
                                                                        preis
```

**c)** Relationales Modell:
```
Bestellung(bestell_id, datum)
Produkt(produkt_id, name, preis)
Bestellposition(bestell_id, positionsnr, produkt_id, menge)
                ^^^^^^^^^^  ^^^^^^^^^^^  ^^^^^^^^^^
                FK→Bestellung  part. Schl.  FK→Produkt
                └──────── gemeinsam PK: (bestell_id, positionsnr) ────────┘
```
</details>

---

### Aufgabe 4 – Gebäude, Stockwerk und Raum

Eine Universität hat mehrere **Gebäude**. Jedes Gebäude hat mehrere **Stockwerke** (EG, 1. OG, 2. OG, …). Jedes Stockwerk hat mehrere **Räume**, die stockwerkintern nummeriert sind (Raum 1, Raum 2, …). Ein Raum hat eine Kapazität (Anzahl Sitzplätze).

Hier gibt es **zwei Ebenen** von schwachen Entitäten.

**a)** Identifiziere alle Entitäten und begründe, welche schwach sind.

**b)** Zeichne das ER-Diagramm. Beachte die korrekte Darstellung beider schwacher Entitäten.

**c)** Übertrage das Diagramm ins relationale Modell. Achte auf die zusammengesetzten Primärschlüssel.

<details>
<summary>Lösung</summary>

**a)**  
- `Gebäude`: starke Entität (hat eigene `gebaeude_id`)  
- `Stockwerk`: schwach – die Stockwerknummer ist nur innerhalb eines Gebäudes eindeutig, ein Stockwerk ohne Gebäude macht keinen Sinn  
- `Raum`: schwach – die Raumnummer ist nur innerhalb eines Stockwerks eindeutig, ein Raum ohne sein Stockwerk (und damit ohne sein Gebäude) macht keinen Sinn

**b)** ER-Diagramm (textuell):
```
[Gebäude] ----<<hat>>---- [[Stockwerk]] ----<<enthält>>---- [[Raum]]
   |                           |                                |
gebaeude_id (PK)       stockwerknr (part. S.)         raumnr (part. S.)
name                   bezeichnung                    kapazitaet
```

**c)** Relationales Modell:
```
Gebaeude(gebaeude_id, name)

Stockwerk(gebaeude_id, stockwerknr, bezeichnung)
          ^^^^^^^^^^^  ^^^^^^^^^^^
          FK→Gebaeude  partieller Schlüssel
          └──── PK: (gebaeude_id, stockwerknr) ────┘

Raum(gebaeude_id, stockwerknr, raumnr, kapazitaet)
     ^^^^^^^^^^^  ^^^^^^^^^^^  ^^^^^^
     └── FK→Stockwerk(gebaeude_id, stockwerknr) ──┘  partieller Schlüssel
     └──────── PK: (gebaeude_id, stockwerknr, raumnr) ────────┘
```
</details>

---

### Aufgabe 5 – Freier Text

Lies den folgenden Text und erstelle daraus ein ER-Diagramm sowie das relationale Modell.

> Ein Musikstreaming-Dienst verwaltet **Alben**. Jedes Album hat einen Titel, ein Erscheinungsjahr und gehört einem **Künstler** (Name, Herkunftsland). Ein Album besteht aus mehreren **Titeln** (Songs). Jeder Titel auf einem Album hat eine Tracknummer (1, 2, 3, …), einen Namen und eine Länge in Sekunden. Die gleiche Tracknummer kann auf verschiedenen Alben vorkommen.

**a)** Identifiziere alle Entitäten. Welche sind schwach, welche stark?

**b)** Zeichne das vollständige ER-Diagramm in Chen-Notation.

**c)** Übertrage das Diagramm ins relationale Modell.

<details>
<summary>Lösung</summary>

**a)**  
- `Künstler`: stark (eigene `kuenstler_id`)  
- `Album`: stark (eigene `album_id`; ein Album ist mit einer ISBN/Katalognummer global identifizierbar)  
- `Titel` (Song): **schwach** – die Tracknummer ist nur innerhalb eines Albums eindeutig; ein Track ohne Album macht keinen Sinn

**b)** ER-Diagramm (textuell):
```
[Künstler] ----<veröffentlicht>---- [Album] ----<<enthält>>---- [[Titel]]
    |                                  |                             |
kuenstler_id (PK)               album_id (PK)              tracknr (partieller Schlüssel)
name                            albumtitel                  songname
herkunftsland                   erscheinungsjahr            laenge_sek
```

**c)** Relationales Modell:
```
Kuenstler(kuenstler_id, name, herkunftsland)

Album(album_id, albumtitel, erscheinungsjahr, kuenstler_id)
                                              ^^^^^^^^^^^
                                              FK→Kuenstler

Titel(album_id, tracknr, songname, laenge_sek)
      ^^^^^^^^  ^^^^^^^
      FK→Album  partieller Schlüssel
      └──── PK: (album_id, tracknr) ────┘
```
</details>
