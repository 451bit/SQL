# Kapitel 4: Mehrwertige Attribute und 1:n-Beziehungen mit Optionalität

**Notation:** Chen-Notation  
**Thema:** Mehrwertige Attribute im ER-Diagramm und optionale 1:n-Beziehungen im relationalen Modell

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md) · [Kapitel 7 – DML in SQL](DML.md) · [Projekt – Wetterdatenbank](Projekt_Wetterdatenbank.md) · [Kapitel 8 – Relationenalgebra](Relationenalgebra.md)

---

## Teil A: Mehrwertige Attribute

### 1. Das Problem – ein Attribut, viele Werte

Stell dir vor, du modellierst eine Lehrerdatenbank. Jede Lehrerin und jeder Lehrer hat eine oder mehrere **Telefonnummern** – manche haben nur eine Handynummer, andere haben zusätzlich eine Festnetznummer im Büro.

Dein erster Entwurf:

```
[Lehrer]
  |
lehrer_id (PK)
name
telefonnummer   ← Wie viele Spalten brauchst du hier?
```

**Das Problem:** Eine einzige Spalte `telefonnummer` reicht nicht, wenn ein Lehrer mehrere Nummern haben kann. Du könntest `telefon1`, `telefon2`, `telefon3` anlegen – aber was, wenn jemand vier Nummern hat? Und was, wenn die meisten Lehrer nur eine haben? Dann sind die anderen Spalten meistens leer.

Ein Attribut, das **mehrere Werte gleichzeitig** annehmen kann, heißt **mehrwertiges Attribut**.

---

### 2. Darstellung im ER-Diagramm

In der Chen-Notation werden Attribute als Ovale (Ellipsen) dargestellt. Ein **mehrwertiges Attribut** bekommt ein **doppelt umrandetes Oval** – also eine doppelte Ellipse.

| Element | Darstellung in Chen |
|---|---|
| Normales Attribut | Einfache Ellipse `( )` |
| Primärschlüssel-Attribut | Einfache Ellipse, Attributname unterstrichen |
| Mehrwertiges Attribut | **Doppelte** Ellipse `(( ))` |
| Abgeleitetes Attribut | Gestrichelte Ellipse |

### Beispiel: Lehrer mit Telefonnummern

```
                ((telefonnummer))
                        |
lehrer_id ---- [Lehrer] ---- name
```

Textuell beschrieben:
- `Lehrer` ist die Entität mit dem Primärschlüssel `lehrer_id` und dem normalen Attribut `name`
- `telefonnummer` ist ein **mehrwertiges Attribut** → dargestellt als **doppelte Ellipse**
- Ein Lehrer kann keine, eine oder mehrere Telefonnummern haben

### Weiteres Beispiel: Schüler mit Hobbys

```
                ((hobby))
                    |
schueler_id ---- [Schüler] ---- vorname ---- nachname
```

Ein Schüler kann mehrere Hobbys haben (Fußball, Lesen, Gitarre, …). Das Attribut `hobby` ist daher mehrwertig.

---

### 3. Warum mehrwertige Attribute nicht direkt in eine Tabelle passen

Eine Tabellenspalte enthält in einer **normalisierten** Datenbank genau **einen atomaren Wert** pro Zeile. Mehrere Werte in einer Zelle (z. B. `"Fußball, Lesen, Gitarre"` als ein Text) verletzt die erste Normalform (1NF) und macht spätere Abfragen sehr schwierig.

**Falsch:**

| schueler_id | vorname | hobby |
|---|---|---|
| 1 | Leon | Fußball, Lesen |
| 2 | Emma | Gitarre |

Wie würde man jetzt alle Schüler abfragen, die Fußball spielen? Man müsste mit `LIKE '%Fußball%'` arbeiten – fehleranfällig und langsam.

---

### 4. Umsetzung ins relationale Modell

Ein mehrwertiges Attribut wird in eine **eigene Tabelle** ausgelagert. Diese Tabelle enthält:

1. Den **Fremdschlüssel** auf die ursprüngliche Entität
2. Das **mehrwertige Attribut selbst** als Spalte
3. Oft bilden beide zusammen den **Primärschlüssel** (damit dieselbe Nummer nicht doppelt eingetragen werden kann)

### Beispiel: Lehrer und Telefonnummern

**ER-Diagramm (textuell):**
```
                ((telefonnummer))
                        |
lehrer_id (PK) ---- [Lehrer] ---- name
```

