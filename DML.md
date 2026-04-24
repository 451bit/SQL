# Kapitel 7: DML in SQL – Daten einfügen, ändern und löschen

**Datenbank:** `schule.db` – öffne die Datei direkt mit *DB Browser for SQLite*  
**Thema:** Data Manipulation Language (DML) – `INSERT`, `UPDATE`, `DELETE`

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md) · [Kapitel 7 – DML in SQL](DML.md) · [Projekt – Wetterdatenbank](Projekt_Wetterdatenbank.md)

---

## 1. Was ist DML?

Nachdem in Kapitel 6 die **Struktur** von Tabellen mit DDL definiert wurde, geht es jetzt um die **Daten** selbst. DML-Befehle fügen Daten ein, ändern sie oder löschen sie.

| Befehl | Bedeutung |
|---|---|
| `INSERT` | Neue Zeile(n) in eine Tabelle einfügen |
| `UPDATE` | Bestehende Zeilen verändern |
| `DELETE` | Bestehende Zeilen löschen |

> **Wichtig:** DML-Befehle verändern **Daten** – nicht die Tabellenstruktur. Die Struktur wird mit DDL (`CREATE TABLE`, `ALTER TABLE`, …) festgelegt.

---

## 2. `INSERT` – Daten einfügen

### 2.1 Grundform

Mit `INSERT INTO` fügt man eine neue Zeile in eine Tabelle ein. Man gibt an, in welche Spalten Werte eingetragen werden sollen, und dann die zugehörigen Werte:

```sql
INSERT INTO tabellenname (spalte1, spalte2, spalte3)
VALUES (wert1, wert2, wert3);
```

**Beispiel:** Eine neue Klasse einfügen:

```sql
INSERT INTO klassen (klasse_id, bezeichnung, stufe, klassenlehrer)
VALUES (5, '10c', 10, 'Frau Hoffmann');
```

> **Teste das:** Führe die Anweisung in DB Browser aus. Wechsle dann zum Tab „Browse Data" und wähle die Tabelle `klassen` – du siehst den neuen Eintrag.

### 2.2 Spalten weglassen

Man muss nicht alle Spalten angeben. Spalten mit `DEFAULT`-Wert oder ohne `NOT NULL` können weggelassen werden – sie erhalten dann ihren Standardwert bzw. `NULL`.

```sql
-- Nur Pflichtfelder angeben:
INSERT INTO klassen (bezeichnung, stufe)
VALUES ('11a', 11);
-- klasse_id bekommt automatisch eine ID (Autoinkrement), klassenlehrer bleibt NULL
```

**Kurzform ohne Spaltenliste** – dann müssen die Werte in der Reihenfolge der Tabellendefinition stehen:

```sql
INSERT INTO klassen VALUES (6, '11b', 11, 'Herr Braun');
```

> Die Kurzform ohne Spaltenliste ist **fehleranfällig** – wenn sich die Tabellenstruktur ändert, bricht die Anweisung. Bevorzuge immer die explizite Spaltenliste.

### 2.3 Mehrere Zeilen gleichzeitig einfügen

```sql
INSERT INTO faecher (fach_id, name, kuerzel)
VALUES
    (1, 'Mathematik', 'M'),
    (2, 'Deutsch', 'D'),
    (3, 'Englisch', 'E'),
    (4, 'Informatik', 'Inf');
```

### 2.4 Reihenfolge beim Einfügen – Fremdschlüssel beachten

Wenn Tabellen Fremdschlüssel aufeinander haben, muss man in der richtigen Reihenfolge einfügen: **zuerst die referenzierte Tabelle, dann die abhängige**.

```sql
-- Richtige Reihenfolge:
INSERT INTO klassen (klasse_id, bezeichnung, stufe) VALUES (1, '9a', 9);
INSERT INTO schueler (schueler_id, vorname, nachname, klasse_id)
VALUES (1, 'Leon', 'Bauer', 1);  -- klasse_id 1 muss bereits existieren

-- Falsche Reihenfolge (schlägt fehl, wenn FK-Prüfung aktiv ist):
INSERT INTO schueler (schueler_id, vorname, nachname, klasse_id)
VALUES (2, 'Emma', 'Schneider', 99);  -- Klasse 99 existiert nicht!
```

