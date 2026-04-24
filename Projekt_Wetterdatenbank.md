# Projekt: Wetterdatenbank mit Python und SQLite

**Thema:** Python + SQLite + GUI (tkinter)  
**Niveau:** Einstieg in die Datenbankprogrammierung

> **Kursübersicht:**  
> [Kapitel 1 – Aggregatfunktionen](README.md) · [Kapitel 2 – Verschachtelte Abfragen](Verschachteltes_SQL.md) · [Kapitel 3 – Schwache Entitäten](Schwache_Entitaeten.md) · [Kapitel 4 – Mehrwertige Attribute & 1:n mit Optionalität](Mehrwertige_Attribute.md) · [Kapitel 5 – Generalisierung](Generalisierung.md) · [Kapitel 6 – DDL in SQL](DDL.md) · [Kapitel 7 – DML in SQL](DML.md) · [Projekt – Wetterdatenbank](Projekt_Wetterdatenbank.md)

---

## Überblick

In diesem Projekt baust du eine vollständige Anwendung, die:
- eine **SQLite-Datenbank** lokal auf deinem Rechner speichert,
- eine **grafische Oberfläche** (GUI) mit tkinter hat,
- Daten aus **Eingabefeldern** und **CSV-Dateien** in die Datenbank schreibt,
- Daten aus der Datenbank **anzeigt** und **auswertet**.

Das Thema: eine **Wetterdatenbank** mit Messstationen, Orten und Tages­messungen (Temperatur, Niederschlag, Luftfeuchtigkeit, Wind).

---

## Lernziele

Nach diesem Projekt kannst du:
- eine SQLite-Datenbank aus Python heraus erstellen und befüllen
- GUI-Eingabefelder auslesen und Daten speichern
- CSV-Dateien importieren
- Daten aus einer Datenbank in einer Tabelle anzeigen
- einfache statistische Auswertungen mit SQL-Aggregatfunktionen durchführen

---

## Projektdateien

| Datei | Inhalt |
|---|---|
| [wetter_vorlage.py](wetter_vorlage.py) | GUI-Vorlage mit `pass`-Platzhaltern – hier arbeitest du |
| [daten_generieren.py](daten_generieren.py) | Erzeugt Beispieldaten als CSV-Dateien |
| `wetterdaten.db` | Wird zur Laufzeit erstellt (SQLite-Datenbankdatei) |
| `messstationen.csv` | Wird von `daten_generieren.py` erzeugt |
| `messungen.csv` | Wird von `daten_generieren.py` erzeugt |

---

## Das Datenbankschema

Die Wetterdatenbank hat drei Tabellen:

```
orte(ort_id, name, bundesland, hoehe_m)

messstationen(station_id, name, ort_id, breitengrad, laengengrad)
                                ^^^^^^
                                FK → orte

messungen(messung_id, station_id, datum, uhrzeit,
          temperatur_c, niederschlag_mm,
          luftfeuchtigkeit_pct, windgeschwindigkeit_kmh)
                    ^^^^^^^^^^
                    FK → messstationen
```

**ER-Diagramm (textuell):**
```
[Ort] ─(1,1)──(1,n)─ [Messstation] ─(1,1)──(1,n)─ [Messung]
```

- Ein Ort hat mehrere Messstationen.
- Eine Messstation hat viele Messungen.
- Eine Messung gehört zu genau einer Messstation.

---

## Teil 1: tkinter – Grundlagen der GUI-Programmierung

### 1.1 Was ist tkinter?

**tkinter** ist Pythons eingebaute Bibliothek für grafische Oberflächen. Sie ist in jeder Python-Installation bereits enthalten – du brauchst nichts zu installieren.

Ein tkinter-Programm hat immer diese Grundstruktur:

```python
import tkinter as tk

fenster = tk.Tk()           # Hauptfenster erstellen
fenster.title("Mein Fenster")
fenster.geometry("400x300") # Breite x Höhe in Pixeln

# ... Inhalt des Fensters ...

fenster.mainloop()          # Ereignisschleife starten (Fenster offen halten)
```

> **`mainloop()`** ist die sogenannte Ereignisschleife. Sie wartet auf Benutzereingaben (Klicks, Tastatureingaben) und reagiert darauf. Das Programm läuft so lange, bis das Fenster geschlossen wird.

---

### 1.2 Widgets – die Bausteine der GUI

Alles, was du in einem Fenster siehst, ist ein **Widget**: ein Label, ein Button, ein Eingabefeld, eine Tabelle.

Die wichtigsten Widgets:

| Widget | Klasse | Wozu? |
|---|---|---|
| Beschriftung | `ttk.Label` | Text anzeigen |
| Schaltfläche | `ttk.Button` | Klick-Aktionen auslösen |
| Eingabefeld | `ttk.Entry` | Einzeiligen Text eingeben |
| Mehrzeiliges Feld | `tk.Text` | Mehrzeiligen Text anzeigen/eingeben |
| Dropdown | `ttk.Combobox` | Aus einer Liste auswählen |
| Tabs | `ttk.Notebook` | Mehrere Seiten mit Reitern |
| Tabelle | `ttk.Treeview` | Daten tabellarisch anzeigen |
| Fortschrittsbalken | `ttk.Progressbar` | Fortschritt visualisieren |

> **`ttk` vs. `tk`:** `ttk` (themed tkinter) sind modernere, besser aussehende Varianten der Widgets. Verwende immer `ttk`, außer es gibt keine `ttk`-Version (z. B. `tk.Text`, `tk.Label` für einfache Fälle).

**Minimales Beispiel:**

```python
import tkinter as tk
from tkinter import ttk

fenster = tk.Tk()
fenster.title("Beispiel")

ttk.Label(fenster, text="Dein Name:").pack()

eingabe = ttk.Entry(fenster, width=25)
eingabe.pack()

def klick():
    name = eingabe.get()
    ergebnis.config(text=f"Hallo, {name}!")

ttk.Button(fenster, text="Begrüßen", command=klick).pack()

ergebnis = ttk.Label(fenster, text="")
ergebnis.pack()

fenster.mainloop()
```

> **Probiere das aus!** Führe diesen Code aus und beobachte, was passiert, wenn du einen Namen eingibst und den Button klickst.

---

### 1.3 Layout: `pack` und `grid`

Widgets werden nicht automatisch platziert – du musst angeben, wie sie angeordnet werden sollen. Es gibt zwei Hauptmethoden:

#### `pack` – einfach, für einfache Layouts

Widgets werden nacheinander gestapelt (standard: von oben nach unten).

```python
ttk.Label(fenster, text="Zeile 1").pack()
ttk.Label(fenster, text="Zeile 2").pack()
ttk.Label(fenster, text="Links").pack(side="left")
ttk.Label(fenster, text="Rechts").pack(side="right")
```

Wichtige Parameter:
- `side="top"` / `"bottom"` / `"left"` / `"right"` – Ausrichtung
- `fill="x"` / `"y"` / `"both"` – Dehnung
- `expand=True` – nutzt verfügbaren Platz
- `padx=10, pady=5` – Abstand außen

#### `grid` – für Formular-Layouts (Zeilen und Spalten)

```python
ttk.Label(fenster, text="Name:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
ttk.Entry(fenster).grid(row=0, column=1, padx=10, pady=5)

ttk.Label(fenster, text="Alter:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
ttk.Entry(fenster).grid(row=1, column=1, padx=10, pady=5)
```

Wichtige Parameter:
- `row=`, `column=` – Position in der Raster-Tabelle
- `sticky="e"` – Ausrichtung innerhalb der Zelle (`n`, `s`, `e`, `w` oder Kombinationen)
- `columnspan=2` – Widget überspannt mehrere Spalten

> **Wichtige Regel:** In einem Frame (Rahmen) darf man nicht `pack` und `grid` mischen! Entweder alle Widgets in einem Frame mit `pack` oder alle mit `grid` – sonst friert das Fenster ein.

---

### 1.4 Ereignisse und Funktionen (Events)

Der wichtigste Parameter für Buttons ist `command=`. Hier gibst du eine Funktion an, die beim Klick aufgerufen wird.

```python
def mein_klick():
    print("Geklickt!")

# Funktion ohne Klammern übergeben! (Nur den Namen, nicht den Aufruf)
ttk.Button(fenster, text="Klick mich", command=mein_klick).pack()
```

Wenn die Methode in einer Klasse ist (wie in der Vorlage), schreibt man `command=self.meine_methode`.

**Typisches Muster:** Eingabe lesen → Verarbeiten → Ergebnis anzeigen:

```python
def speichern():
    name = self.eingabe_name.get()          # Text aus Entry lesen
    if not name:                            # Leere Eingabe prüfen
        messagebox.showwarning("Fehler", "Name darf nicht leer sein!")
        return
    # ... in Datenbank speichern ...
    self.lbl_status.config(text="Gespeichert!")
```

---

### 1.5 Tabs mit `ttk.Notebook`

Ein `Notebook` ist ein Widget mit mehreren Seiten (Tabs), zwischen denen der Nutzer wechseln kann.

```python
notebook = ttk.Notebook(fenster)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Erster Tab")
notebook.add(tab2, text="Zweiter Tab")

# Inhalt in Tab 1 einfügen:
ttk.Label(tab1, text="Inhalt von Tab 1").pack(pady=20)
```

---

### 1.6 Dialoge: `messagebox` und `filedialog`

#### Meldungen anzeigen