**Relationales Modell:**
```
Lehrer(lehrer_id, name)
Lehrer_Telefon(lehrer_id, telefonnummer)
               ^^^^^^^^^ ^^^^^^^^^^^^^^
               FK→Lehrer  mehrwertiges Attribut
               └──────── gemeinsam: Primärschlüssel ────┘
```

**SQL:**
```sql
CREATE TABLE Lehrer (
    lehrer_id    INTEGER PRIMARY KEY,
    name         TEXT NOT NULL
);

CREATE TABLE Lehrer_Telefon (
    lehrer_id    INTEGER NOT NULL REFERENCES Lehrer(lehrer_id),
    telefonnummer TEXT NOT NULL,
    PRIMARY KEY (lehrer_id, telefonnummer)
);
```

> **Was bedeutet der zusammengesetzte Primärschlüssel hier?**  
> Der Primärschlüssel `(lehrer_id, telefonnummer)` stellt sicher, dass dieselbe Nummer für denselben Lehrer nicht zweimal gespeichert wird. Lehrer 1 und Lehrer 2 können aber dieselbe Nummer haben (was zwar selten sinnvoll ist, aber möglich sein soll).

### Beispiel: Schüler und Hobbys

**Relationales Modell:**
```
Schueler(schueler_id, vorname, nachname)
Schueler_Hobby(schueler_id, hobby)
               ^^^^^^^^^^^  ^^^^^
               FK→Schueler  mehrwertiges Attribut
               └──────── gemeinsam: Primärschlüssel ────┘
```

**SQL:**
```sql
CREATE TABLE Schueler_Hobby (
    schueler_id INTEGER NOT NULL REFERENCES Schueler(schueler_id),
    hobby       TEXT NOT NULL,
    PRIMARY KEY (schueler_id, hobby)
);
```

---

## Teil B: 1:n-Beziehung mit Optionalität an der n-Seite

### 5. Wiederholung: 1:n-Beziehungen im relationalen Modell

In einer **1:n-Beziehung** gehört jede Instanz auf der n-Seite zu **genau einer** Instanz auf der 1-Seite. Die Umsetzung: Der **Primärschlüssel der 1-Seite** wird als **Fremdschlüssel in die n-Tabelle** übernommen.

**Beispiel:** Ein Schüler gehört zu genau einer Klasse. Eine Klasse hat viele Schüler.

```
Klasse (1) ────────── Schüler (n)
```

**Relationales Modell:**
```
Klasse(klasse_id, bezeichnung)
Schueler(schueler_id, vorname, nachname, klasse_id)
                                         ^^^^^^^^
                                         FK→Klasse
```

Hier ist `klasse_id` in `Schueler` der Fremdschlüssel – er zeigt auf die Klasse, zu der der Schüler gehört.

---

### 6. Was bedeutet Optionalität?

Bei einer Beziehung kann man für jede Seite festlegen, ob die Teilnahme **verpflichtend** (obligatorisch) oder **freiwillig** (optional) ist.

In der **Min-Max-Notation** (auch Kardinalitätsnotation genannt) schreibt man `(min, max)` an die jeweilige Seite der Beziehung:

| Notation | Bedeutung |
|---|---|
| `(1, 1)` | Genau eine – verpflichtend und einfach |
| `(0, 1)` | Keine oder eine – optional |
| `(1, n)` | Mindestens eine – verpflichtend, beliebig viele |
| `(0, n)` | Keine oder beliebig viele – optional |

**„Optionalität an der Entität mit Kardinalität n"** bedeutet: Die minimale Teilnahme der n-Seite ist **0** – eine Instanz auf der n-Seite muss **nicht** an der Beziehung teilnehmen.

---

### 7. Bedeutung für das relationale Modell

Bei einer **verpflichtenden** 1:n-Beziehung `(1, n)` an der n-Seite wird der Primärschlüssel der 1-Entität als `NOT NULL`-Fremdschlüssel in die n-Tabelle eingefügt – jede Zeile muss einer 1-Seite zugeordnet sein.

Bei einer **optionalen** 1:n-Beziehung `(0, n)` an der n-Seite könnte man denselben FK nullable lassen. Das hat aber einen Nachteil: **Viele Einträge in der n-Tabelle hätten dann `NULL` in dieser Spalte** – also Schüler, die keine AG haben, tragen trotzdem eine leere Spalte mit sich.

Die bessere Lösung: Die Beziehung wird als **eigene Tabelle** umgesetzt – ähnlich wie bei einer n:m-Beziehung.

Diese Beziehungstabelle enthält:
- Den **Primärschlüssel der 1-Entität** als Fremdschlüssel
- Den **Primärschlüssel der n-Entität** als Fremdschlüssel

