# SQL-Arbeitsblatt: Aggregatfunktionen

**Datenbank:** `schule.db` – öffne die Datei direkt mit *DB Browser for SQLite*  
**Thema:** Aggregatfunktionen und `GROUP BY`

---

## Die Ausgangssituation

Unsere Schuldatenbank enthält folgende Tabellen:

| Tabelle | Inhalt |
|---|---|
| `klassen` | Klassen (9a, 9b, 10a, 10b) mit Klassenlehrer |
| `schueler` | 20 Schülerinnen und Schüler mit Klasse |
| `faecher` | Fächer (Mathe, Deutsch, Englisch, Informatik, Sport) |
| `noten` | Einzelne Noten (Klassenarbeit, Test, mündlich) |
| `produkte` | Kantinenangebot mit Preis und Kategorie |
| `bestellungen` | Jede Bestellung eines Schülers in der Kantine |

```
schueler(schueler_id, vorname, nachname, klasse_id, geburtsdatum, geschlecht)
noten(noten_id, schueler_id, fach_id, note, datum, art)
bestellungen(bestell_id, schueler_id, produkt_id, datum, menge)
produkte(produkt_id, name, kategorie, preis)
klassen(klasse_id, bezeichnung, stufe, klassenlehrer)
faecher(fach_id, name, kuerzel)
```

---

## 1. Das Problem – Was ohne Aggregation nicht geht

Du willst wissen: **"Wie viel hat jeder Schüler insgesamt in der Kantine ausgegeben?"**

Dein erster Versuch:

```sql
SELECT schueler_id, preis
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id;
```

**Was passiert?** Du bekommst für jeden Schüler *eine Zeile pro Bestellung* – also mehrere Zeilen pro Schüler, jede mit einem einzelnen Preis. Eine Gesamtsumme gibt es nicht.

```
schueler_id | preis
------------|------
1           | 3.50
1           | 1.20
1           | 4.20
...
```

Eine normale `SELECT`-Abfrage zeigt dir *Einzelwerte*. Um zusammenzurechnen, zu zählen oder den Durchschnitt zu bilden, brauchst du **Aggregatfunktionen**.

---

## 2. `COUNT` – Wie viele?

`COUNT(*)` zählt alle Zeilen eines Ergebnisses.

```sql
SELECT COUNT(*) AS anzahl_schueler
FROM schueler;
```

Du kannst `COUNT` auch mit `WHERE` kombinieren:

```sql
SELECT COUNT(*) AS anzahl_bestellungen
FROM bestellungen
WHERE schueler_id = 1;
```

### Aufgabe 1

Wie viele Schülerinnen (Geschlecht = `'w'`) sind in der Datenbank gespeichert?

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT COUNT(*) AS anzahl_schülerinnen
FROM schueler
WHERE geschlecht = 'w';
```
</details>

---

## 3. `SUM` – Wie viel insgesamt?

`SUM(spalte)` addiert alle Werte einer Spalte. Die Spalte `menge` in `bestellungen` gibt an, wie oft ein Produkt pro Bestellung gekauft wurde.

```sql
SELECT SUM(produkte.preis * bestellungen.menge) AS gesamtausgabe
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
WHERE bestellungen.schueler_id = 1;
```

### Aufgabe 2

Berechne den Gesamtumsatz der Kantine über **alle** Bestellungen.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT ROUND(SUM(produkte.preis * bestellungen.menge), 2) AS gesamtumsatz
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id;
```
</details>

---

## 4. `AVG` – Was ist der Durchschnitt?

`AVG(spalte)` berechnet den Mittelwert aller Werte in einer Spalte.

```sql
SELECT AVG(note) AS durchschnittsnote
FROM noten
WHERE schueler_id = 1;
```

> **Tipp:** Mit `ROUND(AVG(...), 2)` rundet man das Ergebnis auf 2 Nachkommastellen.

### Aufgabe 3

Berechne den Notendurchschnitt von Sophie Wagner (`schueler_id = 2`) **nur im Fach Mathematik** (`fach_id = 1`).

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT AVG(note) AS durchschnitt
FROM noten
WHERE schueler_id = 2
  AND fach_id = 1;