```python
from tkinter import messagebox

messagebox.showinfo("Erfolg", "Daten wurden gespeichert!")
messagebox.showwarning("Warnung", "Feld darf nicht leer sein!")
messagebox.showerror("Fehler", "Datenbankverbindung fehlgeschlagen!")

# Ja/Nein-Frage:
antwort = messagebox.askyesno("Bestätigen", "Wirklich löschen?")
if antwort:   # True bei Ja, False bei Nein
    ...
```

#### Datei auswählen

```python
from tkinter import filedialog

# Datei öffnen (gibt den Pfad als String zurück, oder "" wenn abgebrochen)
pfad = filedialog.askopenfilename(
    title="CSV-Datei auswählen",
    filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
)

if pfad:   # Prüfen ob eine Datei gewählt wurde (nicht abgebrochen)
    print(f"Gewählte Datei: {pfad}")

# Datei speichern:
pfad = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=[("CSV-Dateien", "*.csv")]
)
```

---

### 1.7 Treeview – Tabellen anzeigen

`ttk.Treeview` ist das Widget für tabellarische Daten. Es braucht etwas mehr Konfiguration:

```python
# 1. Spalten definieren
spalten = ("ID", "Name", "Wert")

tabelle = ttk.Treeview(fenster, columns=spalten, show="headings")

# 2. Spaltenköpfe und Breiten setzen
tabelle.heading("ID",   text="ID")
tabelle.heading("Name", text="Name")
tabelle.heading("Wert", text="Messwert")

tabelle.column("ID",   width=50,  anchor="center")
tabelle.column("Name", width=200)
tabelle.column("Wert", width=100, anchor="center")

tabelle.pack(fill="both", expand=True)

# 3. Zeile hinzufügen
tabelle.insert("", "end", values=(1, "München", 12.5))
tabelle.insert("", "end", values=(2, "Hamburg",  9.3))

# 4. Alle Zeilen löschen (z. B. vor dem Neu-Laden)
tabelle.delete(*tabelle.get_children())
```

**Scrollbar hinzufügen:**

```python
scrollbar = ttk.Scrollbar(fenster, orient="vertical", command=tabelle.yview)
tabelle.configure(yscrollcommand=scrollbar.set)
tabelle.pack(side="left",  fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
```

---

### 1.8 StringVar und Combobox

Eine `Combobox` ist ein Dropdown-Menü. Sie braucht eine `StringVar`, die den aktuell gewählten Wert speichert:

```python
auswahl_var = tk.StringVar()

combo = ttk.Combobox(fenster, textvariable=auswahl_var, state="readonly")
combo["values"] = ["München", "Hamburg", "Berlin"]
combo.pack()

def klick():
    gewaehlter_wert = auswahl_var.get()
    print(f"Gewählt: {gewaehlter_wert}")
```

---

## Teil 2: sqlite3 – Datenbankzugriff in Python

Das Modul `sqlite3` ist in Python eingebaut. Es stellt eine Verbindung zu einer SQLite-Datenbankdatei her und ermöglicht das Ausführen von SQL-Befehlen.

### 2.1 Verbindung herstellen

```python
import sqlite3

# Verbindung zur Datei herstellen (Datei wird erstellt, falls nicht vorhanden)
verbindung = sqlite3.connect("meine_datenbank.db")

# row_factory: Ergebniszeilen als dict-ähnliche Objekte (Zugriff per Spaltenname)
verbindung.row_factory = sqlite3.Row

# Cursor: der "Ausführer" von SQL-Befehlen
cursor = verbindung.cursor()

# Am Ende immer schließen!
verbindung.close()
```

> **`sqlite3.Row`:** Ohne `row_factory` bekommst du Tupel: `zeile[0]`, `zeile[1]` … Mit `row_factory = sqlite3.Row` kannst du Spalten beim Namen nennen: `zeile["name"]`, `zeile["temperatur_c"]`. Das macht den Code lesbarer.

---

### 2.2 Tabellen erstellen (`CREATE TABLE`)

```python
verbindung = sqlite3.connect("test.db")
cursor = verbindung.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS personen (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL,
        alter INTEGER
    )
""")

verbindung.commit()   # Änderungen speichern!
verbindung.close()
```

> **`commit()`** speichert alle Änderungen dauerhaft. Ohne `commit()` gehen Einfügungen und Änderungen verloren, wenn die Verbindung geschlossen wird.

Für mehrere SQL-Befehle auf einmal: `executescript()` (enthält automatisch ein `commit`):

```python
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS a (...);
    CREATE TABLE IF NOT EXISTS b (...);
""")
```

---

### 2.3 Daten einfügen (`INSERT`)

```python
verbindung = sqlite3.connect("test.db")
cursor = verbindung.cursor()

# Einzelne Zeile einfügen – NIEMALS f-Strings für Werte verwenden!
# (Sicherheitslücke: SQL-Injection)
cursor.execute(
    "INSERT INTO personen (name, alter) VALUES (?, ?)",
    ("Lisa", 17)   # Werte als Tupel – die ? werden sicher ersetzt
)

verbindung.commit()
verbindung.close()
```

