# Kapitel 6: DDL in SQL – Tabellen definieren und verwalten

**Datenbank:** `schule.db` – öffne die Datei direkt mit *DB Browser for SQLite*  
**Thema:** Data Definition Language (DDL) – Tabellen erstellen, ändern und löschen

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md) · [Kapitel 7 – DML in SQL](DML.md) · [Projekt – Wetterdatenbank](Projekt_Wetterdatenbank.md)

---

## 1. Was ist DDL?

SQL ist in verschiedene Teilbereiche unterteilt:

| Bereich | Abkürzung | Befehle | Wozu? |
|---|---|---|---|
| Data Definition Language | **DDL** | `CREATE`, `ALTER`, `DROP` | Tabellenstruktur definieren |
| Data Manipulation Language | **DML** | `INSERT`, `UPDATE`, `DELETE` | Daten einfügen, ändern, löschen |
| Data Query Language | **DQL** | `SELECT` | Daten abfragen |

In den vorherigen Kapiteln habt ihr hauptsächlich **DQL** (Abfragen) verwendet. In diesem Kapitel geht es um **DDL** – das Erstellen und Verwalten von Tabellenstrukturen.

DDL-Befehle verändern das **Schema** der Datenbank, also die Struktur – nicht die Daten selbst.

---

## 2. `CREATE TABLE` – Eine Tabelle erstellen

Mit `CREATE TABLE` wird eine neue Tabelle angelegt. Man gibt den Tabellennamen und alle Spalten mit ihren **Datentypen** und **Constraints** (Einschränkungen) an.

**Grundstruktur:**
```sql
CREATE TABLE tabellenname (
    spalte1  DATENTYP  CONSTRAINT,
    spalte2  DATENTYP  CONSTRAINT,
    ...
);
```

### 2.1 Datentypen in SQLite