### 2.5 `INSERT OR IGNORE` und `INSERT OR REPLACE`

Manchmal möchte man verhindern, dass ein Fehler entsteht, wenn ein Primärschlüssel bereits existiert:

```sql
-- Einfügen, aber Fehler ignorieren wenn PK schon vorhanden:
INSERT OR IGNORE INTO klassen (klasse_id, bezeichnung, stufe)
VALUES (1, '9a', 9);

-- Einfügen und bestehende Zeile überschreiben:
INSERT OR REPLACE INTO klassen (klasse_id, bezeichnung, stufe)
VALUES (1, '9a_neu', 9);
```

---

## 3. `UPDATE` – Daten ändern

### 3.1 Grundform

Mit `UPDATE` werden **bestehende Zeilen** verändert. Die `WHERE`-Klausel legt fest, welche Zeilen betroffen sind:

```sql
UPDATE tabellenname
SET spalte1 = neuer_wert1,
    spalte2 = neuer_wert2
WHERE bedingung;
```

**Beispiel:** Den Klassenlehrer der Klasse mit `klasse_id = 1` ändern:

```sql
UPDATE klassen
SET klassenlehrer = 'Herr Müller'
WHERE klasse_id = 1;
```

### 3.2 Mehrere Spalten gleichzeitig ändern

```sql
UPDATE schueler
SET vorname = 'Alexander',
    nachname = 'Bauer'
WHERE schueler_id = 1;
```

### 3.3 `WHERE` – die wichtigste Klausel bei UPDATE

> **Gefahr:** Ein `UPDATE` **ohne** `WHERE` ändert **alle** Zeilen der Tabelle!

```sql
-- Ändert NUR den Schüler mit ID 5:
UPDATE schueler SET klasse_id = 2 WHERE schueler_id = 5;

-- Ändert ALLE Schüler – wahrscheinlich unbeabsichtigt:
UPDATE schueler SET klasse_id = 2;
```

### 3.4 Berechnung im SET

Der neue Wert kann auch aus dem alten Wert berechnet werden:

```sql
-- Alle Preise um 10% erhöhen:
UPDATE produkte
SET preis = preis * 1.10;

-- Menge in einer Bestellung um 1 erhöhen:
UPDATE bestellungen
SET menge = menge + 1
WHERE bestell_id = 42;
```

### 3.5 UPDATE mit Subquery

Man kann den neuen Wert auch aus einer Unterabfrage berechnen – oder die `WHERE`-Bedingung mit einer Subquery formulieren:

```sql
-- Klasse aller Schüler aus der 9a auf die 10a umstellen
-- (wenn man nur die Bezeichnung, nicht die ID kennt):
UPDATE schueler
SET klasse_id = (SELECT klasse_id FROM klassen WHERE bezeichnung = '10a')
WHERE klasse_id = (SELECT klasse_id FROM klassen WHERE bezeichnung = '9a');
```

---

## 4. `DELETE` – Daten löschen

### 4.1 Grundform

Mit `DELETE FROM` werden **Zeilen** aus einer Tabelle entfernt. Die `WHERE`-Klausel legt fest, welche Zeilen gelöscht werden:

```sql
DELETE FROM tabellenname
WHERE bedingung;
```

**Beispiel:** Einen Schüler löschen:

```sql
DELETE FROM schueler
WHERE schueler_id = 7;
```

### 4.2 Mehrere Zeilen löschen

Alle Zeilen, die die Bedingung erfüllen, werden gelöscht:

```sql
-- Alle Bestellungen eines bestimmten Schülers löschen:
DELETE FROM bestellungen
WHERE schueler_id = 3;

-- Alle Noten schlechter als 5 löschen:
DELETE FROM noten
WHERE note > 4;
```

### 4.3 `WHERE` – die wichtigste Klausel bei DELETE