> **Warum `?` statt f-String?**  
> `f"INSERT INTO personen VALUES ('{name}')"` ist gefährlich, wenn `name` z. B. `'; DROP TABLE personen; --` enthält. Die `?`-Platzhalter (parametrisierte Abfragen) schützen automatisch davor – der Wert wird nie als SQL interpretiert.

**Mehrere Zeilen auf einmal einfügen:**

```python
daten = [("Max", 15), ("Emma", 16), ("Leon", 17)]
cursor.executemany("INSERT INTO personen (name, alter) VALUES (?, ?)", daten)
verbindung.commit()
```

---

### 2.4 Daten lesen (`SELECT`)

```python
verbindung = sqlite3.connect("test.db")
verbindung.row_factory = sqlite3.Row
cursor = verbindung.cursor()

# Alle Zeilen abfragen
cursor.execute("SELECT * FROM personen")
alle_personen = cursor.fetchall()   # Liste aller Zeilen

for person in alle_personen:
    print(person["name"], person["alter"])

# Nur eine Zeile
cursor.execute("SELECT * FROM personen WHERE id = ?", (1,))
eine_person = cursor.fetchone()   # Einzelne Zeile (oder None)

# Mit Bedingung und Parameter
cursor.execute("SELECT * FROM personen WHERE alter > ?", (16,))
ergebnis = cursor.fetchall()

verbindung.close()
```

---

### 2.5 Daten ändern und löschen

```python
# UPDATE
cursor.execute(
    "UPDATE personen SET alter = ? WHERE name = ?",
    (18, "Lisa")
)

# DELETE
cursor.execute("DELETE FROM personen WHERE id = ?", (3,))

verbindung.commit()
```

---

### 2.6 Fehlerbehandlung

Datenbankoperationen können scheitern (Datei nicht vorhanden, Constraint verletzt, …). Verwende immer `try/except`:

```python
try:
    verbindung = sqlite3.connect("test.db")
    cursor = verbindung.cursor()
    cursor.execute("INSERT INTO personen (name) VALUES (?)", ("Max",))
    verbindung.commit()
except sqlite3.Error as fehler:
    print(f"Datenbankfehler: {fehler}")
    verbindung.rollback()   # Änderungen zurücknehmen
finally:
    verbindung.close()      # Verbindung immer schließen
```

In der GUI-Anwendung gibt man Fehler an den Benutzer weiter:

```python
except sqlite3.Error as fehler:
    messagebox.showerror("Datenbankfehler", str(fehler))
```

---

## Teil 3: Die Vorlage verstehen

Öffne [wetter_vorlage.py](wetter_vorlage.py) und lies sie durch. Hier sind die wichtigsten Punkte erklärt:

### Klassenstruktur

```
WetterApp(tk.Tk)
├── __init__()             → Fenster einrichten, GUI aufbauen
├── _gui_aufbauen()        → Notebook + Tabs erstellen
│
├── _aufbau_tab_db()       → Tab 1 aufbauen
├── _klick_db_erstellen()  → Button-Handler Tab 1 [FERTIG]
│
├── _aufbau_tab_station()  → Tab 2 aufbauen
├── _klick_station_speichern()  → [TODO: Aufgabe 2]
│
├── _aufbau_tab_messung()  → Tab 3 aufbauen
├── _stationen_laden()     → [TODO: Aufgabe 4a]
├── _klick_messung_speichern()  → [TODO: Aufgabe 4b]
│
├── _aufbau_tab_csv()      → Tab 4 aufbauen
├── _klick_csv_importieren()  → [TODO: Aufgabe 3]
│
├── _aufbau_tab_anzeige()  → Tab 5 aufbauen
├── _klick_messungen_laden()  → [TODO: Aufgabe 5]
│
├── _aufbau_tab_auswertung()  → Tab 6 aufbauen
├── _auswertung_stationen_laden()  → [TODO: Aufgabe 6a]
└── _klick_auswerten()     → [TODO: Aufgabe 6b]
```

### Die Formularfelder (Entry-Widgets)

In Tab 2 wird das Formular so aufgebaut, dass alle Entry-Widgets in einem Dictionary gespeichert werden:

```python
self.station_eingaben = {}
self.station_eingaben["name"]       = ttk.Entry(f, width=34)
self.station_eingaben["ort"]        = ttk.Entry(f, width=34)
self.station_eingaben["bundesland"] = ttk.Entry(f, width=34)
# usw.
```

Um einen Wert zu lesen:
```python
name = self.station_eingaben["name"].get().strip()
```

### Der vollständige Tab 1 als Muster

`_klick_db_erstellen()` ist bereits fertig implementiert. Schau dir an, wie:
1. eine Funktion außerhalb der Klasse aufgerufen wird (`db_erstellen()`)
2. ein Label-Text geändert wird (`.config(text=...)`)
3. Fehler abgefangen und als Dialog angezeigt werden

