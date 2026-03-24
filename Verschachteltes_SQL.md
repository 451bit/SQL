# Kapitel 2: Verschachtelte SQL-Abfragen

**Datenbank:** `schule.db` – öffne die Datei direkt mit *DB Browser for SQLite*  
**Thema:** Subqueries (verschachtelte Abfragen)

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten im ER-Diagramm](Schwache_Entitaeten.md)

---

## 1. Zum Grübeln – ein Problem zum Einstieg

Du hast in Kapitel 1 gelernt, wie man mit Aggregatfunktionen Werte zusammenfasst. Jetzt kommt eine Frage, die auf den ersten Blick einfach wirkt:

**„Welche Produkte in der Kantine kosten mehr als der Durchschnitt aller Produkte?"**

Dein erster Versuch:

```sql
SELECT name, preis
FROM produkte
WHERE preis > AVG(preis);
```

> **Teste diese Abfrage.** Was passiert? Lies die Fehlermeldung genau – was bedeutet sie?

SQLite verweigert diese Abfrage, weil `AVG()` eine Aggregatfunktion ist und nicht direkt in einem `WHERE` verwendet werden darf. `WHERE` filtert *einzelne Zeilen* – aber `AVG(preis)` kennt erst alle Zeilen zusammen.

**Die Lösung:** Man berechnet den Durchschnitt in einer eigenen, *inneren* Abfrage und verwendet das Ergebnis dann in der äußeren:

```sql
SELECT name, preis
FROM produkte
WHERE preis > (SELECT AVG(preis) FROM produkte);
```

> **Teste diese Abfrage.** Welche Produkte erscheinen? Überlege: Warum liefert die innere Abfrage genau einen Wert?

Das Konstrukt `(SELECT ...)` mitten in einer Abfrage nennt man **Subquery** (auch: Unterabfrage oder verschachtelte Abfrage).

---

## 2. Was ist eine Subquery?

Eine **Subquery** ist eine vollständige `SELECT`-Abfrage, die *innerhalb* einer anderen Abfrage steht. Sie wird immer zuerst ausgeführt – ihr Ergebnis wird dann von der äußeren Abfrage weiterverwendet.

```
äußere Abfrage
└── (innere Abfrage / Subquery)
         wird zuerst ausgeführt
```

**Grundprinzip:**

```sql
SELECT spalte
FROM tabelle
WHERE spalte operator (SELECT ... FROM ...);
```

### Wo kann eine Subquery stehen?

| Position | Bezeichnung | Beispiel |
|---|---|---|
| Im `WHERE` | skalare Subquery | `WHERE preis > (SELECT AVG(preis) ...)` |
| Im `FROM` | abgeleitete Tabelle | `FROM (SELECT ... ) AS t` |
| Im `HAVING` | aggregierte Subquery | `HAVING AVG(note) < (SELECT AVG(note) ...)` |

---

## 3. Subquery im `WHERE` – skalare Subquery

Die häufigste Form: Die innere Abfrage liefert **genau einen Wert** (eine Zahl, ein Datum, einen Text), mit dem verglichen wird.

### Beispiel: Schüler aus der gleichen Klasse wie Leon

```sql
SELECT vorname, nachname
FROM schueler
WHERE klasse_id = (SELECT klasse_id FROM schueler WHERE vorname = 'Leon' AND nachname = 'Bauer');
```

> **Teste diese Abfrage.** Was liefert die innere Abfrage alleine? Führe sie separat aus:
> ```sql
> SELECT klasse_id FROM schueler WHERE vorname = 'Leon' AND nachname = 'Bauer';
> ```

### Aufgabe 1

Zeige alle Schüler, die in der gleichen Klasse wie **Emma Schneider** sind.  
Gib Vorname und Nachname aus.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT vorname, nachname
FROM schueler
WHERE klasse_id = (SELECT klasse_id FROM schueler WHERE vorname = 'Emma' AND nachname = 'Schneider');
```
</details>

---

### Aufgabe 2

Zeige alle Produkte, die **billiger als das teuerste Getränk** (`kategorie = 'Getränk'`) sind.  
Gib Name, Kategorie und Preis aus.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT name, kategorie, preis
FROM produkte
WHERE preis < (SELECT MAX(preis) FROM produkte WHERE kategorie = 'Getränk');
```
</details>

---

## 4. Subquery im `HAVING` – Vergleich mit dem Gesamtdurchschnitt

Subqueries im `HAVING` ermöglichen den Vergleich eines Gruppenwertes mit einem globalen Aggregat.

### Beispiel: Fächer mit überdurchschnittlich schlechten Noten

```sql
SELECT faecher.name,
       ROUND(AVG(noten.note), 2) AS durchschnitt
FROM noten
JOIN faecher ON noten.fach_id = faecher.fach_id
GROUP BY noten.fach_id
HAVING AVG(noten.note) > (SELECT AVG(note) FROM noten);
```

> **Teste diese Abfrage.** Führe auch die innere Abfrage separat aus – was ist der Gesamtdurchschnitt aller Noten? Welche Fächer liegen darüber?

### Aufgabe 3

