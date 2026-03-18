# SQL-Arbeitsblatt: Aggregatfunktionen

**Datenbank:** `schule.db`  
**Thema:** Aggregatfunktionen und `GROUP BY`

---

## Die Ausgangssituation

Unser Schulsystem speichert Daten in folgenden Tabellen:

| Tabelle | Inhalt |
|---|---|
| `klassen` | Klassen (9a, 9b, 10a, 10b) mit Klassenlehrer |
| `schueler` | 20 Schülerinnen und Schüler mit Klasse |
| `faecher` | Fächer (Mathe, Deutsch, Englisch, Informatik, Sport) |
| `noten` | Einzelne Noten (Klassenarbeit, Test, mündlich) |
| `produkte` | Kantinenangebot mit Preis und Kategorie |
| `bestellungen` | Jede Bestellung eines Schülers in der Kantine |

**Kurzübersicht der Tabellenstruktur:**

```
schueler(schueler_id, vorname, nachname, klasse_id, ...)
noten(noten_id, schueler_id, fach_id, note, datum, art)
bestellungen(bestell_id, schueler_id, produkt_id, datum, menge)
produkte(produkt_id, name, kategorie, preis)
klassen(klasse_id, bezeichnung, stufe, klassenlehrer)
```

---

## 1. Das Problem – Was ohne Aggregation nicht geht

### Aufgabe

Du willst wissen: **„Wie viel hat jeder Schüler insgesamt in der Kantine ausgegeben?"**

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
1           | 0.80
...
```

**Das Problem:** Eine normale `SELECT`-Abfrage zeigt dir *Einzelwerte*. Du kannst damit nicht automatisch zusammenrechnen, zählen oder den Durchschnitt bilden. Dafür brauchst du **Aggregatfunktionen**.

---

## 2. Aggregatfunktionen – Überblick

Aggregatfunktionen fassen **mehrere Zeilen zu einem einzigen Ergebniswert** zusammen.

| Funktion | Bedeutung | Beispiel |
|---|---|---|
| `COUNT(...)` | Anzahl der Zeilen | Wie viele Bestellungen? |
| `SUM(...)` | Summe aller Werte | Gesamtumsatz der Kantine |
| `AVG(...)` | Durchschnitt der Werte | Durchschnittsnote in Mathe |
| `MIN(...)` | Kleinster Wert | Billigstes Produkt |
| `MAX(...)` | Größter Wert | Teuerste Bestellung |

---

## 3. Die Funktionen im Einsatz

### 3.1 `COUNT` – Wie viele?

`COUNT(*)` zählt alle Zeilen. `COUNT(spalte)` zählt alle Zeilen, in denen die Spalte **nicht leer** ist.

**Beispiel A:** Wie viele Schüler sind in der Datenbank gespeichert?

```sql
SELECT COUNT(*) AS anzahl_schueler
FROM schueler;
```

| anzahl_schueler |
|---|
| 20 |

**Beispiel B:** Wie viele Bestellungen hat Leon (schueler_id = 1) aufgegeben?

```sql
SELECT COUNT(*) AS anzahl_bestellungen
FROM bestellungen
WHERE schueler_id = 1;
```

| anzahl_bestellungen |
|---|
| 8 |

---

### 3.2 `SUM` – Wie viel insgesamt?

**Beispiel:** Wie viel hat Leon insgesamt in der Kantine ausgegeben?

```sql
SELECT SUM(produkte.preis * bestellungen.menge) AS gesamtausgabe
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
WHERE bestellungen.schueler_id = 1;
```

| gesamtausgabe |
|---|
| 16.50 |

> **Hinweis:** Die Spalte `menge` berücksichtigt, wie oft ein Produkt pro Bestellung gekauft wurde.

---

### 3.3 `AVG` – Was ist der Durchschnitt?

**Beispiel:** Was ist Leonidas' Durchschnittsnote in allen Fächern?

```sql
SELECT AVG(note) AS durchschnittsnote
FROM noten
WHERE schueler_id = 1;
```

| durchschnittsnote |
|---|
| 2.0 |

---

### 3.4 `MIN` und `MAX` – Extremwerte

**Beispiel:** Was ist das billigste und das teuerste Produkt in der Kantine?

```sql
SELECT MIN(preis) AS guenstigstes,
       MAX(preis) AS teuerstes