Dieses Muster verwendest du in allen anderen Aufgaben.

---

## Teil 4: Vorbereitung – Beispieldaten erzeugen

Bevor du mit den Aufgaben anfängst, erzeuge die CSV-Beispieldaten:

```
python daten_generieren.py
```

Danach solltest du zwei Dateien im gleichen Ordner haben:
- `messstationen.csv` – 5 Stationen
- `messungen.csv` – 1825 Messungen (5 Stationen × 365 Tage)

Schaue in die Dateien (z. B. mit einem Texteditor), um das Format zu verstehen.

---

## Aufgabe 1: Datenbank auf Knopfdruck erstellen

### Ziel

Der Tab „Datenbank" ist bereits fertig implementiert. Deine Aufgabe ist es, den Code zu **verstehen** und das Ergebnis zu testen.

### Schritte

1. Starte die Anwendung:
   ```
   python wetter_vorlage.py
   ```
2. Wechsle zum Tab **„Datenbank"**.
3. Klicke auf **„Datenbank erstellen / Tabellen prüfen"**.
4. Prüfe: Wurde die Datei `wetterdaten.db` im selben Ordner erstellt?
5. Öffne `wetterdaten.db` mit **DB Browser for SQLite** und kontrolliere die drei Tabellen.

### Verständnisfragen

**a)** Warum schlägt ein erneuter Klick auf den Button nicht fehl, obwohl die Datei schon existiert?

**b)** Wozu dient `verbindung.row_factory = sqlite3.Row`?

**c)** Warum wird `verbindung.commit()` aufgerufen?

**d)** Was passiert, wenn du `executescript()` durch `execute()` ersetzt?

<details>
<summary>Antworten</summary>

**a)** Weil alle `CREATE TABLE`-Befehle `IF NOT EXISTS` enthalten. Existierende Tabellen werden einfach übersprungen.

**b)** Damit Ergebniszeilen per Spaltenname angesprochen werden können (`zeile["name"]` statt `zeile[0]`).

**c)** Damit alle Änderungen dauerhaft in die Datei geschrieben werden. Ohne `commit()` gingen sie beim Schließen verloren.

**d)** `execute()` führt nur einen einzigen SQL-Befehl aus. Für mehrere Befehle (durch `;` getrennt) braucht man `executescript()`.
</details>

---

## Aufgabe 2: Messstation über Formular speichern

### Ziel

Implementiere `_klick_station_speichern()` in [wetter_vorlage.py](wetter_vorlage.py), sodass eine neue Messstation aus dem Formular in die Datenbank gespeichert wird.

### Hintergrund: Zwei Tabellen befüllen

Eine Station gehört zu einem Ort. Das Schema sieht vor:
- Erst den **Ort** in `orte` einfügen (oder nachschlagen, falls er schon existiert)
- Dann die **Station** in `messstationen` einfügen, mit dem `ort_id` als Fremdschlüssel

### Schritt-für-Schritt-Anleitung

**Schritt 1:** Werte aus den Eingabefeldern lesen

```python
name       = self.station_eingaben["name"].get().strip()
ort        = self.station_eingaben["ort"].get().strip()
bundesland = self.station_eingaben["bundesland"].get().strip()
hoehe      = self.station_eingaben["hoehe"].get().strip()
breite     = self.station_eingaben["breitengrad"].get().strip()
laenge     = self.station_eingaben["laengengrad"].get().strip()
```

**Schritt 2:** Pflichtfelder prüfen

```python
if not name or not ort or not bundesland:
    messagebox.showwarning("Eingabe fehlt", "Name, Ort und Bundesland sind Pflichtfelder!")
    return
```

**Schritt 3:** Optionale Zahlenfelder konvertieren

```python
# Felder können leer sein → None wenn leer, sonst float/int
hoehe_wert  = int(hoehe)     if hoehe  else None
breite_wert = float(breite)  if breite else None
laenge_wert = float(laenge)  if laenge else None
```

**Schritt 4:** Ort in `orte` einfügen (oder bereits vorhandenen `ort_id` holen)

```python
verbindung = db_verbinden()
cursor = verbindung.cursor()

# Prüfen ob Ort schon existiert
cursor.execute("SELECT ort_id FROM orte WHERE name = ? AND bundesland = ?",
               (ort, bundesland))
zeile = cursor.fetchone()

if zeile:
    ort_id = zeile["ort_id"]
else:
    cursor.execute(
        "INSERT INTO orte (name, bundesland, hoehe_m) VALUES (?, ?, ?)",
        (ort, bundesland, hoehe_wert)
    )
    ort_id = cursor.lastrowid   # ← ID der gerade eingefügten Zeile
```

> `cursor.lastrowid` gibt die automatisch vergebene ID der zuletzt eingefügten Zeile zurück.

**Schritt 5:** Station einfügen

