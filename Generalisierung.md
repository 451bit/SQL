# Kapitel 5: Generalisierung im ER-Diagramm (is-a-Beziehung)

**Notation:** Chen-Notation  
**Thema:** Generalisierung und Spezialisierung – Modellierung und Übertragung ins relationale Modell

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md) · [Kapitel 7 – DML in SQL](DML.md) · [Projekt – Wetterdatenbank](Projekt_Wetterdatenbank.md)

---

## 1. Zum Einstieg – ein Modellierungsproblem

Du entwickelst eine Datenbank für eine Schule. Es gibt **Schüler** und **Lehrer**. Beide haben gemeinsame Eigenschaften:

- Vorname, Nachname, Geburtsdatum, E-Mail-Adresse

Aber sie haben auch **unterschiedliche** Eigenschaften:
- Schüler: Klasse, Notendurchschnitt
- Lehrer: Personalnummer, Fachbereich, Gehalt

**Erste Idee: Alles in eine Tabelle**

```
Person(person_id, vorname, nachname, geburtsdatum, email, klasse_id, notendurchschnitt, personalnummer, fachbereich, gehalt)
```

**Problem:** Bei einem Schüler sind `personalnummer`, `fachbereich` und `gehalt` immer leer. Bei einem Lehrer sind `klasse_id` und `notendurchschnitt` immer leer. Viele `NULL`-Werte und unklare Struktur.

**Zweite Idee: Zwei völlig getrennte Tabellen**

```
Schueler(schueler_id, vorname, nachname, geburtsdatum, email, klasse_id, notendurchschnitt)
Lehrer(lehrer_id, vorname, nachname, geburtsdatum, email, personalnummer, fachbereich, gehalt)
```

**Problem:** Die gemeinsamen Attribute `vorname`, `nachname`, `geburtsdatum`, `email` sind doppelt – Redundanz, die zu Widersprüchen führen kann.

**Die Lösung:** Generalisierung – gemeinsame Eigenschaften werden in einer übergeordneten Entität zusammengefasst.

---

## 2. Was ist Generalisierung?

**Generalisierung** ist das Zusammenfassen gemeinsamer Eigenschaften mehrerer Entitäten in einer allgemeinen, übergeordneten Entität.

Das Gegenstück heißt **Spezialisierung**: Man nimmt eine allgemeine Entität und verfeinert sie in speziellere Untertypen.

| Begriff | Bedeutung |
|---|---|
| **Supertyp** (Obertyp) | Die allgemeine Entität mit gemeinsamen Eigenschaften |
| **Subtyp** (Untertyp) | Die spezialisierte Entität mit eigenen zusätzlichen Eigenschaften |
| **is-a-Beziehung** | „Ein Schüler ist eine Person" – Subtyp ist ein Spezialfall des Supertyps |
| **Generalisierung** | Gemeinsamkeiten nach oben zusammenfassen |
| **Spezialisierung** | Einen Typ in Untertypen aufteilen |

