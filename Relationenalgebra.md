# Kapitel 8: Relationenalgebra

**Datenbank:** `schule.db`  
**Thema:** Formale Beschreibung von Datenbankabfragen mit der Relationenalgebra

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md) · [Kapitel 7 – DML in SQL](DML.md) · [Projekt – Wetterdatenbank](Projekt_Wetterdatenbank.md) · [Kapitel 8 – Relationenalgebra](Relationenalgebra.md)

---

## Was ist die Relationenalgebra?

SQL ist eine **deklarative** Sprache: Man beschreibt *was* man haben möchte, nicht *wie* der Computer es ermitteln soll. Hinter SQL steckt eine formale, mathematische Grundlage – die **Relationenalgebra**.

Die Relationenalgebra stellt eine Menge von **Operationen** bereit, die auf Tabellen (= Relationen) angewendet werden. Jede Operation nimmt eine oder zwei Relationen als Eingabe und liefert immer wieder eine **Relation** als Ergebnis. Dadurch können Operationen beliebig kombiniert und ineinander verschachtelt werden.

> **Warum lernen wir das?**  
> Relationenalgebra-Ausdrücke beschreiben Datenbankabfragen **präzise und eindeutig** – unabhängig von einer konkreten Programmiersprache. Außerdem ist das Verständnis von Relationenalgebra Prüfungsstoff im Informatik-Landesabitur Hessen (LA 2026).

---

## Das verwendete Datenbankschema

Alle Beispiele verwenden die Schuldatenbank mit folgenden Tabellen:

```
schueler(schueler_id, vorname, nachname, klasse_id, geburtsdatum, geschlecht)
klassen(klasse_id, bezeichnung, stufe, klassenlehrer)
faecher(fach_id, name, kuerzel)
noten(noten_id, schueler_id, fach_id, note, datum, art)
produkte(produkt_id, name, kategorie, preis)
bestellungen(bestell_id, schueler_id, produkt_id, datum, menge)
```

---

## Überblick: Die Operatoren

| Symbol | Name | Was es tut | SQL-Entsprechung |
|:---:|---|---|---|
| **σ** | Selektion | Zeilen filtern (nach Bedingung) | `WHERE` |
| **π** | Projektion | Spalten auswählen | `SELECT` (ohne Duplikatentfernung) |
| **⋈** | Verbund (Join) | Tabellen verknüpfen | `JOIN … ON …` |
| **∪** | Vereinigung | Alle Zeilen beider Tabellen | `UNION` |
| **−** | Differenz | Zeilen, die nur in der linken Tabelle stehen | `EXCEPT` |
| **∩** | Durchschnitt | Zeilen, die in beiden Tabellen stehen | `INTERSECT` |
| **×** | Kreuzprodukt | Alle Kombinationen zweier Tabellen | `FROM A, B` (ohne WHERE) |

---

## 1. Selektion – σ (Sigma)

### Bedeutung

Die **Selektion** filtert Zeilen aus einer Tabelle heraus. Sie wählt nur die Tupel aus, die eine bestimmte Bedingung erfüllen.

> Selektion = Zeilen filtern = Zeilenauswahl

### Notation

$$\sigma_{\text{Bedingung}}(\text{Relation})$$

Die Bedingung kann enthalten:
- Vergleiche: `=`, `≠`, `<`, `>`, `≤`, `≥`
- Logische Verknüpfungen: `∧` (und), `∨` (oder), `¬` (nicht)

### Beispiel

**Aufgabe:** Alle Schüler des Geschlechts „w" auswählen.

**Relationenalgebra:**
$$\sigma_{\text{geschlecht} = \text{'w'}}(\text{schueler})$$

**Ergebnis:** Eine neue Tabelle mit denselben Spalten wie `schueler`, aber nur den Zeilen, bei denen `geschlecht = 'w'` gilt.

**SQL-Entsprechung:**
```sql
SELECT *
FROM schueler
WHERE geschlecht = 'w';
```

---

**Weiteres Beispiel:** Alle Noten, die schlechter als 4 sind und mündlich vergeben wurden.