SQLite verwendet flexible Datentypen (sogenannte „Type Affinity"):

| Datentyp | Verwendung | Beispiel |
|---|---|---|
| `INTEGER` | Ganze Zahlen | `1`, `42`, `-7` |
| `REAL` | Dezimalzahlen | `3.14`, `9.99` |
| `TEXT` | Zeichenketten | `'Hallo'`, `'Max Mustermann'` |
| `BLOB` | Binärdaten (Dateien, Bilder) | selten direkt verwendet |
| `NUMERIC` | Zahlen (intern flexibel) | |

> **Hinweis:** In anderen Datenbanksystemen (z. B. MySQL, PostgreSQL) gibt es strengere Typen wie `VARCHAR(255)`, `INT`, `FLOAT`, `DATE`, `BOOLEAN`. SQLite ist hier toleranter, aber im Unterricht schreiben wir trotzdem sinnvolle Typen.

### 2.2 Ein einfaches Beispiel

```sql
CREATE TABLE klassen (
    klasse_id   INTEGER PRIMARY KEY,
    bezeichnung TEXT    NOT NULL,
    stufe       INTEGER,
    klassenlehrer TEXT
);
```

> **Teste das:** Öffne DB Browser for SQLite, wähle „Execute SQL" und führe diese Anweisung aus. Du siehst die neue Tabelle im Tab „Database Structure".

---

## 3. Constraints – Einschränkungen

Constraints legen Regeln für die Daten in einer Spalte fest. Sie werden direkt bei `CREATE TABLE` angegeben.

### 3.1 `PRIMARY KEY`

Legt den **Primärschlüssel** fest. Ein Primärschlüssel muss eindeutig und darf nicht `NULL` sein.

```sql
CREATE TABLE schueler (
    schueler_id INTEGER PRIMARY KEY,   -- einfacher Primärschlüssel
    vorname     TEXT,
    nachname    TEXT
);
```

**Zusammengesetzter Primärschlüssel** (z. B. bei schwachen Entitäten): wird als Tabellenconstraint am Ende angegeben:

```sql
CREATE TABLE sitzplatz (
    klasse_id   INTEGER,
    platznummer INTEGER,
    reihe       INTEGER,
    PRIMARY KEY (klasse_id, platznummer)   -- zusammengesetzt
);
```

> In SQLite wirkt `INTEGER PRIMARY KEY` als **Autoinkrement** – die Datenbank vergibt automatisch aufsteigende IDs, wenn kein Wert angegeben wird.

---

### 3.2 `NOT NULL`

Verbietet `NULL`-Werte in dieser Spalte. Der Wert muss immer angegeben werden.

```sql
CREATE TABLE schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,    -- muss immer ausgefüllt sein
    nachname    TEXT NOT NULL,    -- muss immer ausgefüllt sein
    spitzname   TEXT              -- darf NULL sein (optional)
);
```

**Wann `NOT NULL` verwenden?** Immer dann, wenn ein Wert für den Datensatz zwingend benötigt wird.

---

### 3.3 `UNIQUE`

Stellt sicher, dass kein Wert in dieser Spalte **doppelt** vorkommt. Anders als `PRIMARY KEY` erlaubt `UNIQUE` aber `NULL`-Werte (sofern nicht `NOT NULL` kombiniert wird).

```sql
CREATE TABLE lehrer (
    lehrer_id      INTEGER PRIMARY KEY,
    personalnummer TEXT NOT NULL UNIQUE,   -- jede Personalnummer nur einmal
    vorname        TEXT NOT NULL,
    nachname       TEXT NOT NULL,
    email          TEXT UNIQUE             -- eindeutig, aber optional
);
```

---

### 3.4 `DEFAULT`

Legt einen **Standardwert** fest, der eingetragen wird, wenn beim Einfügen kein Wert angegeben wird.

```sql
CREATE TABLE bestellungen (
    bestell_id  INTEGER PRIMARY KEY,
    schueler_id INTEGER NOT NULL,
    datum       TEXT    DEFAULT (date('now')),   -- heute als Standarddatum
    menge       INTEGER DEFAULT 1               -- Standardmenge: 1
);
```

**Nützliche DEFAULT-Werte:**
- `DEFAULT 0` für Zähler, die bei 0 beginnen
- `DEFAULT (date('now'))` für das aktuelle Datum in SQLite
- `DEFAULT 'aktiv'` für einen Standardstatus

---

### 3.5 `CHECK`

Prüft, ob ein Wert eine bestimmte **Bedingung** erfüllt. Wird die Bedingung verletzt, schlägt das Einfügen fehl.

```sql
CREATE TABLE noten (
    noten_id    INTEGER PRIMARY KEY,
    schueler_id INTEGER NOT NULL,
    note        INTEGER NOT NULL CHECK (note >= 1 AND note <= 6),  -- nur Werte 1–6
    art         TEXT    CHECK (art IN ('Klassenarbeit', 'Test', 'mündlich'))
);
```

Weitere Beispiele:
```sql
preis  REAL CHECK (preis >= 0)           -- kein negativer Preis
stufe  INTEGER CHECK (stufe BETWEEN 5 AND 13)
datum  TEXT CHECK (datum > '2000-01-01')
```

---

### 3.6 `REFERENCES` / `FOREIGN KEY` – Fremdschlüssel

Ein **Fremdschlüssel** verweist auf den Primärschlüssel einer anderen Tabelle. Er stellt die **referenzielle Integrität** sicher: Es kann kein Fremdschlüsselwert eingetragen werden, der in der referenzierten Tabelle nicht existiert.

**Kurzform (Spaltenebene) in SQLite:**
```sql
CREATE TABLE schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL,
    klasse_id   INTEGER NOT NULL REFERENCES klassen(klasse_id)
    --                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    --                           Fremdschlüssel auf klassen
);
```

**Langform (Tabellenebene) – Standard SQL:**
```sql
CREATE TABLE schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL,
    klasse_id   INTEGER NOT NULL,
    FOREIGN KEY (klasse_id) REFERENCES klassen(klasse_id)
);
```

> **Wichtig für SQLite:** Fremdschlüsselprüfungen sind in SQLite standardmäßig **deaktiviert**! Um sie zu aktivieren, muss man am Anfang jeder Verbindung ausführen:  
> ```sql
> PRAGMA foreign_keys = ON;
> ```

#### `ON DELETE` und `ON UPDATE`

Was passiert, wenn ein Datensatz gelöscht oder geändert wird, auf den ein Fremdschlüssel zeigt?

```sql
FOREIGN KEY (klasse_id) REFERENCES klassen(klasse_id)
    ON DELETE CASCADE     -- Schüler werden automatisch mitgelöscht
    ON UPDATE CASCADE     -- Fremdschlüssel wird automatisch angepasst
```

| Option | Verhalten |
|---|---|
| `RESTRICT` (Standard) | Löschen/Ändern wird verweigert, wenn noch Verweise existieren |
| `CASCADE` | Abhängige Zeilen werden automatisch mitgelöscht/-geändert |
| `SET NULL` | Fremdschlüssel wird auf `NULL` gesetzt |
| `SET DEFAULT` | Fremdschlüssel wird auf den Standardwert gesetzt |

**Beispiel: Schüler werden automatisch gelöscht, wenn ihre Klasse gelöscht wird:**
```sql
CREATE TABLE schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL,
    klasse_id   INTEGER NOT NULL,
    FOREIGN KEY (klasse_id) REFERENCES klassen(klasse_id) ON DELETE CASCADE
);
```

---

## 4. Vollständiges Beispiel – die Schuldatenbank

```sql
-- Zuerst Tabellen ohne Fremdschlüssel:
CREATE TABLE klassen (
    klasse_id    INTEGER PRIMARY KEY,
    bezeichnung  TEXT    NOT NULL UNIQUE,
    stufe        INTEGER NOT NULL CHECK (stufe BETWEEN 5 AND 13),
    klassenlehrer TEXT
);

CREATE TABLE faecher (
    fach_id  INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL UNIQUE,
    kuerzel  TEXT    NOT NULL UNIQUE
);

-- Dann Tabellen mit Fremdschlüsseln:
CREATE TABLE schueler (
    schueler_id  INTEGER PRIMARY KEY,
    vorname      TEXT    NOT NULL,
    nachname     TEXT    NOT NULL,
    geburtsdatum TEXT,
    geschlecht   TEXT    CHECK (geschlecht IN ('m', 'w', 'd')),
    klasse_id    INTEGER NOT NULL REFERENCES klassen(klasse_id)
);

CREATE TABLE noten (
    noten_id    INTEGER PRIMARY KEY,
    schueler_id INTEGER NOT NULL REFERENCES schueler(schueler_id),
    fach_id     INTEGER NOT NULL REFERENCES faecher(fach_id),
    note        INTEGER NOT NULL CHECK (note >= 1 AND note <= 6),
    datum       TEXT    NOT NULL DEFAULT (date('now')),
    art         TEXT    NOT NULL CHECK (art IN ('Klassenarbeit', 'Test', 'mündlich'))
);

CREATE TABLE produkte (
    produkt_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    kategorie  TEXT,
    preis      REAL NOT NULL CHECK (preis >= 0)
);

CREATE TABLE bestellungen (
    bestell_id  INTEGER PRIMARY KEY,
    schueler_id INTEGER NOT NULL REFERENCES schueler(schueler_id),
    produkt_id  INTEGER NOT NULL REFERENCES produkte(produkt_id),
    datum       TEXT    NOT NULL DEFAULT (date('now')),
    menge       INTEGER NOT NULL DEFAULT 1 CHECK (menge > 0)
);
```

> **Beachte die Reihenfolge:** Tabellen, auf die mit Fremdschlüsseln verwiesen wird, müssen zuerst erstellt werden. `klassen` muss vor `schueler` erstellt werden, weil `schueler` auf `klassen` verweist.

---

## 5. `ALTER TABLE` – Tabellen nachträglich ändern

Mit `ALTER TABLE` kann man eine bestehende Tabelle **nachträglich verändern**, ohne sie neu erstellen zu müssen.

### 5.1 Spalte hinzufügen

```sql
-- Spalte 'email' zur Tabelle schueler hinzufügen:
ALTER TABLE schueler ADD COLUMN email TEXT;

-- Mit Standardwert:
ALTER TABLE schueler ADD COLUMN aktiv INTEGER DEFAULT 1;
```

> **Hinweis:** In SQLite kann man Spalten nur **hinzufügen**, aber nicht umbenennen oder löschen (ohne die Tabelle neu zu erstellen). Andere Datenbanksysteme wie PostgreSQL unterstützen mehr Operationen.

### 5.2 Tabelle umbenennen

```sql
-- Tabelle 'schueler' umbenennen in 'lernende':
ALTER TABLE schueler RENAME TO lernende;
```

### 5.3 Spalte umbenennen (ab SQLite 3.25.0)

```sql
-- Spalte 'klassenlehrer' umbenennen in 'klassenlehrkraft':
ALTER TABLE klassen RENAME COLUMN klassenlehrer TO klassenlehrkraft;
```

---

## 6. `DROP TABLE` – Tabelle löschen

Mit `DROP TABLE` wird eine Tabelle **vollständig gelöscht** – inklusive aller Daten.

```sql
DROP TABLE bestellungen;
```

**Sicher löschen (nur wenn Tabelle existiert):**
```sql
DROP TABLE IF EXISTS bestellungen;
```

> **Achtung:** `DROP TABLE` ist nicht rückgängig zu machen! Die Tabelle und alle Daten sind dauerhaft weg. Wenn andere Tabellen Fremdschlüssel auf diese Tabelle haben, schlägt das Löschen fehl (außer bei `ON DELETE CASCADE`).

**Reihenfolge beim Löschen:** Zuerst abhängige Tabellen löschen, dann die referenzierte Tabelle:
```sql
DROP TABLE IF EXISTS noten;
DROP TABLE IF EXISTS bestellungen;
DROP TABLE IF EXISTS schueler;     -- erst dann klassen löschen
DROP TABLE IF EXISTS klassen;
```

---

## 7. Übungsaufgaben

### Aufgabe 1 – Bibliotheksdatenbank erstellen

Eine Bibliothek möchte ihre Bücher und Ausleihen verwalten. Folgende Entitäten sind bekannt:

- **Buch:** `buch_id` (PK), `titel` (nicht leer), `isbn` (eindeutig), `erscheinungsjahr`, `preis` (nicht negativ)
- **Mitglied:** `mitglied_id` (PK), `vorname` (nicht leer), `nachname` (nicht leer), `email` (eindeutig), `mitglied_seit` (Standardwert: heutiges Datum)
- **Ausleihe:** `ausleihe_id` (PK), `mitglied_id` (FK, verpflichtend), `buch_id` (FK, verpflichtend), `ausleihdatum` (Standardwert: heute), `rueckgabedatum` (optional)

**a)** Schreibe alle `CREATE TABLE`-Anweisungen in der richtigen Reihenfolge.