FROM produkte;
```

| guenstigstes | teuerstes |
|---|---|
| 0.80 | 4.20 |

---

## 4. `GROUP BY` – Für jede Gruppe ein Ergebnis

Bisher haben alle Aggregatfunktionen **eine einzige Zahl** für die gesamte Tabelle berechnet. Mit `GROUP BY` kannst du die Daten **in Gruppen aufteilen** und für jede Gruppe separat aggregieren.

### Syntax

```sql
SELECT gruppierungsspalte, AGGREGATFUNKTION(spalte)
FROM tabelle
GROUP BY gruppierungsspalte;
```

**Regel:** Alle Spalten im `SELECT`, die *keine* Aggregatfunktion sind, **müssen** in `GROUP BY` stehen.

---

### 4.1 Gesamtausgabe jedes Schülers

```sql
SELECT schueler_id,
       SUM(produkte.preis * bestellungen.menge) AS gesamtausgabe
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
GROUP BY bestellungen.schueler_id;
```

| schueler_id | gesamtausgabe |
|---|---|
| 1 | 16.50 |
| 2 | 11.30 |
| 3 | 15.40 |
| ... | ... |

Jetzt bekommt jeder Schüler **eine eigene Zeile** mit seiner persönlichen Gesamtsumme.

---

### 4.2 Durchschnittsnote pro Fach

```sql
SELECT fach_id,
       AVG(note) AS durchschnitt,
       MIN(note) AS beste_note,
       MAX(note) AS schlechteste_note
FROM noten
GROUP BY fach_id;
```

| fach_id | durchschnitt | beste_note | schlechteste_note |
|---|---|---|---|
| 1 | 2.75 | 1.0 | 5.0 |
| 2 | 2.70 | 1.0 | 5.0 |
| ... | ... | ... | ... |

---

### 4.3 Lesbare Ausgabe mit JOIN

Statt der `fach_id` kann man den Fachnamen anzeigen, indem man mit `faecher` joined:

```sql
SELECT faecher.name AS fach,
       ROUND(AVG(note), 2) AS durchschnitt
FROM noten
JOIN faecher ON noten.fach_id = faecher.fach_id
GROUP BY noten.fach_id;
```

| fach | durchschnitt |
|---|---|
| Mathematik | 2.75 |
| Deutsch | 2.65 |
| Englisch | 2.65 |
| Informatik | 2.5 |

> **`ROUND(wert, 2)`** rundet auf 2 Nachkommastellen.

---

### 4.4 Anzahl Bestellungen pro Schüler mit Name

```sql
SELECT schueler.vorname || ' ' || schueler.nachname AS name,
       COUNT(*) AS anzahl_bestellungen
FROM bestellungen
JOIN schueler ON bestellungen.schueler_id = schueler.schueler_id
GROUP BY bestellungen.schueler_id
ORDER BY anzahl_bestellungen DESC;
```

| name | anzahl_bestellungen |
|---|---|
| Leon Bauer | 8 |
| Finn Schulz | 6 |
| Luca Hoffmann | 6 |
| ... | ... |

---

### 4.5 Umsatz pro Produktkategorie

```sql
SELECT kategorie,
       COUNT(*) AS bestellungen,
       SUM(preis * menge) AS umsatz
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
GROUP BY kategorie
ORDER BY umsatz DESC;
```

| kategorie | bestellungen | umsatz |
|---|---|---|
| Hauptgericht | 62 | 224.80 |
| Getränk | 28 | 32.90 |
| Snack | 17 | 27.30 |

---

## 5. `HAVING` – Gruppen filtern

`WHERE` filtert **Zeilen** *vor* der Aggregation.  
`HAVING` filtert **Gruppen** *nach* der Aggregation.

> **Merksatz:** `WHERE` arbeitet mit Einzelwerten, `HAVING` mit Aggregatwerten.

### Beispiel: Nur Fächer, in denen der Durchschnitt schlechter als 2,5 ist

```sql
SELECT faecher.name,
       ROUND(AVG(note), 2) AS durchschnitt
FROM noten
JOIN faecher ON noten.fach_id = faecher.fach_id
GROUP BY noten.fach_id
HAVING AVG(note) > 2.5;
```

### Beispiel: Schüler, die mehr als 5 Bestellungen aufgegeben haben

```sql
SELECT schueler.vorname || ' ' || schueler.nachname AS name,
       COUNT(*) AS anzahl