Den **Primärschlüssel der Beziehungstabelle** bildet dabei **nur der FK der n-Entität** – denn da es eine 1:n-Beziehung ist, kann jede n-Instanz höchstens einer 1-Instanz zugeordnet sein. Ein Schüler kann in maximal einer AG sein, also identifiziert die `schueler_id` eine Zeile in der Beziehungstabelle eindeutig.

| Situation | Umsetzung |
|---|---|
| Verpflichtend `(1, n)` | FK in die n-Tabelle, `NOT NULL` |
| Optional `(0, n)` | Eigene Beziehungstabelle; PK = FK der n-Entität |

In der Beziehungstabelle erscheinen **nur die n-Instanzen, die tatsächlich an der Beziehung teilnehmen** – n-Instanzen ohne Zuordnung fehlen einfach, ohne dass eine `NULL`-Spalte nötig ist.

---

### 8. Konkretes Beispiel: Schüler und Arbeitsgemeinschaft (AG)

Jede Schule bietet freiwillige **Arbeitsgemeinschaften** (AGs) an – z. B. Theater, Robotik, Schach. Ein Schüler **kann** an einer AG teilnehmen, **muss** es aber nicht. Eine AG hat viele Schüler.

**ER-Diagramm:**
```
[AG] ─(1,1)─────(0,n)─ [Schüler]
```

- Ein Schüler nimmt an **0 oder einer** AG teil → optional an der n-Seite
- Eine AG hat **1 bis n** Schüler

**Vergleich: Schüler und Klasse vs. Schüler und AG**

```
[Klasse] ─(1,1)──(1,n)─ [Schüler]     ← verpflichtend: jeder Schüler MUSS in einer Klasse sein
[AG]     ─(1,1)──(0,n)─ [Schüler]     ← optional: ein Schüler KANN in einer AG sein
```

**Würde man den FK in die Schüler-Tabelle einfügen**, hätten alle Schüler ohne AG eine leere `ag_id`-Spalte (`NULL`). Bei hunderten Schülern, von denen nur wenige eine AG haben, entstehen viele überflüssige NULL-Einträge.

**Lösung: eigene Beziehungstabelle** – nur Schüler, die tatsächlich einer AG zugeordnet sind, bekommen einen Eintrag.

**Relationales Modell:**

```
AG(ag_id, name, raum)
Schueler(schueler_id, vorname, nachname, klasse_id)
                                         ^^^^^^^^^
                                         FK→Klasse, NOT NULL

Schueler_AG(schueler_id, ag_id)
            ^^^^^^^^^^^  ^^^^^
            PK + FK→Schueler  FK→AG
```

- `schueler_id` ist der alleinige **Primärschlüssel** der Beziehungstabelle: Da es 1:n ist, kann jeder Schüler höchstens einer AG angehören – die `schueler_id` identifiziert die Zeile eindeutig.
- `ag_id` ist nur Fremdschlüssel – mehrere Schüler können dieselbe AG haben.

**SQL:**
```sql
CREATE TABLE AG (
    ag_id INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    raum  TEXT
);

CREATE TABLE Schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL,
    klasse_id   INTEGER NOT NULL REFERENCES Klasse(klasse_id)  -- verpflichtend
);

CREATE TABLE Schueler_AG (
    schueler_id INTEGER PRIMARY KEY REFERENCES Schueler(schueler_id),  -- PK + FK
    ag_id       INTEGER NOT NULL REFERENCES AG(ag_id)                  -- FK
);
```

> **Warum ist `schueler_id` der alleinige PK?**  
> Bei einer n:m-Beziehung wäre der PK zusammengesetzt aus beiden FKs – weil ein Schüler in mehreren AGs sein könnte. Hier ist es aber 1:n: Ein Schüler gehört zu **höchstens einer** AG. Deshalb reicht `schueler_id` allein als PK – es kann nie zwei Zeilen mit derselben `schueler_id` geben.

---

### 9. Daten abfragen mit der Beziehungstabelle

Durch die eigene Beziehungstabelle ergibt sich eine klare Abfragelogik:

```sql
-- Alle Schüler MIT ihrer AG (nur Schüler mit Eintrag in Schueler_AG)
SELECT s.vorname, s.nachname, a.name AS ag_name
FROM Schueler s
JOIN Schueler_AG sa ON s.schueler_id = sa.schueler_id
JOIN AG a ON sa.ag_id = a.ag_id;

-- Alle Schüler, auch ohne AG (NULL bei Schülern ohne AG-Eintrag)
SELECT s.vorname, s.nachname, a.name AS ag_name
FROM Schueler s
LEFT JOIN Schueler_AG sa ON s.schueler_id = sa.schueler_id
LEFT JOIN AG a ON sa.ag_id = a.ag_id;
```