> **Gefahr:** Ein `DELETE` **ohne** `WHERE` löscht **alle** Zeilen der Tabelle – die Tabellenstruktur bleibt, aber alle Daten sind weg!

```sql
-- Löscht NUR Schüler mit ID 5:
DELETE FROM schueler WHERE schueler_id = 5;

-- Löscht ALLE Schüler – sehr gefährlich!
DELETE FROM schueler;
```

> Der Unterschied zu `DROP TABLE`: `DROP TABLE` löscht die **Tabelle selbst** (Struktur + Daten). `DELETE FROM` ohne `WHERE` löscht nur die **Daten**, die Tabelle bleibt leer erhalten.

### 4.4 Reihenfolge beim Löschen – Fremdschlüssel beachten

Wenn Tabellen über Fremdschlüssel verbunden sind, muss man in der richtigen Reihenfolge löschen: **zuerst abhängige Tabellen, dann die referenzierte Tabelle**.

```sql
-- Richtige Reihenfolge:
DELETE FROM noten WHERE schueler_id = 1;        -- erst Noten löschen
DELETE FROM bestellungen WHERE schueler_id = 1; -- dann Bestellungen
DELETE FROM schueler WHERE schueler_id = 1;     -- dann den Schüler

-- Falsche Reihenfolge (schlägt fehl, wenn FK-Prüfung aktiv ist):
DELETE FROM schueler WHERE schueler_id = 1;
-- → Fehler: Es existieren noch Noten/Bestellungen, die auf diesen Schüler zeigen
```

### 4.5 DELETE mit Subquery

Auch beim Löschen kann man Subqueries einsetzen:

```sql
-- Alle Noten des Schülers 'Leon Bauer' löschen:
DELETE FROM noten
WHERE schueler_id = (
    SELECT schueler_id FROM schueler
    WHERE vorname = 'Leon' AND nachname = 'Bauer'
);
```

---

## 5. Zusammenfassung: INSERT, UPDATE, DELETE im Vergleich

| | `INSERT` | `UPDATE` | `DELETE` |
|---|---|---|---|
| Zweck | Neue Zeile einfügen | Bestehende Zeile ändern | Zeile löschen |
| `WHERE` nötig? | Nein | **Ja – sonst alle!** | **Ja – sonst alle!** |
| Fremdschlüssel | Erst referenzierte Tabelle befüllen | FK-Werte müssen existieren | Erst abhängige Tabellen leeren |
| Rückgängig? | Nur mit Transaction | Nur mit Transaction | Nur mit Transaction |

> **Transaktionen** (kurz: `BEGIN` / `COMMIT` / `ROLLBACK`) ermöglichen es, mehrere DML-Befehle als eine atomare Einheit auszuführen und bei Fehlern alles rückgängig zu machen. Das ist ein eigenes Thema, aber wichtig zu wissen.

---

## 6. Übungsaufgaben

### Aufgabe 1 – Daten einfügen

Gegeben ist folgendes Schema:

```sql
CREATE TABLE abteilung (
    abteilung_id INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    standort     TEXT
);

CREATE TABLE mitarbeiter (
    mitarbeiter_id INTEGER PRIMARY KEY,
    vorname        TEXT NOT NULL,
    nachname       TEXT NOT NULL,
    gehalt         REAL NOT NULL DEFAULT 2500.00,
    abteilung_id   INTEGER NOT NULL REFERENCES abteilung(abteilung_id)
);
```

**a)** Füge drei Abteilungen ein: `(1, 'Entwicklung', 'Berlin')`, `(2, 'Marketing', 'Hamburg')`, `(3, 'Vertrieb', NULL)`.

**b)** Füge zwei Mitarbeiter ein:  
- Anna Meier, Gehalt 3200, Abteilung Entwicklung  
- Tom Fischer, Gehalt wird nicht angegeben (Standardwert), Abteilung Marketing

**c)** Was passiert, wenn du versuchst, einen Mitarbeiter in die Abteilung mit `abteilung_id = 99` einzufügen? Begründe.