Zeige alle Schülerinnen und Schüler, deren persönlicher Notendurchschnitt **besser als der Gesamtdurchschnitt** aller Noten in der Datenbank ist.  
Gib Vorname, Nachname und den Durchschnitt aus (gerundet auf 2 Stellen).

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

## 5. Subquery im `FROM` – abgeleitete Tabelle

Eine Subquery im `FROM` verhält sich wie eine temporäre Tabelle. Sie **muss einen Alias** erhalten.

```sql
SELECT *
FROM (SELECT ...) AS aliasname
```

### Beispiel: Die drei teuersten Bestellungen

Gesucht: Wer hat bei einer einzelnen Bestellung (ein Produkt, eine Menge) am meisten ausgegeben?

```sql
SELECT schueler.vorname, schueler.nachname, teilsummen.ausgabe
FROM (
    SELECT schueler_id,
           ROUND(produkte.preis * bestellungen.menge, 2) AS ausgabe
    FROM bestellungen
    JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
) AS teilsummen
JOIN schueler ON teilsummen.schueler_id = schueler.schueler_id
ORDER BY teilsummen.ausgabe DESC
LIMIT 3;
```

> **Teste diese Abfrage.** Führe zunächst nur die innere Abfrage (den Subquery-Teil zwischen den äußeren Klammern) aus – was siehst du? Was macht der äußere Teil daraus?

### Aufgabe 4

Zeige den Schüler mit dem **höchsten Gesamtausgaben** in der Kantine.  
Verwende eine Subquery im `FROM`, um zuerst die Gesamtsumme pro Schüler zu berechnen, und zeige dann nur die maximale Zeile.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT schueler.vorname || ' ' || schueler.nachname AS name,
       gesamtausgaben.gesamt
FROM (
    SELECT schueler_id,
           ROUND(SUM(produkte.preis * bestellungen.menge), 2) AS gesamt
    FROM bestellungen
    JOIN produkte ON bestellungen.produkt_id = produkte.produkt_id
    GROUP BY schueler_id
) AS gesamtausgaben
JOIN schueler ON gesamtausgaben.schueler_id = schueler.schueler_id
ORDER BY gesamtausgaben.gesamt DESC
LIMIT 1;
```
</details>

---

## 6. Was ist zu beachten?

| Regel | Erklärung |
|---|---|
| Innere Abfrage zuerst | SQL führt die Subquery aus, bevor die äußere Abfrage läuft. |
| Skalare Subquery → 1 Wert | Im `WHERE` mit `=`, `<`, `>` darf die Subquery nur **eine Zeile, eine Spalte** liefern. Mehrere Werte → Fehler. |
| Alias im `FROM` Pflicht | Eine Subquery im `FROM` **muss** mit `AS name` benannt werden. |
| Subquery separat testen | Immer zuerst die innere Abfrage alleine ausführen und das Ergebnis prüfen, bevor man sie einbettet. |
| Lesbarkeit | Subqueries können schnell unübersichtlich werden. Einrücken und kommentieren hilft. |

---

## 7. Kombinations-Aufgaben

### Aufgabe 5

Zeige alle Produkte, die **teurer als der Durchschnittspreis ihrer eigenen Kategorie** sind.  
Hinweis: Das ist knifflig – die Subquery muss für jede Zeile der äußeren Abfrage den Kategoriedurchschnitt berechnen. Nutze einen Bezug auf die äußere Tabelle in der inneren Abfrage (`WHERE kategorie = p.kategorie`).

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT p.name, p.kategorie, p.preis
FROM produkte AS p
WHERE p.preis > (
    SELECT AVG(preis)
    FROM produkte
    WHERE kategorie = p.kategorie
);
```
</details>

---

### Aufgabe 6

Welche Klasse hat den **besten Notendurchschnitt** (niedrigsten Wert)?  
Zeige nur diese eine Klasse mit Bezeichnung und Durchschnitt.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT klassen.bezeichnung,
       ROUND(AVG(noten.note), 2) AS durchschnitt
FROM noten
JOIN schueler ON noten.schueler_id = schueler.schueler_id
JOIN klassen  ON schueler.klasse_id = klassen.klasse_id
GROUP BY klassen.klasse_id
HAVING AVG(noten.note) = (
    SELECT MIN(klassenschnitt) FROM (
        SELECT AVG(note) AS klassenschnitt
        FROM noten
        JOIN schueler ON noten.schueler_id = schueler.schueler_id
        GROUP BY schueler.klasse_id
    )
);
```
</details>

---

### Aufgabe 7

Zeige alle Schüler, die **noch nie etwas in der Kantine bestellt** haben.  
*Hinweis:* Verwende `NOT IN` mit einer Subquery.

```sql
-- Deine Lösung:

```

<details>
<summary>Lösung</summary>

```sql
SELECT vorname, nachname
FROM schueler
WHERE schueler_id NOT IN (
    SELECT DISTINCT schueler_id
    FROM bestellungen
);
```
</details>

---

> Weiter mit [Kapitel 3 – Schwache Entitäten im ER-Diagramm](Schwache_Entitaeten.md)