Die Beziehung zwischen Supertyp und Subtyp heißt **is-a-Beziehung** (englisch: „is a"), weil gilt:
- Ein Schüler **ist eine** Person
- Ein Lehrer **ist eine** Person

Jeder Subtyp **erbt** alle Attribute des Supertyps.

---

## 3. Darstellung in der Chen-Notation

In der Chen-Notation wird die Generalisierung durch eine **Raute** mit der Beschriftung **„is-a"** dargestellt – genau wie eine normale Beziehung. Der Unterschied: Ein **Pfeil** zeigt vom Subtyp in Richtung des **Supertyps** und kennzeichnet so die is-a-Richtung.

```
    [Schüler] ──→──┐
                 <is-a>
    [Lehrer]  ──→──┘
                   │
              [Person]
```

Der Pfeil bedeutet: „Schüler ist eine Person", „Lehrer ist eine Person" – der Subtyp zeigt auf seinen Supertyp.

> **Kardinalität der is-a-Beziehung:**  
> Die Kardinalität zwischen Subtyp und Supertyp ist immer **1:1** – jede Instanz des Subtyps entspricht genau einer Instanz des Supertyps. Die Optionalität ist **kann** auf der Supertyp-Seite (eine Person muss kein Schüler sein) und **muss** auf der Subtyp-Seite (jeder Schüler ist zwingend eine Person). Da diese Kardinalität bei der is-a-Beziehung **immer gleich** ist, wird sie in der Regel **weggelassen**.

### Vollständiges Beispiel mit Attributen

```
vorname  nachname  geburtsdatum  email
   \        |          |        /
           [Person]
           person_id (PK)
               ↑
            <is-a>
           ↗        ↖
     [Schüler]    [Lehrer]
          |              |
    klasse_id     personalnummer
    notendurch-   fachbereich
    schnitt       gehalt
```

Textuell beschrieben:
- `Person` ist der **Supertyp** mit Primärschlüssel `person_id` und den Attributen `vorname`, `nachname`, `geburtsdatum`, `email`
- `Schüler` ist ein **Subtyp** mit den zusätzlichen Attributen `klasse_id`, `notendurchschnitt`
- `Lehrer` ist ein **Subtyp** mit den zusätzlichen Attributen `personalnummer`, `fachbereich`, `gehalt`
- Die Pfeile zeigen jeweils vom Subtyp zur Raute und von der Raute zum Supertyp
- Jeder Schüler und jeder Lehrer **erbt** automatisch alle Attribute von `Person`

---

## 4. Vollständigkeit und Disjunktheit

Zwei wichtige Eigenschaften der Generalisierung:

**Vollständigkeit** (Total vs. Partiell):
- **Totale Generalisierung:** Jede Instanz des Supertyps gehört zu mindestens einem Subtyp. Es gibt keine „generische" Person, die weder Schüler noch Lehrer ist. (Darstellung: doppelte Linie zwischen Raute und Supertyp)
- **Partielle Generalisierung:** Es kann Instanzen des Supertyps geben, die zu keinem Subtyp gehören. (einfache Linie)

**Disjunktheit** (Disjunkt vs. Überlappend):
- **Disjunkt:** Eine Instanz kann nur zu genau einem Subtyp gehören. Ein Mensch ist entweder Schüler oder Lehrer, nicht beides.
- **Überlappend:** Eine Instanz kann gleichzeitig zu mehreren Subtypen gehören. (seltenere Sonderfälle)

In Schulszenarien ist die Generalisierung meistens **total und disjunkt**: Jede Person ist entweder Schüler oder Lehrer, und kann nicht beides gleichzeitig sein.

---

## 5. Überführung ins relationale Modell – drei Strategien

Es gibt drei gängige Strategien, eine Generalisierung ins relationale Modell zu überführen.

### Strategie 1: Eine gemeinsame Tabelle für alle (Flat Table)

Alle Attribute des Supertyps und aller Subtypen kommen in eine einzige Tabelle. Eine zusätzliche Spalte (`typ`) gibt an, welcher Subtyp gemeint ist.

```
Person(person_id, vorname, nachname, geburtsdatum, email, typ,
       klasse_id, notendurchschnitt,           ← nur für Schüler
       personalnummer, fachbereich, gehalt)    ← nur für Lehrer
```

**SQL:**
```sql
CREATE TABLE Person (
    person_id          INTEGER PRIMARY KEY,
    vorname            TEXT NOT NULL,
    nachname           TEXT NOT NULL,
    geburtsdatum       TEXT,
    email              TEXT,
    typ                TEXT NOT NULL CHECK (typ IN ('Schueler', 'Lehrer')),
    -- Schüler-spezifisch:
    klasse_id          INTEGER,
    notendurchschnitt  REAL,
    -- Lehrer-spezifisch:
    personalnummer     TEXT,
    fachbereich        TEXT,
    gehalt             REAL
);
```

| Vorteile | Nachteile |
|---|---|
| Nur eine Tabelle, einfache Abfragen | Viele `NULL`-Werte (Schüler-Spalten bei Lehrern leer) |
| Kein JOIN nötig | Unübersichtlich bei vielen Subtypen |
| Gut bei einfacher Generalisierung | Keine erzwingbare Trennung der Subtyp-Attribute |

---

### Strategie 2: Tabelle für Supertyp + Tabellen für Subtypen (empfohlen)

Der Supertyp bekommt eine eigene Tabelle. Jeder Subtyp bekommt ebenfalls eine eigene Tabelle, deren **Primärschlüssel gleichzeitig Fremdschlüssel** auf den Supertyp ist.

```
Person(person_id, vorname, nachname, geburtsdatum, email)
Schueler(person_id, klasse_id, notendurchschnitt)
         ^^^^^^^^^
         PK und FK→Person
Lehrer(person_id, personalnummer, fachbereich, gehalt)
       ^^^^^^^^^
       PK und FK→Person
```

**SQL:**
```sql
CREATE TABLE Person (
    person_id    INTEGER PRIMARY KEY,
    vorname      TEXT NOT NULL,
    nachname     TEXT NOT NULL,
    geburtsdatum TEXT,
    email        TEXT
);

CREATE TABLE Schueler (
    person_id         INTEGER PRIMARY KEY REFERENCES Person(person_id),
    klasse_id         INTEGER REFERENCES Klasse(klasse_id),
    notendurchschnitt REAL
);

CREATE TABLE Lehrer (
    person_id      INTEGER PRIMARY KEY REFERENCES Person(person_id),
    personalnummer TEXT UNIQUE,
    fachbereich    TEXT,
    gehalt         REAL
);
```

> **Schlüssel:** `person_id` in `Schueler` und `Lehrer` ist gleichzeitig **Primärschlüssel** und **Fremdschlüssel** auf `Person`. Dadurch ist garantiert, dass jeder Schüler und jeder Lehrer auch in `Person` eingetragen ist.

**Abfrage: Alle Schüler mit Namen**
```sql
SELECT p.vorname, p.nachname, s.klasse_id
FROM Person p
JOIN Schueler s ON p.person_id = s.person_id;
```

| Vorteile | Nachteile |
|---|---|
| Klare Trennung der Subtypen | JOINs nötig bei vollständigen Abfragen |
| Keine unnötigen `NULL`-Werte | Zwei Tabellen pro Entität |
| Gute Erweiterbarkeit | |

---

### Strategie 3: Nur Tabellen für Subtypen (Kein Supertyp)

Es gibt keine Supertyp-Tabelle. Jeder Subtyp bekommt eine vollständige Tabelle, die **alle Attribute des Supertyps wiederholt**.

```
Schueler(schueler_id, vorname, nachname, geburtsdatum, email, klasse_id, notendurchschnitt)
Lehrer(lehrer_id, vorname, nachname, geburtsdatum, email, personalnummer, fachbereich, gehalt)
```

**SQL:**
```sql
CREATE TABLE Schueler (
    schueler_id       INTEGER PRIMARY KEY,
    vorname           TEXT NOT NULL,
    nachname          TEXT NOT NULL,
    geburtsdatum      TEXT,
    email             TEXT,
    klasse_id         INTEGER,
    notendurchschnitt REAL
);

CREATE TABLE Lehrer (
    lehrer_id      INTEGER PRIMARY KEY,
    vorname        TEXT NOT NULL,
    nachname       TEXT NOT NULL,
    geburtsdatum   TEXT,
    email          TEXT,
    personalnummer TEXT UNIQUE,
    fachbereich    TEXT,
    gehalt         REAL
);
```

| Vorteile | Nachteile |
|---|---|
| Einfache Abfragen pro Subtyp | Redundanz: gemeinsame Attribute wiederholt |
| Kein JOIN für vollständige Daten | Inkonsistenzen möglich |
| Gut wenn Subtypen selten zusammen abgefragt werden | Schwierig, wenn alle Personen zusammen abgefragt werden |

---

### Zusammenfassung: Wann welche Strategie?

| Situation | Empfohlene Strategie |
|---|---|
| Wenige Subtypen, wenige spezifische Attribute | Strategie 1 (eine Tabelle) |
| Klare Trennung gewünscht, JOINs akzeptabel | **Strategie 2** (empfohlen in den meisten Fällen) |
| Subtypen haben sehr wenig gemeinsam, werden selten zusammen abgefragt | Strategie 3 |

---

## 6. Übungsaufgaben

### Aufgabe 1 – Fahrzeuge

Ein Unternehmen verwaltet seinen Fahrzeugpark. Es gibt **PKW** und **LKW**. Beide haben: `fahrzeug_id` (PK), `kennzeichen`, `baujahr`, `marke`. PKW haben zusätzlich: `anzahl_sitzplaetze`, `motorisierung`. LKW haben zusätzlich: `ladekapazitaet_tonnen`, `anzahl_achsen`.

**a)** Modelliere das ER-Diagramm mit Generalisierung in Chen-Notation. Kennzeichne Supertyp, Subtypen und is-a-Beziehung.