**b)** Was muss beim Löschen eines Mitglieds passieren, wenn das Mitglied noch Ausleihen hat? Welche `ON DELETE`-Option wäre sinnvoll?

**c)** Füge der Tabelle `Buch` nachträglich eine Spalte `genre` (Text, optional) hinzu.

<details>
<summary>Lösung</summary>

**a)** SQL:
```sql
CREATE TABLE Buch (
    buch_id           INTEGER PRIMARY KEY,
    titel             TEXT    NOT NULL,
    isbn              TEXT    UNIQUE,
    erscheinungsjahr  INTEGER,
    preis             REAL    CHECK (preis >= 0)
);

CREATE TABLE Mitglied (
    mitglied_id   INTEGER PRIMARY KEY,
    vorname       TEXT    NOT NULL,
    nachname      TEXT    NOT NULL,
    email         TEXT    UNIQUE,
    mitglied_seit TEXT    DEFAULT (date('now'))
);

CREATE TABLE Ausleihe (
    ausleihe_id    INTEGER PRIMARY KEY,
    mitglied_id    INTEGER NOT NULL REFERENCES Mitglied(mitglied_id),
    buch_id        INTEGER NOT NULL REFERENCES Buch(buch_id),
    ausleihdatum   TEXT    NOT NULL DEFAULT (date('now')),
    rueckgabedatum TEXT
);
```