> **Merke:** Mit `INNER JOIN` erscheinen nur Schüler, die einer AG zugeordnet sind. Mit `LEFT JOIN` erscheinen alle Schüler – Schüler ohne AG-Eintrag haben `NULL` in den AG-Spalten.

---

## 10. Übungsaufgaben

### Aufgabe 1 – Sprachen eines Schülers (mehrwertiges Attribut)

Ein Schüler kann mehrere **Fremdsprachen** sprechen (Englisch, Französisch, Spanisch, …). Das Attribut `sprache` soll im ER-Diagramm modelliert werden.

**a)** Warum ist `sprache` ein mehrwertiges Attribut? Erkläre kurz.

**b)** Zeichne das ER-Diagramm in Chen-Notation. Verwende die korrekte Darstellung für mehrwertige Attribute.

**c)** Übertrage das Diagramm ins relationale Modell. Gib Primär- und Fremdschlüssel an.

**d)** Schreibe die SQL-`CREATE TABLE`-Anweisungen für beide Tabellen.

<details>
<summary>Lösung</summary>

**a)** Ein Schüler kann mehr als eine Fremdsprache sprechen. Das Attribut `sprache` kann also mehrere Werte gleichzeitig haben – es ist nicht atomar. Deshalb ist es ein mehrwertiges Attribut.

**b)** ER-Diagramm (textuell):
```
            ((sprache))
                 |
schueler_id ---- [Schüler] ---- vorname ---- nachname
(PK, unterstrichen)
```

**c)** Relationales Modell:
```
Schueler(schueler_id, vorname, nachname)
Schueler_Sprache(schueler_id, sprache)
                 ^^^^^^^^^^^  ^^^^^^^
                 FK→Schueler  mehrwertiges Attribut
                 └──── gemeinsam: Primärschlüssel ────┘
```

**d)** SQL:
```sql
CREATE TABLE Schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL
);

CREATE TABLE Schueler_Sprache (
    schueler_id INTEGER NOT NULL REFERENCES Schueler(schueler_id),
    sprache     TEXT NOT NULL,
    PRIMARY KEY (schueler_id, sprache)
);
```
</details>

---

### Aufgabe 2 – Produkt mit Allergenen (mehrwertiges Attribut)

Ein Kantinenprodukt kann mehrere **Allergene** enthalten (Gluten, Laktose, Nüsse, …).

**a)** Modelliere das ER-Diagramm für `Produkt` mit dem mehrwertigen Attribut `allergen`. Das Produkt hat außerdem `produkt_id` (PK), `name` und `preis`.

**b)** Erstelle das relationale Modell.

**c)** Schreibe die SQL-Anweisungen.

<details>
<summary>Lösung</summary>

**a)** ER-Diagramm:
```
                    ((allergen))
                         |
produkt_id (PK) ---- [Produkt] ---- name ---- preis
```

**b)** Relationales Modell:
```
Produkt(produkt_id, name, preis)
Produkt_Allergen(produkt_id, allergen)
                 ^^^^^^^^^^  ^^^^^^^^
                 FK→Produkt  mehrwertiges Attribut
                 └──── gemeinsam: Primärschlüssel ────┘
```

**c)** SQL:
```sql
CREATE TABLE Produkt (
    produkt_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    preis      REAL NOT NULL
);

CREATE TABLE Produkt_Allergen (
    produkt_id INTEGER NOT NULL REFERENCES Produkt(produkt_id),
    allergen   TEXT NOT NULL,
    PRIMARY KEY (produkt_id, allergen)
);
```
</details>

---

### Aufgabe 3 – Nachhilfelehrer (1:n mit Optionalität)

Ein Schüler kann freiwillig einen **Nachhilfelehrer** annehmen, muss es aber nicht. Jeder Nachhilfelehrer kann mehrere Schüler betreuen.

**a)** Handelt es sich um eine verpflichtende oder optionale Teilnahme an der n-Seite? Begründe.

**b)** Wie unterscheidet sich das SQL-Schema von einer verpflichtenden Beziehung?

**c)** Schreibe das relationale Modell und die SQL-Anweisungen für `Nachhilfelehrer` und `Schueler`.

<details>
<summary>Lösung</summary>