```
</details>

---

## 5. `MIN` und `MAX` – Extremwerte

`MIN(spalte)` liefert den kleinsten, `MAX(spalte)` den größten Wert.

```sql
SELECT MIN(preis) AS guenstigstes,
       MAX(preis) AS teuerstes
FROM produkte;
```

### Aufgabe 4

Welche beste und welche schlechteste Note wurde in der gesamten `noten`-Tabelle vergeben?  
*(In Deutschland ist 1 die beste Note.)*

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT MIN(note) AS beste_note,
       MAX(note) AS schlechteste_note
FROM noten;
```
</details>

---

## 6. `GROUP BY` – Für jede Gruppe ein Ergebnis

Bisher haben alle Aggregatfunktionen **einen einzigen Wert** für die gesamte Tabelle geliefert. Mit `GROUP BY` teilst du die Daten in **Gruppen** auf und bekommst für jede Gruppe ein eigenes Ergebnis.

**Syntax:**
```sql
SELECT gruppierungsspalte, AGGREGATFUNKTION(spalte)
FROM tabelle
GROUP BY gruppierungsspalte;
```

> **Regel:** Alle Spalten im `SELECT`, die *keine* Aggregatfunktion sind, **müssen** auch in `GROUP BY` stehen.

**Beispiel:** Gesamtausgabe jedes Schülers in der Kantine:

```sql
SELECT schueler_id,
       ROUND(SUM(produkte.preis * bestellungen.menge), 2) AS gesamtausgabe
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
GROUP BY bestellungen.schueler_id;
```

Jetzt bekommt jeder Schüler **eine eigene Zeile** mit seiner persönlichen Gesamtsumme.

### Aufgabe 5

Zeige für jede Klasse die Anzahl der Schüler. Nutze die Tabelle `schueler` und gruppiere nach `klasse_id`.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT klasse_id, COUNT(*) AS anzahl_schueler
FROM schueler
GROUP BY klasse_id;
```
</details>

---

## 7. `GROUP BY` mit `JOIN` – Lesbare Ausgabe

Statt einer ID kann man mit einem `JOIN` den echten Namen anzeigen.

```sql
SELECT faecher.name AS fach,
       ROUND(AVG(note), 2) AS durchschnitt
FROM noten
JOIN faecher ON noten.fach_id = faecher.fach_id
GROUP BY noten.fach_id;
```

### Aufgabe 6

Zeige für jede Klasse den **Klassennamen** (aus der Tabelle `klassen`) und die Anzahl der Schüler.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT klassen.bezeichnung, COUNT(*) AS anzahl_schueler
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id
GROUP BY schueler.klasse_id;
```
</details>

---

## 8. `HAVING` – Gruppen filtern

`WHERE` filtert **Zeilen** *vor* der Aggregation.  
`HAVING` filtert **Gruppen** *nach* der Aggregation.

> `WHERE` arbeitet mit Einzelwerten – `HAVING` mit Aggregatwerten.

```sql
SELECT faecher.name,
       ROUND(AVG(note), 2) AS durchschnitt
FROM noten
JOIN faecher ON noten.fach_id = faecher.fach_id
GROUP BY noten.fach_id
HAVING AVG(note) > 2.5;
```

Dieses Beispiel zeigt nur Fächer, deren Notendurchschnitt schlechter als 2,5 ist.

> **Wichtig:** Im `HAVING` muss die Aggregatfunktion wiederholt werden – Alias-Namen aus dem `SELECT` funktionieren dort nicht, weil `HAVING` vor `SELECT` ausgewertet wird.

### Aufgabe 7

Zeige alle Schüler, die **mehr als 5 Bestellungen** in der Kantine aufgegeben haben.  
Gib Vorname, Nachname und Anzahl der Bestellungen aus, sortiert nach Anzahl absteigend.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT schueler.vorname || ' ' || schueler.nachname AS name,
       COUNT(*) AS anzahl