<details>
<summary>Lösung</summary>

**a)**
```sql
INSERT INTO abteilung (abteilung_id, name, standort)
VALUES
    (1, 'Entwicklung', 'Berlin'),
    (2, 'Marketing', 'Hamburg'),
    (3, 'Vertrieb', NULL);
```

**b)**
```sql
INSERT INTO mitarbeiter (mitarbeiter_id, vorname, nachname, gehalt, abteilung_id)
VALUES (1, 'Anna', 'Meier', 3200.00, 1);

INSERT INTO mitarbeiter (mitarbeiter_id, vorname, nachname, abteilung_id)
VALUES (2, 'Tom', 'Fischer', 2);
-- gehalt wird nicht angegeben → Standardwert 2500.00
```

**c)** Die Datenbank verweigert den Eintrag mit einem Fremdschlüsselfehler, weil keine Abteilung mit `abteilung_id = 99` existiert. Die referenzielle Integrität ist verletzt.
</details>

---

### Aufgabe 2 – Daten ändern

Gegeben sind folgende Tabellen (aus Aufgabe 1 befüllt):

**a)** Ändere den Standort der Abteilung `Vertrieb` auf `'München'`.

**b)** Erhöhe das Gehalt aller Mitarbeiter in der Abteilung `Entwicklung` um 5%.

**c)** Jemand tippt versehentlich `UPDATE mitarbeiter SET gehalt = 0;` ohne `WHERE`. Was passiert? Wie könnte man das verhindern?

**d)** Schreibe ein `UPDATE` mit Subquery: Erhöhe das Gehalt aller Mitarbeiter der Abteilung `'Marketing'` um 200 € – du kennst aber nur den Namen der Abteilung, nicht die ID.

<details>
<summary>Lösung</summary>

**a)**
```sql
UPDATE abteilung
SET standort = 'München'
WHERE name = 'Vertrieb';
```

**b)**
```sql
UPDATE mitarbeiter
SET gehalt = gehalt * 1.05
WHERE abteilung_id = 1;
```

**c)** Das Gehalt **aller** Mitarbeiter wird auf 0 gesetzt – alle Zeilen sind betroffen, weil keine `WHERE`-Bedingung vorhanden ist. Verhindern könnte man das durch: Transaktionen (`BEGIN` + `ROLLBACK`), Zugriffsrechte, oder in manchen Datenbanksystemen durch einen „safe update mode".

**d)**
```sql
UPDATE mitarbeiter
SET gehalt = gehalt + 200
WHERE abteilung_id = (
    SELECT abteilung_id FROM abteilung WHERE name = 'Marketing'
);
```
</details>

---

### Aufgabe 3 – Daten löschen

**a)** Lösche die Abteilung `Vertrieb`. Was muss vorher sichergestellt sein?

**b)** Lösche alle Mitarbeiter, deren Gehalt unter 2600 € liegt.

**c)** Lösche den Mitarbeiter `Anna Meier` vollständig – du kennst nur ihren Namen, nicht ihre ID. Verwende eine Subquery.

**d)** Erkläre den Unterschied zwischen `DELETE FROM mitarbeiter;` und `DROP TABLE mitarbeiter;`.

<details>
<summary>Lösung</summary>

**a)**
```sql
-- Erst sicherstellen, dass keine Mitarbeiter in der Abteilung sind
-- (oder diese vorher in eine andere Abteilung verschieben):
UPDATE mitarbeiter SET abteilung_id = 1 WHERE abteilung_id = 3;

-- Dann die Abteilung löschen:
DELETE FROM abteilung WHERE name = 'Vertrieb';
```
Wenn noch Mitarbeiter auf diese Abteilung zeigen, schlägt das Löschen fehl (FK-Constraint).

**b)**
```sql
DELETE FROM mitarbeiter
WHERE gehalt < 2600;
```

**c)**
```sql
DELETE FROM mitarbeiter
WHERE mitarbeiter_id = (
    SELECT mitarbeiter_id FROM mitarbeiter
    WHERE vorname = 'Anna' AND nachname = 'Meier'
);
```