**a)** Optional – ein Schüler KANN einen Nachhilfelehrer haben, muss es aber nicht. Die minimale Kardinalität auf der n-Seite ist 0: `(0, n)`.

**b)** Bei einer verpflichtenden Beziehung wird der FK direkt in die n-Tabelle eingefügt (`NOT NULL`). Bei einer optionalen Beziehung verwendet man eine **eigene Beziehungstabelle**, um NULL-Werte in der Schüler-Tabelle zu vermeiden. Der Primärschlüssel der Beziehungstabelle ist nur die `schueler_id` (1:n → jeder Schüler hat höchstens einen Nachhilfelehrer).

**c)** Relationales Modell:
```
Nachhilfelehrer(nl_id, vorname, nachname, fach)
Schueler(schueler_id, vorname, nachname, klasse_id)

Schueler_Nachhilfe(schueler_id, nl_id)
                   ^^^^^^^^^^^  ^^^^^
                   PK + FK→Schueler  FK→Nachhilfelehrer
```

SQL:
```sql
CREATE TABLE Nachhilfelehrer (
    nl_id    INTEGER PRIMARY KEY,
    vorname  TEXT NOT NULL,
    nachname TEXT NOT NULL,
    fach     TEXT
);

CREATE TABLE Schueler (
    schueler_id INTEGER PRIMARY KEY,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL,
    klasse_id   INTEGER NOT NULL REFERENCES Klasse(klasse_id)
);

CREATE TABLE Schueler_Nachhilfe (
    schueler_id INTEGER PRIMARY KEY REFERENCES Schueler(schueler_id),
    nl_id       INTEGER NOT NULL REFERENCES Nachhilfelehrer(nl_id)
);
```
</details>

---

### Aufgabe 4 – Vergleich: optional vs. verpflichtend

Gegeben sind zwei Beziehungen in einer Schulverwaltung:

- Ein Schüler **muss** einer Klasse zugeordnet sein (verpflichtend)
- Ein Schüler **kann** an einer Projektwoche teilnehmen (optional)

**a)** Zeichne beide Beziehungen im ER-Diagramm (textuell) mit Min-Max-Notation.

**b)** Schreibe für beide Beziehungen das relationale Modell. Erkläre den entscheidenden Unterschied in der Umsetzung.

**c)** Erkläre: Warum setzt man die optionale Beziehung als eigene Tabelle um – und nicht einfach mit einem nullable Fremdschlüssel in der Schüler-Tabelle?

**d)** Warum ist `schueler_id` der alleinige PK der Beziehungstabelle – und nicht ein zusammengesetzter PK aus `schueler_id` und `pw_id`?

<details>
<summary>Lösung</summary>

**a)** ER-Diagramm:
```
[Klasse]      ─(1,1)──(1,n)─ [Schüler]     ← verpflichtend an der n-Seite
[Projektwoche] ─(1,1)──(0,n)─ [Schüler]    ← optional an der n-Seite
```

**b)** Relationales Modell:
```
Klasse(klasse_id, bezeichnung)
Projektwoche(pw_id, thema, jahr)

Schueler(schueler_id, vorname, nachname, klasse_id)
                                         ^^^^^^^^^
                                         FK→Klasse, NOT NULL  ← direkt in der Tabelle

Schueler_Projektwoche(schueler_id, pw_id)
                      ^^^^^^^^^^^  ^^^^^
                      PK + FK→Schueler  FK→Projektwoche  ← eigene Beziehungstabelle
```

Unterschied: Die verpflichtende Beziehung (Klasse) wird als `NOT NULL`-FK direkt in `Schueler` eingetragen. Die optionale Beziehung (Projektwoche) bekommt eine eigene Tabelle.

**c)** Mit einem nullable FK hätten alle Schüler ohne Projektwoche einen `NULL`-Eintrag in der Spalte `pw_id` – das sind unnötige Leerstellen in der Tabelle. Die Beziehungstabelle enthält dagegen nur Schüler, die tatsächlich an einer Projektwoche teilnehmen. Schüler ohne Projektwoche haben schlicht keinen Eintrag in `Schueler_Projektwoche`.

**d)** Es handelt sich um eine 1:n-Beziehung: Ein Schüler kann an **höchstens einer** Projektwoche teilnehmen. Daher identifiziert `schueler_id` jede Zeile in der Beziehungstabelle eindeutig – sie ist der alleinige PK. Bei einer n:m-Beziehung (Schüler in mehreren Projektwochen möglich) wäre der PK zusammengesetzt aus `(schueler_id, pw_id)`.
</details>