FROM bestellungen
JOIN schueler ON bestellungen.schueler_id = schueler.schueler_id
GROUP BY bestellungen.schueler_id
HAVING COUNT(*) > 5
ORDER BY anzahl DESC;
```
</details>

---

## 9. Kombinations-Aufgaben

### Aufgabe 8

Zeige für jede **Produktkategorie** den Gesamtumsatz und die Anzahl der Bestellungen.  
Sortiere nach Umsatz absteigend.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT kategorie,
       COUNT(*) AS bestellungen,
       ROUND(SUM(preis * menge), 2) AS umsatz
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
GROUP BY kategorie
ORDER BY umsatz DESC;
```
</details>

---

### Aufgabe 9

Welche **drei Produkte** wurden insgesamt am häufigsten bestellt?  
Zeige Produktname und Gesamtmenge, nur die Top 3.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT produkte.name,
       SUM(bestellungen.menge) AS gesamtmenge
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
GROUP BY bestellungen.produkt_id
ORDER BY gesamtmenge DESC
LIMIT 3;
```
</details>

---

### Aufgabe 10

Zeige für jeden Schüler (Vorname, Nachname) seinen **Notendurchschnitt in jedem Fach** (Fachname).  
Sortiere nach Nachname, dann nach Fach.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT schueler.vorname,
       schueler.nachname,
       faecher.name AS fach,
       ROUND(AVG(noten.note), 2) AS durchschnitt
FROM noten
JOIN schueler ON noten.schueler_id = schueler.schueler_id
JOIN faecher  ON noten.fach_id     = faecher.fach_id
GROUP BY noten.schueler_id, noten.fach_id
ORDER BY schueler.nachname, faecher.name;
```
</details>

---

### Aufgabe 11

Zeige für jede Klasse (Klassenname) den Notendurchschnitt **aller Schüler dieser Klasse**.  
Zeige nur Klassen, deren Durchschnitt besser als 2,8 ist (also kleiner als 2,8).

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT klassen.bezeichnung,
       ROUND(AVG(noten.note), 2) AS klassendurchschnitt
FROM noten
JOIN schueler ON noten.schueler_id = schueler.schueler_id
JOIN klassen  ON schueler.klasse_id = klassen.klasse_id
GROUP BY klassen.klasse_id
HAVING AVG(noten.note) < 2.8;
```
</details>

---

## 10. Zum Grübeln

### Aufgabe 12

Welche Produkte kosten **mehr als der Durchschnittspreis** aller Produkte?  
Gib Name und Preis aus.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT name, preis
FROM produkte
WHERE preis > (SELECT AVG(preis) FROM produkte);
```
</details>

---

### Aufgabe 13

Welche Schülerinnen und Schüler haben einen **besseren Notendurchschnitt als der Gesamtdurchschnitt** aller Noten in der Datenbank?  
Gib Vorname, Nachname und den persönlichen Durchschnitt aus.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT schueler.vorname,
       schueler.nachname,
       ROUND(AVG(noten.note), 2) AS durchschnitt
FROM noten
JOIN schueler ON noten.schueler_id = schueler.schueler_id
GROUP BY noten.schueler_id
HAVING AVG(noten.note) < (SELECT AVG(note) FROM noten);
```
</details>

---

### Aufgabe 14

Welcher Schüler hat in der Kantine **am meisten Geld ausgegeben**?  
Gib nur genau diesen einen Schüler mit seinem Namen und der Gesamtsumme aus.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT schueler.vorname || ' ' || schueler.nachname AS name,
       ROUND(SUM(produkte.preis * bestellungen.menge), 2) AS gesamtausgabe
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
JOIN schueler ON bestellungen.schueler_id = schueler.schueler_id
GROUP BY bestellungen.schueler_id
HAVING gesamtausgabe = (
    SELECT MAX(summe) FROM (
        SELECT SUM(produkte.preis * bestellungen.menge) AS summe
        FROM bestellungen
        JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
        GROUP BY bestellungen.schueler_id
    )
);
```
</details>