**b)** Überführe das Diagramm in das relationale Modell nach **Strategie 2** (Supertyp + Subtypen).

**c)** Schreibe die SQL-`CREATE TABLE`-Anweisungen.

**d)** Schreibe eine SQL-Abfrage, die alle PKW mit Kennzeichen und Anzahl Sitzplätze ausgibt.

<details>
<summary>Lösung</summary>

**a)** ER-Diagramm (textuell):
```
kennzeichen  baujahr  marke
     \          |       /
            [Fahrzeug]
            fahrzeug_id (PK)
                 |
              (is-a)
             /       \
          [PKW]      [LKW]
            |              |
  anzahl_sitzplaetze  ladekapazitaet_tonnen
  motorisierung       anzahl_achsen
```

**b)** Relationales Modell (Strategie 2):
```
Fahrzeug(fahrzeug_id, kennzeichen, baujahr, marke)
PKW(fahrzeug_id, anzahl_sitzplaetze, motorisierung)
    ^^^^^^^^^^^
    PK und FK→Fahrzeug
LKW(fahrzeug_id, ladekapazitaet_tonnen, anzahl_achsen)
    ^^^^^^^^^^^
    PK und FK→Fahrzeug
```

**c)** SQL:
```sql
CREATE TABLE Fahrzeug (
    fahrzeug_id INTEGER PRIMARY KEY,
    kennzeichen TEXT NOT NULL UNIQUE,
    baujahr     INTEGER,
    marke       TEXT
);

CREATE TABLE PKW (
    fahrzeug_id          INTEGER PRIMARY KEY REFERENCES Fahrzeug(fahrzeug_id),
    anzahl_sitzplaetze   INTEGER,
    motorisierung        TEXT
);

CREATE TABLE LKW (
    fahrzeug_id             INTEGER PRIMARY KEY REFERENCES Fahrzeug(fahrzeug_id),
    ladekapazitaet_tonnen   REAL,
    anzahl_achsen           INTEGER
);
```