**Relationenalgebra:**
$$\sigma_{\text{note} > 4 \,\wedge\, \text{art} = \text{'mündlich'}}(\text{noten})$$

**SQL:**
```sql
SELECT *
FROM noten
WHERE note > 4 AND art = 'mündlich';
```

---

## 2. Projektion – π (Pi)

### Bedeutung

Die **Projektion** wählt bestimmte Spalten aus einer Tabelle aus und blendet alle anderen aus. Doppelte Zeilen werden entfernt (Mengensemantik).

> Projektion = Spalten auswählen = Spaltenauswahl

### Notation

$$\pi_{\text{Spalte}_1,\, \text{Spalte}_2,\, \ldots}(\text{Relation})$$

### Beispiel

**Aufgabe:** Nur Vor- und Nachname aller Schüler ausgeben.

**Relationenalgebra:**
$$\pi_{\text{vorname},\, \text{nachname}}(\text{schueler})$$

**Ergebnis:** Eine Tabelle mit nur zwei Spalten: `vorname` und `nachname`.

**SQL:**
```sql
SELECT vorname, nachname
FROM schueler;
```

---

**Weiteres Beispiel:** Welche Notenarten gibt es? (Jede Notenart nur einmal)

**Relationenalgebra:**
$$\pi_{\text{art}}(\text{noten})$$

**SQL:**
```sql
SELECT DISTINCT art
FROM noten;
```

> **Hinweis:** In der Relationenalgebra werden Duplikate durch die Projektion automatisch entfernt (Mengensemantik). In SQL muss man `DISTINCT` explizit angeben, wenn man das möchte.

---

## 3. Kombination von Selektion und Projektion

Selektion und Projektion lassen sich kombinieren: zuerst Zeilen filtern, dann Spalten auswählen (oder umgekehrt, aber Selektion zuerst ist effizienter).

### Notation

$$\pi_{\text{Spalten}}\bigl(\sigma_{\text{Bedingung}}(\text{Relation})\bigr)$$

Der innere Ausdruck wird zuerst ausgeführt – wie in der Mathematik werden Klammern von innen nach außen aufgelöst.

### Beispiel

**Aufgabe:** Vor- und Nachname aller weiblichen Schülerinnen.

**Relationenalgebra:**
$$\pi_{\text{vorname},\, \text{nachname}}\bigl(\sigma_{\text{geschlecht} = \text{'w'}}(\text{schueler})\bigr)$$

**Ausführungsreihenfolge:**
1. `σ` filtert die `schueler`-Tabelle → nur weibliche Schülerinnen
2. `π` wählt aus dem Ergebnis die Spalten `vorname` und `nachname` aus

**SQL:**
```sql
SELECT vorname, nachname
FROM schueler
WHERE geschlecht = 'w';
```

---

## 4. Verbund – ⋈ (Join)

### Bedeutung

Der **Verbund** (Join) verknüpft zwei Tabellen anhand einer gemeinsamen Bedingung (meist: gleiche Schlüsselwerte in einer Fremdschlüsselbeziehung).

> Verbund = Tabellen zusammenfügen

### Varianten

#### a) Theta-Verbund (allgemeiner Verbund)

$$R \underset{\text{Bedingung}}{\bowtie} S$$

Verknüpft alle Tupel aus $R$ und $S$, für die die Bedingung gilt. Beide Fremdschlüsselspalten sind im Ergebnis enthalten.

#### b) Equi-Join (Gleichverbund)

Spezialfall des Theta-Verbunds: Die Bedingung ist eine Gleichheit.

$$\text{schueler} \underset{\text{schueler.klasse\_id} = \text{klassen.klasse\_id}}{\bowtie} \text{klassen}$$

#### c) Natural Join (natürlicher Verbund)

$$R \bowtie S$$

Verbindet automatisch über **alle gleichnamigen Spalten** und entfernt eine der doppelten Spalten aus dem Ergebnis.

### Beispiel mit Equi-Join

**Aufgabe:** Schüler zusammen mit ihrer Klassenbezeichnung anzeigen.