```python
cursor.execute(
    """INSERT INTO messstationen (name, ort_id, breitengrad, laengengrad)
       VALUES (?, ?, ?, ?)""",
    (name, ort_id, breite_wert, laenge_wert)
)
verbindung.commit()
verbindung.close()
```

**Schritt 6:** Statusmeldung und Felder leeren

```python
self.lbl_station_status.config(
    text=f"Station '{name}' gespeichert.", foreground="green"
)
# Felder leeren:
for eingabe in self.station_eingaben.values():
    eingabe.delete(0, "end")
```

**Schritt 7:** Alles in ein `try/except` einwickeln

```python
try:
    verbindung = db_verbinden()
    # ... dein Code ...
    verbindung.commit()
    verbindung.close()
    self.lbl_station_status.config(text="Gespeichert.", foreground="green")
except sqlite3.Error as fehler:
    messagebox.showerror("Datenbankfehler", str(fehler))
```

### Test

Trage die Zugspitze ein: Name: `Zugspitze Gipfel`, Ort: `Grainau`, Bundesland: `Bayern`, Höhe: `2962`, Breitengrad: `47.421`, Längengrad: `10.985`. Überprüfe das Ergebnis in DB Browser.

---

## Aufgabe 3: CSV-Datei importieren

### Ziel

Implementiere `_klick_csv_importieren()`, sodass eine CSV-Datei mit Messwerten ausgewählt und in die Tabelle `messungen` importiert wird.

### Voraussetzung

Die Stationen müssen zuerst in der Datenbank vorhanden sein (Aufgabe 2 oder direkt aus `messstationen.csv` – dafür müsste man `messstationen.csv` separat importieren, was ihr als Bonus-Aufgabe machen könnt).

Für die Stationen aus `daten_generieren.py` empfiehlt es sich, sie **direkt per Python** einzutragen (kein GUI-Aufwand):

```python
# Einmalig ausführen (z. B. im Python-Interpreter):
from wetter_vorlage import db_verbinden, db_erstellen

db_erstellen()
verbindung = db_verbinden()
cursor = verbindung.cursor()

stationen = [
    ("München Stadtmitte",    "München",   "Bayern",             520,  48.137, 11.576),
    ("Zugspitze Gipfel",      "Grainau",   "Bayern",            2962,  47.421, 10.985),
    ("Hamburg Fuhlsbüttel",   "Hamburg",   "Hamburg",             15,  53.633,  9.998),
    ("Berlin Tempelhof",      "Berlin",    "Berlin",              48,  52.468, 13.404),
    ("Freiburg Hauptbahnhof", "Freiburg",  "Baden-Württemberg",  278,  48.000,  7.842),
]
for name, ort, bl, hoehe, breite, laenge in stationen:
    cursor.execute("INSERT OR IGNORE INTO orte (name, bundesland, hoehe_m) VALUES (?, ?, ?)",
                   (ort, bl, hoehe))
    ort_id = cursor.execute("SELECT ort_id FROM orte WHERE name = ?", (ort,)).fetchone()["ort_id"]
    cursor.execute("INSERT OR IGNORE INTO messstationen (name, ort_id, breitengrad, laengengrad) VALUES (?, ?, ?, ?)",
                   (name, ort_id, breite, laenge))

verbindung.commit()
verbindung.close()
print("Stationen eingetragen.")
```

### Schritt-für-Schritt-Anleitung

**Schritt 1:** Dateiauswahl-Dialog

```python
pfad = filedialog.askopenfilename(
    title="Messwerte-CSV auswählen",
    filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
)
if not pfad:
    return   # Abgebrochen
```

**Schritt 2:** CSV einlesen und Zeilen zählen (für den Fortschrittsbalken)

```python
import csv

with open(pfad, newline="", encoding="utf-8") as datei:
    zeilen = list(csv.DictReader(datei))   # Alle Zeilen laden

self.csv_fortschritt["maximum"] = len(zeilen)
self.csv_fortschritt["value"] = 0
```

**Schritt 3:** In die Datenbank einfügen

```python
verbindung = db_verbinden()
cursor = verbindung.cursor()

for i, zeile in enumerate(zeilen):
    cursor.execute("""
        INSERT INTO messungen
            (station_id, datum, uhrzeit, temperatur_c,
             niederschlag_mm, luftfeuchtigkeit_pct, windgeschwindigkeit_kmh)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        int(zeile["station_id"]),
        zeile["datum"],
        zeile["uhrzeit"],
        float(zeile["temperatur_c"]),
        float(zeile["niederschlag_mm"]),
        int(zeile["luftfeuchtigkeit_pct"]),
        float(zeile["windgeschwindigkeit_kmh"]),
    ))
    self.csv_fortschritt["value"] = i + 1
    self.update_idletasks()   # ← Fortschrittsbalken sofort neu zeichnen

verbindung.commit()
verbindung.close()
```