**d)** SQL-Abfrage:
```sql
SELECT f.kennzeichen, p.anzahl_sitzplaetze
FROM Fahrzeug f
JOIN PKW p ON f.fahrzeug_id = p.fahrzeug_id;
```
</details>

---

### Aufgabe 2 – Mitarbeiter eines Krankenhauses

Ein Krankenhaus beschäftigt **Ärzte** und **Pflegepersonal**. Alle sind Mitarbeiter mit: `mitarbeiter_id` (PK), `vorname`, `nachname`, `einstellungsdatum`. Ärzte haben zusätzlich: `fachgebiet`, `approbationsnummer`. Pflegepersonal hat: `station`, `schichtmodell`.

**a)** Zeichne das ER-Diagramm mit Generalisierung.

**b)** Überführe nach Strategie 2 ins relationale Modell.

**c)** Schreibe die SQL-Anweisungen.

**d)** Welche Strategie würdest du wählen, wenn das Krankenhaus häufig **alle Mitarbeiter gemeinsam** (ohne Unterschied Arzt/Pflege) auflisten muss? Begründe.

<details>
<summary>Lösung</summary>

**a)** ER-Diagramm:
```
vorname  nachname  einstellungsdatum
   \         |           /
         [Mitarbeiter]
         mitarbeiter_id (PK)
               |
            (is-a)
           /        \
        [Arzt]    [Pflegepersonal]
          |                |
    fachgebiet          station
    approbations-       schichtmodell
    nummer
```