**Relationenalgebra:**
$$\text{schueler} \underset{\text{schueler.klasse\_id} = \text{klassen.klasse\_id}}{\bowtie} \text{klassen}$$

**Ergebnis:** Eine Tabelle mit allen Spalten aus `schueler` und `klassen` (wobei `klasse_id` doppelt vorkommt).

**SQL:**
```sql
SELECT *
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id;
```

---

### Kombination: Verbund + Selektion + Projektion

**Aufgabe:** Vorname, Nachname und Klassenbezeichnung aller Schüler der Stufe 10.

**Relationenalgebra:**
$$\pi_{\text{vorname},\, \text{nachname},\, \text{bezeichnung}}\Bigl(\sigma_{\text{stufe} = 10}\bigl(\text{schueler} \underset{\text{schueler.klasse\_id} = \text{klassen.klasse\_id}}{\bowtie} \text{klassen}\bigr)\Bigr)$$

**Ausführungsreihenfolge:**
1. **⋈** verbindet `schueler` und `klassen`
2. **σ** filtert auf `stufe = 10`
3. **π** wählt die drei Spalten aus

**SQL:**
```sql
SELECT vorname, nachname, bezeichnung
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id
WHERE stufe = 10;
```

---

### Mehrfach-Verbund (drei oder mehr Tabellen)

**Aufgabe:** Vorname, Nachname und Fachnamen aller Noten, die schlechter als 3 sind.

**Relationenalgebra:**
$$\pi_{\text{vorname},\, \text{nachname},\, \text{faecher.name}}\Bigl(\sigma_{\text{note} > 3}\bigl((\text{schueler} \underset{\text{schueler.schueler\_id} = \text{noten.schueler\_id}}{\bowtie} \text{noten}) \underset{\text{noten.fach\_id} = \text{faecher.fach\_id}}{\bowtie} \text{faecher}\bigr)\Bigr)$$

**SQL:**
```sql
SELECT vorname, nachname, faecher.name
FROM schueler
JOIN noten   ON schueler.schueler_id = noten.schueler_id
JOIN faecher ON noten.fach_id        = faecher.fach_id
WHERE note > 3;
```

---

## 5. Kreuzprodukt – ×

### Bedeutung

Das **Kreuzprodukt** (auch kartesisches Produkt) kombiniert jede Zeile der ersten Tabelle mit jeder Zeile der zweiten Tabelle. Es entstehen `|R| × |S|` Zeilen.

$$R \times S$$

Das Kreuzprodukt ist die Grundlage des Verbunds:
$$R \underset{\text{Bedingung}}{\bowtie} S = \sigma_{\text{Bedingung}}(R \times S)$$

> **Im Unterricht:** Das Kreuzprodukt alleine ist selten nützlich (zu viele bedeutungslose Kombinationen). In der Praxis immer sofort eine Selektion dahinter.

### Beispiel

`schueler × klassen` erzeugt alle Kombinationen – auch unsinnige wie Schüler-Klasse-Paare, die gar nicht zusammengehören. Erst die Selektion `σ_{schueler.klasse_id = klassen.klasse_id}` macht daraus den sinnvollen Join.

---

## 6. Vereinigung – ∪

### Bedeutung

Die **Vereinigung** fügt die Zeilen zweier Tabellen zusammen. Doppelte Zeilen werden entfernt.

**Voraussetzung:** Beide Tabellen müssen dasselbe Schema haben (gleiche Anzahl und Art von Spalten).

$$R \cup S$$

### Beispiel

**Aufgabe:** Eine Liste aller Personen, die entweder als Schüler oder als Klassenlehrer in der Datenbank stehen.

Zuerst müssen die Schemata vereinheitlicht werden (beide Tabellen auf die gleichen Spalten projizieren):

$$\pi_{\text{name}}\bigl(\sigma_{\text{...}}(\text{schueler})\bigr) \cup \pi_{\text{klassenlehrer}}(\text{klassen})$$

**SQL:**
```sql
SELECT vorname || ' ' || nachname AS name FROM schueler
UNION
SELECT klassenlehrer FROM klassen;
```