**d)**
- `DELETE FROM mitarbeiter;` löscht **alle Zeilen** – die Tabelle bleibt aber als leere Struktur erhalten. Neue Daten können danach wieder eingefügt werden.
- `DROP TABLE mitarbeiter;` löscht die **Tabelle vollständig** – Struktur und Daten sind weg. Die Tabelle muss mit `CREATE TABLE` neu angelegt werden.
</details>

---

### Aufgabe 4 – Gemischte Aufgabe: Schulverwaltung

Gegeben ist die Schuldatenbank mit den Tabellen `klassen`, `schueler`, `faecher`, `noten` (wie in Kapitel 6 definiert).

**a)** Füge eine neue Klasse `'10d'` (Stufe 10, Klassenlehrkraft `'Herr Wagner'`) ein.

**b)** Wechsle alle Schüler der Klasse `'9a'` in die Klasse `'10a'` (du kennst nur die Bezeichnungen, nicht die IDs).

**c)** Lösche alle Noten der Art `'Test'` aus dem Fach `'Sport'` (du kennst nur die Namen, nicht die IDs). Verwende Subqueries.

**d)** Ein Schüler hat die Schule verlassen. Schreibe die Anweisungen, um den Schüler mit `schueler_id = 15` vollständig zu entfernen. Beachte die richtige Reihenfolge.

<details>
<summary>Lösung</summary>

**a)**
```sql
INSERT INTO klassen (bezeichnung, stufe, klassenlehrer)
VALUES ('10d', 10, 'Herr Wagner');
```

**b)**
```sql
UPDATE schueler
SET klasse_id = (SELECT klasse_id FROM klassen WHERE bezeichnung = '10a')
WHERE klasse_id = (SELECT klasse_id FROM klassen WHERE bezeichnung = '9a');
```

**c)**
```sql
DELETE FROM noten
WHERE art = 'Test'
  AND fach_id = (SELECT fach_id FROM faecher WHERE name = 'Sport');
```

**d)**
```sql
-- Erst abhängige Datensätze löschen:
DELETE FROM noten        WHERE schueler_id = 15;
DELETE FROM bestellungen WHERE schueler_id = 15;

-- Dann den Schüler selbst löschen:
DELETE FROM schueler WHERE schueler_id = 15;
```
</details>

---

### Aufgabe 5 – Fehler finden

Die folgenden SQL-Anweisungen enthalten jeweils einen Fehler. Finde und korrigiere ihn.

```sql
-- 1)
UPDATE produkte
SET preis = preis * 0.9;
WHERE kategorie = 'Snack';

-- 2)
INSERT INTO noten (schueler_id, fach_id, note, art)
VALUES (1, 1, 7, 'Klassenarbeit');

-- 3)
DELETE klassen WHERE klasse_id = 3;

-- 4)
INSERT INTO schueler (schueler_id, vorname, nachname)
VALUES (1, 'Max', 'Mustermann');
```

<details>
<summary>Lösung</summary>

**1)** Das Semikolon steht **vor** der `WHERE`-Klausel – dadurch wird die `WHERE`-Bedingung ignoriert und alle Preise werden geändert. Korrekt:
```sql
UPDATE produkte
SET preis = preis * 0.9
WHERE kategorie = 'Snack';
```

**2)** `note = 7` verletzt den CHECK-Constraint `note >= 1 AND note <= 6`. Korrekt wäre ein Wert zwischen 1 und 6:
```sql
INSERT INTO noten (schueler_id, fach_id, note, art)
VALUES (1, 1, 5, 'Klassenarbeit');
```

**3)** Das `FROM` fehlt. Korrekt:
```sql
DELETE FROM klassen WHERE klasse_id = 3;
```

**4)** `klasse_id` ist `NOT NULL` und hat keinen Standardwert – sie muss angegeben werden. Korrekt:
```sql
INSERT INTO schueler (schueler_id, vorname, nachname, klasse_id)
VALUES (1, 'Max', 'Mustermann', 1);
```
</details>