**b)** Relationales Modell:
```
Mitarbeiter(mitarbeiter_id, vorname, nachname, einstellungsdatum)
Arzt(mitarbeiter_id, fachgebiet, approbationsnummer)
     ^^^^^^^^^^^^^^
     PK und FK→Mitarbeiter
Pflegepersonal(mitarbeiter_id, station, schichtmodell)
               ^^^^^^^^^^^^^^
               PK und FK→Mitarbeiter
```

**c)** SQL:
```sql
CREATE TABLE Mitarbeiter (
    mitarbeiter_id    INTEGER PRIMARY KEY,
    vorname           TEXT NOT NULL,
    nachname          TEXT NOT NULL,
    einstellungsdatum TEXT
);

CREATE TABLE Arzt (
    mitarbeiter_id      INTEGER PRIMARY KEY REFERENCES Mitarbeiter(mitarbeiter_id),
    fachgebiet          TEXT,
    approbationsnummer  TEXT UNIQUE
);

CREATE TABLE Pflegepersonal (
    mitarbeiter_id INTEGER PRIMARY KEY REFERENCES Mitarbeiter(mitarbeiter_id),
    station        TEXT,
    schichtmodell  TEXT
);
```

**d)** Strategie 2 ist trotzdem sinnvoll, weil man alle Mitarbeiter einfach aus der `Mitarbeiter`-Tabelle lesen kann, ohne JOIN:
```sql
SELECT * FROM Mitarbeiter;
```
Strategie 1 (eine Tabelle) wäre ebenfalls möglich, hätte aber viele NULL-Werte.
</details>

---

### Aufgabe 3 – Vergleich der Strategien

Gegeben ist folgendes ER-Diagramm mit Generalisierung:

```
name  preis  kategorie
  \     |      /
     [Produkt]
     produkt_id (PK)
          |
       (is-a)
      /        \
[Getränk]    [Speise]
     |               |
  volumen_ml      kalorien
  alkoholgehalt   allergene (mehrwertig)
```

**a)** Überführe nach **Strategie 1** (eine Tabelle). Hinweis: Das mehrwertige Attribut `allergene` muss trotzdem ausgelagert werden.

**b)** Überführe nach **Strategie 2** (Supertyp + Subtypen).

**c)** Welche Strategie ist hier besser geeignet? Begründe.

<details>
<summary>Lösung</summary>

**a)** Strategie 1:
```
Produkt(produkt_id, name, preis, kategorie, typ,
        volumen_ml, alkoholgehalt,    ← nur für Getränke
        kalorien)                     ← nur für Speisen

Produkt_Allergen(produkt_id, allergen)   ← mehrwertiges Attribut immer auslagern
```

**b)** Strategie 2:
```
Produkt(produkt_id, name, preis, kategorie)
Getraenk(produkt_id, volumen_ml, alkoholgehalt)
         ^^^^^^^^^^
         PK und FK→Produkt
Speise(produkt_id, kalorien)
       ^^^^^^^^^^
       PK und FK→Produkt
Speise_Allergen(produkt_id, allergen)
                ^^^^^^^^^^
                FK→Speise (oder FK→Produkt, je nach Modell)
```

**c)** Strategie 2 ist hier besser, weil Getränke und Speisen sehr unterschiedliche Attribute haben und die `NULL`-Werte bei Strategie 1 unübersichtlich wären. Außerdem lässt sich das mehrwertige Attribut `allergene` sauber an `Speise` hängen.
</details>