> **`UNION` vs. `UNION ALL`:** `UNION` entfernt Duplikate (entspricht der Mengensemantik der Relationenalgebra). `UNION ALL` behält Duplikate.

---

## 7. Differenz – −

### Bedeutung

Die **Differenz** $R - S$ enthält alle Zeilen aus $R$, die **nicht** in $S$ vorkommen.

**Voraussetzung:** Gleiche Schemata (wie bei der Vereinigung).

$$R - S$$

> **Achtung:** Die Differenz ist **nicht kommutativ**: $R - S \neq S - R$

### Beispiel

**Aufgabe:** Welche Schüler haben noch **keine** Note bekommen?

$$\pi_{\text{schueler\_id}}(\text{schueler}) - \pi_{\text{schueler\_id}}(\text{noten})$$

**Ausführungsreihenfolge:**
1. `π` auf `schueler` → Tabelle mit allen Schüler-IDs
2. `π` auf `noten` → Tabelle mit allen Schüler-IDs, die mindestens eine Note haben
3. `−` → IDs, die nur in der linken, aber nicht in der rechten Tabelle stehen

**SQL:**
```sql
SELECT schueler_id FROM schueler
EXCEPT
SELECT schueler_id FROM noten;
```

---

## 8. Durchschnitt – ∩

### Bedeutung

Der **Durchschnitt** (Schnittmenge) $R \cap S$ enthält alle Zeilen, die **sowohl** in $R$ **als auch** in $S$ vorkommen.

**Voraussetzung:** Gleiche Schemata.

$$R \cap S$$

Der Durchschnitt kann auch durch die Differenz ausgedrückt werden:
$$R \cap S = R - (R - S)$$

### Beispiel

**Aufgabe:** Welche Schüler haben sowohl in Mathe als auch in Deutsch eine Note?

```
Schüler mit Mathe-Note:    π_{schueler_id}(σ_{fach_id = 1}(noten))
Schüler mit Deutsch-Note:  π_{schueler_id}(σ_{fach_id = 2}(noten))
```

$$\pi_{\text{schueler\_id}}\bigl(\sigma_{\text{fach\_id} = 1}(\text{noten})\bigr) \cap \pi_{\text{schueler\_id}}\bigl(\sigma_{\text{fach\_id} = 2}(\text{noten})\bigr)$$

**SQL:**
```sql
SELECT schueler_id FROM noten WHERE fach_id = 1
INTERSECT
SELECT schueler_id FROM noten WHERE fach_id = 2;
```

---

## 9. Ausführungsreihenfolge und Klammern

### Regel

Wie in der Mathematik gilt: **von innen nach außen**. Klammern bestimmen die Reihenfolge.

$$\pi_{\text{A}}\bigl(\sigma_{\text{B}}(\text{Tabelle})\bigr)$$

→ Erst σ, dann π.

### Prioritäten (ohne Klammern)

Wenn keine Klammern gesetzt sind, gilt folgende Priorität (von hoch zu niedrig):

1. **σ, π** – unäre Operatoren (wirken auf eine Relation)
2. **×, ⋈** – Kreuzprodukt und Verbund
3. **∩** – Durchschnitt
4. **∪, −** – Vereinigung und Differenz

> **Empfehlung:** Setze im Zweifel immer **Klammern**, um die Reihenfolge eindeutig zu machen.

### Lesetipp für verschachtelte Ausdrücke

Beim Lesen eines komplexen Ausdrucks:
1. Finde den **innersten** Klammerausdruck → das ist der erste Schritt.
2. Arbeite dich **von innen nach außen** vor.

**Beispiel:**
$$\pi_{\text{vorname}}\Bigl(\sigma_{\text{stufe}=9}\bigl(\text{schueler} \underset{\text{schueler.klasse\_id = klassen.klasse\_id}}{\bowtie} \text{klassen}\bigr)\Bigr)$$

Schritt 1: `schueler ⋈ klassen` → verbundene Tabelle  
Schritt 2: `σ_{stufe=9}(...)` → nur Stufe-9-Schüler  
Schritt 3: `π_{vorname}(...)` → nur die Vornamen