**b)** Es sollte verhindert werden, dass ein Mitglied gelöscht wird, das noch Ausleihen hat → `ON DELETE RESTRICT` (Standard).  
Alternativ könnte `ON DELETE CASCADE` sinnvoll sein, wenn die Ausleihehistorie mit gelöscht werden soll.

```sql
-- Mit explizitem RESTRICT:
FOREIGN KEY (mitglied_id) REFERENCES Mitglied(mitglied_id) ON DELETE RESTRICT
```

**c)** SQL:
```sql
ALTER TABLE Buch ADD COLUMN genre TEXT;
```
</details>

---

### Aufgabe 2 – Constraints analysieren

Gegeben ist folgende Tabellendefinition:

```sql
CREATE TABLE veranstaltung (
    veranstaltung_id INTEGER PRIMARY KEY,
    name             TEXT    NOT NULL,
    datum            TEXT    NOT NULL,
    max_teilnehmer   INTEGER DEFAULT 30 CHECK (max_teilnehmer > 0),
    typ              TEXT    CHECK (typ IN ('Kurs', 'Workshop', 'Vortrag')),
    ort              TEXT
);
```

**a)** Welche der folgenden INSERT-Anweisungen funktionieren, welche schlagen fehl? Begründe jeweils.

```sql
-- 1)
INSERT INTO veranstaltung (name, datum) VALUES ('Mathe-AG', '2026-09-01');

-- 2)
INSERT INTO veranstaltung (name, datum, typ) VALUES ('Python-Kurs', '2026-10-15', 'Seminar');

-- 3)
INSERT INTO veranstaltung (name, datum, max_teilnehmer) VALUES ('Chor', '2026-11-20', 0);

-- 4)
INSERT INTO veranstaltung (veranstaltung_id, name, datum, typ)
VALUES (1, 'Theater', '2026-12-01', 'Workshop');
```