> **`self.update_idletasks()`** zwingt tkinter, die GUI zu aktualisieren, während die Schleife läuft. Ohne diesen Aufruf würde der Fortschrittsbalken erst am Ende (also nie sichtbar) aktualisiert.

**Schritt 4:** Statusmeldung

```python
self.lbl_csv_status.config(
    text=f"{len(zeilen)} Messungen importiert.",
    foreground="green"
)
```

### Test

Importiere `messungen.csv` und überprüfe in DB Browser: Wie viele Zeilen sind in der Tabelle `messungen`?

---

## Aufgabe 4: Messung über Formular eingeben

### Ziel

Implementiere `_stationen_laden()` (Dropdown befüllen) und `_klick_messung_speichern()` (Messung speichern).

### 4a: Stationen in das Dropdown laden

```python
def _stationen_laden(self):
    try:
        verbindung = db_verbinden()
        cursor = verbindung.cursor()
        cursor.execute("""
            SELECT station_id, messstationen.name
            FROM messstationen
            ORDER BY messstationen.name
        """)
        zeilen = cursor.fetchall()
        verbindung.close()

        self.messung_station_ids = {}
        namen = []
        for zeile in zeilen:
            namen.append(zeile["name"])
            self.messung_station_ids[zeile["name"]] = zeile["station_id"]

        self.combo_station["values"] = namen
        if namen:
            self.combo_station.current(0)   # Ersten Eintrag vorauswählen
    except sqlite3.Error as fehler:
        messagebox.showerror("Fehler", str(fehler))
```

### 4b: Messung speichern

Lies alle Felder aus `self.messung_eingaben` aus und führe einen `INSERT` in `messungen` durch. Die `station_id` holst du aus `self.messung_station_ids`:

```python
station_name = self.messung_station_var.get()
if not station_name:
    messagebox.showwarning("Keine Station", "Bitte zuerst eine Station auswählen (↺).")
    return

station_id = self.messung_station_ids[station_name]
datum      = self.messung_eingaben["datum"].get().strip()
uhrzeit    = self.messung_eingaben["uhrzeit"].get().strip()
temp       = self.messung_eingaben["temp"].get().strip()
# ... usw. ...

cursor.execute("""
    INSERT INTO messungen
        (station_id, datum, uhrzeit, temperatur_c, niederschlag_mm,
         luftfeuchtigkeit_pct, windgeschwindigkeit_kmh)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (station_id, datum, uhrzeit,
      float(temp) if temp else None,
      ...))
```

### Test

Wähle eine Station, gib Werte ein und speichere. Überprüfe in DB Browser oder Tab 5.

---

## Aufgabe 5: Messungen in der Tabelle anzeigen

### Ziel

Implementiere `_klick_messungen_laden()`, sodass alle Messungen (mit Stationsname per JOIN) im Treeview angezeigt werden.

### Anleitung

```python
def _klick_messungen_laden(self):
    try:
        verbindung = db_verbinden()
        cursor = verbindung.cursor()
        cursor.execute("""
            SELECT
                m.messung_id,
                s.name           AS station_name,
                m.datum,
                m.uhrzeit,
                m.temperatur_c,
                m.niederschlag_mm,
                m.luftfeuchtigkeit_pct,
                m.windgeschwindigkeit_kmh
            FROM messungen m
            JOIN messstationen s ON m.station_id = s.station_id
            ORDER BY m.datum DESC, s.name
        """)
        zeilen = cursor.fetchall()
        verbindung.close()

        # Alte Einträge löschen
        self.tabelle.delete(*self.tabelle.get_children())

        # Neue Einträge einfügen
        for zeile in zeilen:
            self.tabelle.insert("", "end", values=(
                zeile["messung_id"],
                zeile["station_name"],
                zeile["datum"],
                zeile["uhrzeit"],
                zeile["temperatur_c"],
                zeile["niederschlag_mm"],
                zeile["luftfeuchtigkeit_pct"],
                zeile["windgeschwindigkeit_kmh"],
            ))

        self.lbl_anzeige_info.config(text=f"{len(zeilen)} Messungen geladen.")

    except sqlite3.Error as fehler:
        messagebox.showerror("Datenbankfehler", str(fehler))
```

### Test

Nach dem Import von `messungen.csv` sollten 1825 Zeilen erscheinen. Scrolle durch die Tabelle und überprüfe die Daten.

---

## Aufgabe 6: Statistische Auswertung

### Ziel

Implementiere `_auswertung_stationen_laden()` (analog zu Aufgabe 4a) und `_klick_auswerten()`.

### 6a: Stationsliste laden

Analog zu `_stationen_laden()` aus Aufgabe 4 – aber diesmal für `self.combo_auswertung` und `self.auswertung_station_ids`.

### 6b: Auswertung berechnen

Abfrage mit Aggregatfunktionen für die gewählte Station:

```python
station_name = self.auswertung_station_var.get()
if not station_name:
    messagebox.showwarning("Keine Station", "Bitte zuerst eine Station laden und auswählen.")
    return

station_id = self.auswertung_station_ids[station_name]

verbindung = db_verbinden()
cursor = verbindung.cursor()
cursor.execute("""
    SELECT
        COUNT(*)                        AS anzahl,
        MIN(datum)                      AS von,
        MAX(datum)                      AS bis,
        MIN(temperatur_c)               AS temp_min,
        MAX(temperatur_c)               AS temp_max,
        ROUND(AVG(temperatur_c), 1)     AS temp_avg,
        ROUND(SUM(niederschlag_mm), 1)  AS regen_gesamt,
        ROUND(AVG(luftfeuchtigkeit_pct),1) AS feuchte_avg,
        ROUND(AVG(windgeschwindigkeit_kmh),1) AS wind_avg
    FROM messungen
    WHERE station_id = ?
""", (station_id,))

r = cursor.fetchone()
verbindung.close()
```

Ergebnis in das Textfeld schreiben:

```python
ausgabe = f"""
Station:       {station_name}
Zeitraum:      {r['von']}  bis  {r['bis']}
Messungen:     {r['anzahl']}

Temperatur:
  Minimum:     {r['temp_min']} °C
  Maximum:     {r['temp_max']} °C
  Durchschnitt:{r['temp_avg']} °C

Niederschlag:  {r['regen_gesamt']} mm gesamt

Luftfeuchte:   {r['feuchte_avg']} % (Ø)
Wind:          {r['wind_avg']} km/h (Ø)
"""

self.auswertung_text.config(state="normal")
self.auswertung_text.delete("1.0", "end")
self.auswertung_text.insert("end", ausgabe)
self.auswertung_text.config(state="disabled")
```

### Test

Wähle verschiedene Stationen aus und vergleiche die Werte. Die Zugspitze sollte die kältesten Temperaturen und den meisten Niederschlag haben.

---

## Erweiterungsideen (freiwillig)

Wenn du die Pflichtaufgaben abgeschlossen hast, kannst du die Anwendung erweitern:

**E1:** Füge einen **Filter** zum Daten-Tab hinzu: Nach Stations-Dropdown filtern, sodass nur Messungen der gewählten Station angezeigt werden.

**E2:** Füge einen **Datums-Filter** hinzu: Nur Messungen zwischen zwei Daten anzeigen.

**E3:** Exportiere die angezeigte Tabelle als neue **CSV-Datei** (Button „Als CSV exportieren").

**E4:** Füge zum Auswertungs-Tab ein **Monats-Dropdown** hinzu, sodass die Auswertung auf einen Monat beschränkt werden kann.

**E5:** Importiere auch `messstationen.csv` über die GUI (eigener Tab oder Button).

**E6:** Füge eine **Suchfunktion** in die Tabelle ein: Eingabefeld für einen Suchbegriff, der in allen Spalten gesucht wird.

---

## Anhang: Beispieldaten im Überblick

### Stationen

| ID | Name | Ort | Bundesland | Höhe |
|---|---|---|---|---|
| 1 | München Stadtmitte | München | Bayern | 520 m |
| 2 | Zugspitze Gipfel | Grainau | Bayern | 2962 m |
| 3 | Hamburg Fuhlsbüttel | Hamburg | Hamburg | 15 m |
| 4 | Berlin Tempelhof | Berlin | Berlin | 48 m |
| 5 | Freiburg Hauptbahnhof | Freiburg | Baden-Württemberg | 278 m |

### Erwartete Auswertungswerte (ungefähr)

| Station | Temp. Ø | Temp. Min | Temp. Max | Niederschlag |
|---|---|---|---|---|
| München | ~9 °C | ~−14 °C | ~32 °C | ~2000 mm |
| Zugspitze | ~−2 °C | ~−25 °C | ~19 °C | ~4000 mm |
| Hamburg | ~10 °C | ~−11 °C | ~32 °C | ~2000 mm |
| Berlin | ~10 °C | ~−13 °C | ~34 °C | ~1600 mm |
| Freiburg | ~13 °C | ~−8 °C | ~38 °C | ~1700 mm |

*(Werte variieren durch den Zufallsanteil; bei gleichem Seed ähnlich reproduzierbar)*

### Ausschnitt aus `messungen.csv`

```
station_id,datum,uhrzeit,temperatur_c,niederschlag_mm,luftfeuchtigkeit_pct,windgeschwindigkeit_kmh
1,2024-01-01,12:00,-3.4,0.0,72,12.3
1,2024-01-02,12:00,1.8,4.2,85,8.7
1,2024-01-03,12:00,-0.9,0.0,68,20.1
2,2024-01-01,12:00,-14.2,12.5,91,31.4
2,2024-01-02,12:00,-11.7,0.0,78,18.2
...
```