---

## 10. Zusammenfassung: Relationenalgebra ↔ SQL

| Relationenalgebra | SQL |
|---|---|
| $\sigma_{\text{Bedingung}}(R)$ | `SELECT * FROM R WHERE Bedingung` |
| $\pi_{\text{A,B}}(R)$ | `SELECT DISTINCT A, B FROM R` |
| $R \underset{R.x = S.y}{\bowtie} S$ | `FROM R JOIN S ON R.x = S.y` |
| $R \times S$ | `FROM R, S` (ohne WHERE) |
| $R \cup S$ | `... UNION ...` |
| $R - S$ | `... EXCEPT ...` |
| $R \cap S$ | `... INTERSECT ...` |
| $\pi_B(\sigma_C(R))$ | `SELECT DISTINCT B FROM R WHERE C` |
| $\pi_B(\sigma_C(R \bowtie S))$ | `SELECT DISTINCT B FROM R JOIN S ON … WHERE C` |

---

## Übungsaufgaben

### Aufgabe 1: Relationenalgebra → SQL

Übersetze die folgenden Ausdrücke in SQL-Abfragen. Gib an, was das Ergebnis inhaltlich bedeutet.

---

**1a)**
$$\sigma_{\text{note} = 1}(\text{noten})$$

**1b)**
$$\pi_{\text{vorname},\, \text{nachname}}\bigl(\sigma_{\text{stufe} = 9}(\text{schueler} \underset{\text{schueler.klasse\_id = klassen.klasse\_id}}{\bowtie} \text{klassen})\bigr)$$

**1c)**
$$\pi_{\text{schueler\_id}}(\text{schueler}) - \pi_{\text{schueler\_id}}(\text{bestellungen})$$

**1d)**
$$\pi_{\text{vorname},\, \text{nachname},\, \text{note}}\Bigl(\sigma_{\text{kuerzel} = \text{'M'} \,\wedge\, \text{art} = \text{'Klassenarbeit'}}\bigl((\text{schueler} \underset{\text{schueler.schueler\_id = noten.schueler\_id}}{\bowtie} \text{noten}) \underset{\text{noten.fach\_id = faecher.fach\_id}}{\bowtie} \text{faecher}\bigr)\Bigr)$$

**1e)**
$$\pi_{\text{schueler\_id}}\bigl(\sigma_{\text{fach\_id} = 1}(\text{noten})\bigr) \cap \pi_{\text{schueler\_id}}\bigl(\sigma_{\text{fach\_id} = 3}(\text{noten})\bigr)$$

---

<details>
<summary>Lösungen Aufgabe 1</summary>

**1a)** Alle Noten mit Note 1 (alle Einsen):
```sql
SELECT *
FROM noten
WHERE note = 1;
```

**1b)** Vor- und Nachname aller Schüler der Stufe 9:
```sql
SELECT vorname, nachname
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id
WHERE stufe = 9;
```

**1c)** Schüler-IDs der Schüler, die noch nie etwas in der Kantine bestellt haben:
```sql
SELECT schueler_id FROM schueler
EXCEPT
SELECT schueler_id FROM bestellungen;
```

**1d)** Vorname, Nachname und Note aller Mathe-Klassenarbeiten:
```sql
SELECT vorname, nachname, note
FROM schueler
JOIN noten   ON schueler.schueler_id = noten.schueler_id
JOIN faecher ON noten.fach_id        = faecher.fach_id
WHERE faecher.kuerzel = 'M'
  AND art = 'Klassenarbeit';
```

**1e)** Schüler-IDs der Schüler, die sowohl in Fach 1 als auch in Fach 3 eine Note haben:
```sql
SELECT schueler_id FROM noten WHERE fach_id = 1
INTERSECT
SELECT schueler_id FROM noten WHERE fach_id = 3;
```
</details>

---

### Aufgabe 2: SQL → Relationenalgebra

Übersetze die folgenden SQL-Abfragen in die Relationenalgebra.