**b)** Was ist der Wert von `max_teilnehmer`, wenn man in Anweisung 1 keinen Wert angibt?

<details>
<summary>Lösung</summary>

**a)**

1. **Funktioniert.** `name` und `datum` sind angegeben (`NOT NULL`). `max_teilnehmer` bekommt den Standardwert `30`. `typ` und `ort` sind optional (kein `NOT NULL`), also `NULL`.

2. **Schlägt fehl.** `typ = 'Seminar'` verletzt den CHECK-Constraint `typ IN ('Kurs', 'Workshop', 'Vortrag')`. Nur diese drei Werte sind erlaubt.

3. **Schlägt fehl.** `max_teilnehmer = 0` verletzt den CHECK-Constraint `max_teilnehmer > 0`.

4. **Funktioniert** (sofern noch keine Zeile mit `veranstaltung_id = 1` existiert). Alle Constraints sind erfüllt.

**b)** `max_teilnehmer` bekommt den Wert `30` (durch `DEFAULT 30`).
</details>

---

### Aufgabe 3 – Sportvereindatenbank

Ein Sportverein möchte seine **Mitglieder**, **Mannschaften** und **Spiele** verwalten.

Anforderungen:
- Jedes Mitglied hat: `mitglied_id` (PK), `name` (Pflicht), `geburtsdatum`, `beitrag_monatlich` (positiv, Standard: 15.00)
- Jede Mannschaft hat: `mannschaft_id` (PK), `name` (Pflicht, eindeutig), `sportart`, `trainer_id` (FK auf Mitglied, optional – nicht jede Mannschaft hat einen eingetragenen Trainer)
- Jedes Spiel hat: `spiel_id` (PK), `heimmannschaft_id` (FK, Pflicht), `gastmannschaft_id` (FK, Pflicht), `datum` (Pflicht), `tore_heim` (Standard: 0), `tore_gast` (Standard: 0)