FROM bestellungen
JOIN schueler ON bestellungen.schueler_id = schueler.schueler_id
GROUP BY bestellungen.schueler_id
HAVING COUNT(*) > 5
ORDER BY anzahl DESC;
```

---

## 6. Verarbeitungsreihenfolge in SQL

Eine SQL-Abfrage wird in dieser Reihenfolge verarbeitet – **nicht** so, wie sie geschrieben steht:

```
1. FROM / JOIN   → Welche Tabellen?
2. WHERE         → Welche Zeilen?
3. GROUP BY      → Gruppen bilden
4. HAVING        → Gruppen filtern
5. SELECT        → Was ausgeben?
6. ORDER BY      → Sortierung
7. LIMIT         → Anzahl begrenzen
```

Das erklärt, warum du in `HAVING` **keine Alias-Namen** aus dem `SELECT` verwenden kannst:

```sql
-- ✗ Falsch: 'durchschnitt' ist beim HAVING noch nicht bekannt
HAVING durchschnitt > 2.5

-- ✓ Richtig: Aggregatfunktion direkt wiederholen
HAVING AVG(note) > 2.5
```

---

## 7. Aufgaben

### Aufgabe 1 – COUNT
Wie viele Schülerinnen (Geschlecht = `'w'`) sind in der Datenbank?

```sql
-- Deine Lösung:

```

---

### Aufgabe 2 – SUM
Berechne den Gesamtumsatz der Kantine über alle Bestellungen.

```sql
-- Deine Lösung:

```

---

### Aufgabe 3 – AVG mit WHERE
Berechne den Notendurchschnitt von Sophie Wagner (schueler_id = 2) in **Mathematik** (fach_id = 1).

```sql
-- Deine Lösung:

```

---

### Aufgabe 4 – GROUP BY
Zeige für jede Klasse (nach `klasse_id`) die Anzahl der Schüler an.

```sql
-- Deine Lösung:

```

---

### Aufgabe 5 – GROUP BY mit JOIN
Zeige für jede Klasse den **Klassennamen** (aus der Tabelle `klassen`) und die Anzahl der Schüler.

```sql
-- Deine Lösung:

```

---

### Aufgabe 6 – HAVING
Zeige alle Schüler an, deren Durchschnittsnote in der Tabelle `noten` besser als 2,0 ist (also kleiner als 2,0, da 1 die beste Note ist).  
Gib Vorname, Nachname und den gerundeten Durchschnitt aus.

```sql
-- Deine Lösung:

```

---

### Aufgabe 7 – Kombiniert
Welche **Produkte** aus der Kantine wurden insgesamt am häufigsten bestellt?  
Zeige Produktname und Gesamtmenge, sortiert nach Gesamtmenge absteigend. Zeige nur die Top 3.

```sql
-- Deine Lösung:

```

---

## 8. Lösungen

<details>
<summary>Aufgabe 1</summary>

```sql
SELECT COUNT(*) AS anzahl_schülerinnen
FROM schueler
WHERE geschlecht = 'w';
```
</details>

<details>
<summary>Aufgabe 2</summary>

```sql
SELECT SUM(produkte.preis * bestellungen.menge) AS gesamtumsatz
FROM bestellungen
JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id;
```
</details>

<details>
<summary>Aufgabe 3</summary>

```sql
SELECT AVG(note) AS durchschnitt
FROM noten
WHERE schueler_id = 2
  AND fach_id = 1;
```
</details>

<details>
<summary>Aufgabe 4</summary>

```sql
SELECT klasse_id, COUNT(*) AS anzahl_schueler
FROM schueler
GROUP BY klasse_id;
```
</details>

<details>
<summary>Aufgabe 5</summary>

```sql
SELECT klassen.bezeichnung, COUNT(*) AS anzahl_schueler
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id
GROUP BY schueler.klasse_id;
```
</details>

<details>
<summary>Aufgabe 6</summary>

```sql
SELECT schueler.vorname, schueler.nachname,
       ROUND(AVG(note), 2) AS durchschnitt
FROM noten
JOIN schueler ON noten.schueler_id = schueler.schueler_id
GROUP BY noten.schueler_id
HAVING AVG(note) < 2.0;
```
</details>

<details>
<summary>Aufgabe 7</summary>

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