---

**2a)**
```sql
SELECT *
FROM produkte
WHERE preis < 2.00;
```

**2b)**
```sql
SELECT name, preis
FROM produkte
WHERE kategorie = 'Getränk';
```

**2c)**
```sql
SELECT vorname, nachname, bezeichnung
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id;
```

**2d)**
```sql
SELECT vorname, nachname
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id
WHERE stufe = 10 AND geschlecht = 'w';
```

**2e)**
```sql
SELECT schueler_id FROM bestellungen
EXCEPT
SELECT schueler_id FROM noten;
```

---

<details>
<summary>Lösungen Aufgabe 2</summary>

**2a)**
$$\sigma_{\text{preis} < 2{,}00}(\text{produkte})$$

**2b)**
$$\pi_{\text{name},\, \text{preis}}\bigl(\sigma_{\text{kategorie} = \text{'Getränk'}}(\text{produkte})\bigr)$$

**2c)**
$$\pi_{\text{vorname},\, \text{nachname},\, \text{bezeichnung}}\bigl(\text{schueler} \underset{\text{schueler.klasse\_id = klassen.klasse\_id}}{\bowtie} \text{klassen}\bigr)$$

**2d)**
$$\pi_{\text{vorname},\, \text{nachname}}\Bigl(\sigma_{\text{stufe} = 10 \,\wedge\, \text{geschlecht} = \text{'w'}}\bigl(\text{schueler} \underset{\text{schueler.klasse\_id = klassen.klasse\_id}}{\bowtie} \text{klassen}\bigr)\Bigr)$$

**2e)**
$$\pi_{\text{schueler\_id}}(\text{bestellungen}) - \pi_{\text{schueler\_id}}(\text{noten})$$

</details>

---

### Aufgabe 3: Inhaltliche Bedeutung beschreiben

Beschreibe in einem vollständigen deutschen Satz, was der folgende Ausdruck inhaltlich berechnet. Gib auch an, welche Spalten das Ergebnis hat.

---

**3a)**
$$\sigma_{\text{geschlecht} = \text{'m'} \,\wedge\, \text{klasse\_id} = 2}(\text{schueler})$$

**3b)**
$$\pi_{\text{klassenlehrer}}(\text{klassen})$$

**3c)**
$$\pi_{\text{schueler\_id}}(\text{schueler}) - \pi_{\text{schueler\_id}}(\text{noten})$$

**3d)**
$$\pi_{\text{vorname},\, \text{nachname}}\Bigl(\sigma_{\text{note} \leq 2}\bigl(\text{schueler} \underset{\text{schueler.schueler\_id = noten.schueler\_id}}{\bowtie} \text{noten}\bigr)\Bigr)$$

**3e)**
$$\pi_{\text{name}}\bigl(\sigma_{\text{kategorie} = \text{'Hauptgericht'}}(\text{produkte})\bigr) \cup \pi_{\text{name}}\bigl(\sigma_{\text{kategorie} = \text{'Dessert'}}(\text{produkte})\bigr)$$

---

<details>
<summary>Lösungen Aufgabe 3</summary>

**3a)** Alle männlichen Schüler aus der Klasse mit der ID 2.  
Ergebnisspalten: alle Spalten von `schueler` (schueler_id, vorname, nachname, klasse_id, geburtsdatum, geschlecht).

**3b)** Die Namen aller Klassenlehrer (jeder Name nur einmal, da Projektion Duplikate entfernt).  
Ergebnisspalten: `klassenlehrer`.

**3c)** Die IDs aller Schüler, die noch gar keine Note in der Datenbank haben (also noch nie bewertet wurden).  
Ergebnisspalten: `schueler_id`.

**3d)** Vorname und Nachname aller Schüler, die mindestens eine Note von 1 oder 2 erhalten haben. (Ein Schüler kann mehrfach auftauchen, wenn er mehrere solche Noten hat – außer wenn Duplikate durch π entfernt werden.)  
Ergebnisspalten: `vorname`, `nachname`.