**a)** Schreibe alle `CREATE TABLE`-Anweisungen.

**b)** Warum ist `trainer_id` in `Mannschaft` ein optionaler Fremdschlüssel?

**c)** Schreibe eine `ALTER TABLE`-Anweisung, die der Tabelle `Spiel` eine Spalte `schiedsrichter` (Text, optional) hinzufügt.

**d)** In welcher Reihenfolge müssen die Tabellen gelöscht werden?

<details>
<summary>Lösung</summary>

**a)** SQL:
```sql
CREATE TABLE Mitglied (
    mitglied_id        INTEGER PRIMARY KEY,
    name               TEXT    NOT NULL,
    geburtsdatum       TEXT,
    beitrag_monatlich  REAL    NOT NULL DEFAULT 15.00 CHECK (beitrag_monatlich > 0)
);

CREATE TABLE Mannschaft (
    mannschaft_id INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL UNIQUE,
    sportart      TEXT,
    trainer_id    INTEGER REFERENCES Mitglied(mitglied_id)   -- optional: kein NOT NULL
);

CREATE TABLE Spiel (
    spiel_id           INTEGER PRIMARY KEY,
    heimmannschaft_id  INTEGER NOT NULL REFERENCES Mannschaft(mannschaft_id),
    gastmannschaft_id  INTEGER NOT NULL REFERENCES Mannschaft(mannschaft_id),
    datum              TEXT    NOT NULL,
    tore_heim          INTEGER NOT NULL DEFAULT 0,
    tore_gast          INTEGER NOT NULL DEFAULT 0
);
```

**b)** `trainer_id` ist optional, weil nicht jede Mannschaft einen eingetragenen Trainer hat. Der Fremdschlüssel darf `NULL` sein → kein `NOT NULL`-Constraint.

**c)** SQL:
```sql
ALTER TABLE Spiel ADD COLUMN schiedsrichter TEXT;
```

**d)** Reihenfolge (abhängige Tabellen zuerst):
```sql
DROP TABLE IF EXISTS Spiel;
DROP TABLE IF EXISTS Mannschaft;
DROP TABLE IF EXISTS Mitglied;
```
</details>

---

### Aufgabe 4 – Fehler finden

Die folgende SQL-Anweisung enthält **drei Fehler**. Finde und korrigiere sie.

```sql
CREATE TABLE kurs (
    kurs_id    INT PRIMARY KEY,
    titel      TEXT,
    max_plätze INTEGER DEFAULT CHECK (max_plätze > 0),
    leiter_id  INTEGER NOT NULL,
    preis      REAL DEFAULT -1,
    FOREIGN KEY leiter_id REFERENCES lehrer(lehrer_id)
);
```

<details>
<summary>Lösung</summary>

**Fehler 1:** `DEFAULT CHECK` ist falsch. `DEFAULT` braucht einen Wert, `CHECK` ist ein eigenes Constraint. Korrekt:
```sql
max_plätze INTEGER DEFAULT 20 CHECK (max_plätze > 0),
```

**Fehler 2:** `DEFAULT -1` bei `preis` verletzt logisch den Sinn (negativer Preis). Besser mit CHECK:
```sql
preis REAL DEFAULT 0.00 CHECK (preis >= 0),
```

**Fehler 3:** `FOREIGN KEY leiter_id` fehlt die Klammerung. Korrekt:
```sql
FOREIGN KEY (leiter_id) REFERENCES lehrer(lehrer_id)
```

**Korrigierte Anweisung:**
```sql
CREATE TABLE kurs (
    kurs_id    INTEGER PRIMARY KEY,
    titel      TEXT,
    max_plätze INTEGER DEFAULT 20 CHECK (max_plätze > 0),
    leiter_id  INTEGER NOT NULL,
    preis      REAL DEFAULT 0.00 CHECK (preis >= 0),
    FOREIGN KEY (leiter_id) REFERENCES lehrer(lehrer_id)
);
```
</details>