**3e)** Die Namen aller Produkte, die entweder zur Kategorie „Hauptgericht" oder zur Kategorie „Dessert" gehören. Duplikate werden entfernt.  
Ergebnisspalten: `name`.
</details>

---

### Aufgabe 4: Ausführungsreihenfolge bestimmen

Nummeriere die Operationen des folgenden Ausdrucks in der Reihenfolge, in der sie ausgeführt werden (1 = zuerst):

$$\pi_{\text{vorname},\, \text{note}}\Bigl(\sigma_{\text{bezeichnung} = \text{'10a'} \,\wedge\, \text{note} < 3}\bigl(\text{schueler} \underset{\text{schueler.klasse\_id = klassen.klasse\_id}}{\bowtie} \text{klassen} \underset{\text{schueler.schueler\_id = noten.schueler\_id}}{\bowtie} \text{noten}\bigr)\Bigr)$$

<details>
<summary>Lösung Aufgabe 4</summary>

1. **⋈** – `schueler` und `klassen` verbinden
2. **⋈** – das Ergebnis mit `noten` verbinden
3. **σ** – auf `bezeichnung = '10a' AND note < 3` filtern
4. **π** – nur `vorname` und `note` behalten

**Inhaltliche Bedeutung:** Vorname und Note aller Schüler der Klasse 10a, die eine Note besser als 3 erhalten haben.

**SQL:**
```sql
SELECT vorname, note
FROM schueler
JOIN klassen ON schueler.klasse_id    = klassen.klasse_id
JOIN noten   ON schueler.schueler_id  = noten.schueler_id
WHERE bezeichnung = '10a'
  AND note < 3;
```
</details>

---

### Aufgabe 5: Ausdrücke selbst bilden

Formuliere einen Relationenalgebra-Ausdruck für die folgenden Aufgaben. Gib anschließend die SQL-Abfrage an.

**5a)** Alle Produkte, die mehr als 3,00 € kosten, aber noch nie bestellt wurden.

**5b)** Vorname, Nachname und Klassenbezeichnung aller Schülerinnen (Geschlecht = 'w') der Stufe 9.

**5c)** Namen aller Fächer, in denen es mindestens eine Note mit der Note 6 gibt.

**5d)** Schüler-IDs, die sowohl in der Kantine bestellt haben als auch mindestens eine Note haben.

---

<details>
<summary>Lösungen Aufgabe 5</summary>

**5a)**
$$\pi_{\text{produkt\_id}}\bigl(\sigma_{\text{preis} > 3{,}00}(\text{produkte})\bigr) - \pi_{\text{produkt\_id}}(\text{bestellungen})$$

```sql
SELECT produkt_id FROM produkte WHERE preis > 3.00
EXCEPT
SELECT produkt_id FROM bestellungen;
```

**5b)**
$$\pi_{\text{vorname},\, \text{nachname},\, \text{bezeichnung}}\Bigl(\sigma_{\text{geschlecht} = \text{'w'} \,\wedge\, \text{stufe} = 9}\bigl(\text{schueler} \underset{\text{schueler.klasse\_id = klassen.klasse\_id}}{\bowtie} \text{klassen}\bigr)\Bigr)$$

```sql
SELECT vorname, nachname, bezeichnung
FROM schueler
JOIN klassen ON schueler.klasse_id = klassen.klasse_id
WHERE geschlecht = 'w' AND stufe = 9;
```

**5c)**
$$\pi_{\text{faecher.name}}\Bigl(\sigma_{\text{note} = 6}\bigl(\text{noten} \underset{\text{noten.fach\_id = faecher.fach\_id}}{\bowtie} \text{faecher}\bigr)\Bigr)$$

```sql
SELECT DISTINCT faecher.name
FROM noten
JOIN faecher ON noten.fach_id = faecher.fach_id
WHERE note = 6;
```

**5d)**
$$\pi_{\text{schueler\_id}}(\text{bestellungen}) \cap \pi_{\text{schueler\_id}}(\text{noten})$$

```sql
SELECT schueler_id FROM bestellungen
INTERSECT
SELECT schueler_id FROM noten;
```
</details>
