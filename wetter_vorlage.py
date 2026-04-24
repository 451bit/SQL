# wetter_vorlage.py
# ─────────────────────────────────────────────────────────────────
# Vorlage: Wetterdatenbank-App mit Python, tkinter und SQLite
#
# Starte das Programm mit:
#   python wetter_vorlage.py
#
# Voraussetzungen: Python 3.x (tkinter und sqlite3 sind bereits
# in der Standardbibliothek enthalten – keine Installation nötig)
# ─────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
import os
from datetime import date


# ══════════════════════════════════════════════════════════════════
# KONFIGURATION
# ══════════════════════════════════════════════════════════════════

# Datenbankdatei im selben Ordner wie dieses Skript speichern,
# unabhängig davon, von wo Python gestartet wird.
DB_PFAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wetterdaten.db")


# ══════════════════════════════════════════════════════════════════
# DATENBANKFUNKTIONEN
# Diese Funktionen sind unabhängig von der GUI und können auch
# einzeln getestet werden (z. B. im Python-Interpreter).
# ══════════════════════════════════════════════════════════════════

def db_verbinden():
    """
    Öffnet eine Verbindung zur SQLite-Datenbank und gibt sie zurück.
    row_factory = sqlite3.Row erlaubt Zugriff auf Spalten per Name
    (z. B. zeile["temperatur_c"] statt zeile[0]).
    """
    verbindung = sqlite3.connect(DB_PFAD)
    verbindung.row_factory = sqlite3.Row
    return verbindung


def db_erstellen():
    """
    Erstellt alle Tabellen der Wetterdatenbank (falls noch nicht vorhanden).
    Kann beliebig oft aufgerufen werden – bestehende Daten bleiben erhalten
    (CREATE TABLE IF NOT EXISTS).
    """
    verbindung = db_verbinden()
    cursor = verbindung.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS orte (
            ort_id     INTEGER PRIMARY KEY,
            name       TEXT    NOT NULL,
            bundesland TEXT    NOT NULL,
            hoehe_m    INTEGER
        );

        CREATE TABLE IF NOT EXISTS messstationen (
            station_id  INTEGER PRIMARY KEY,
            name        TEXT    NOT NULL,
            ort_id      INTEGER NOT NULL REFERENCES orte(ort_id),
            breitengrad REAL,
            laengengrad REAL
        );

        CREATE TABLE IF NOT EXISTS messungen (
            messung_id              INTEGER PRIMARY KEY,
            station_id              INTEGER NOT NULL REFERENCES messstationen(station_id),
            datum                   TEXT    NOT NULL,
            uhrzeit                 TEXT    NOT NULL DEFAULT '12:00',
            temperatur_c            REAL,
            niederschlag_mm         REAL    DEFAULT 0.0,
            luftfeuchtigkeit_pct    INTEGER,
            windgeschwindigkeit_kmh REAL
        );
    """)

    verbindung.commit()
    verbindung.close()


# ══════════════════════════════════════════════════════════════════
# HAUPT-ANWENDUNG (GUI)
# ══════════════════════════════════════════════════════════════════

class WetterApp(tk.Tk):
    """
    Hauptfenster der Wetterdatenbank-Anwendung.
    Die Klasse erbt von tk.Tk – das Objekt IST das Hauptfenster.
    """

    def __init__(self):
        super().__init__()                      # Tkinter-Fenster initialisieren
        self.title("Wetterdatenbank")
        self.geometry("960x700")
        self.resizable(True, True)
        self._gui_aufbauen()

    # ──────────────────────────────────────────────────────────────
    # GUI-GRUNDGERÜST
    # ──────────────────────────────────────────────────────────────

    def _gui_aufbauen(self):
        """Baut die gesamte Benutzeroberfläche auf."""

        # Überschrift
        tk.Label(
            self,
            text="Wetterdatenbank",
            font=("Arial", 18, "bold"),
            pady=8
        ).pack()

        # Trennlinie
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Leere Tab-Rahmen anlegen
        self.tab_db         = ttk.Frame(self.notebook)
        self.tab_station    = ttk.Frame(self.notebook)
        self.tab_messung    = ttk.Frame(self.notebook)
        self.tab_csv        = ttk.Frame(self.notebook)
        self.tab_anzeige    = ttk.Frame(self.notebook)
        self.tab_auswertung = ttk.Frame(self.notebook)

        # Tabs einhängen
        self.notebook.add(self.tab_db,         text="  Datenbank  ")
        self.notebook.add(self.tab_station,    text="  Station eintragen  ")
        self.notebook.add(self.tab_messung,    text="  Messung eintragen  ")
        self.notebook.add(self.tab_csv,        text="  CSV-Import  ")
        self.notebook.add(self.tab_anzeige,    text="  Daten anzeigen  ")
        self.notebook.add(self.tab_auswertung, text="  Auswertung  ")

        # Jeden Tab mit Inhalt füllen
        self._aufbau_tab_db()
        self._aufbau_tab_station()
        self._aufbau_tab_messung()
        self._aufbau_tab_csv()
        self._aufbau_tab_anzeige()
        self._aufbau_tab_auswertung()

    # ──────────────────────────────────────────────────────────────
    # TAB 1: DATENBANK ERSTELLEN
    # Dieser Tab ist bereits vollständig implementiert.
    # Er dient als Beispiel dafür, wie Button-Klicks mit
    # Datenbankfunktionen verknüpft werden.
    # ──────────────────────────────────────────────────────────────

    def _aufbau_tab_db(self):
        f = self.tab_db

        ttk.Label(f, text="Datenbankverwaltung",
                  font=("Arial", 13, "bold")).pack(pady=(30, 6))
        ttk.Label(f, text=f"Datenbankdatei: {os.path.abspath(DB_PFAD)}",
                  foreground="gray").pack()

        ttk.Button(
            f,
            text="Datenbank erstellen / Tabellen prüfen",
            command=self._klick_db_erstellen
        ).pack(pady=22)

        self.lbl_db_status = ttk.Label(f, text="")
        self.lbl_db_status.pack()

    def _klick_db_erstellen(self):
        """Wird aufgerufen, wenn der Button geklickt wird."""
        try:
            db_erstellen()
            self.lbl_db_status.config(
                text="Datenbank wurde erfolgreich erstellt.",
                foreground="green"
            )
        except Exception as fehler:
            messagebox.showerror("Fehler", str(fehler))

    # ──────────────────────────────────────────────────────────────
    # TAB 2: STATION EINTRAGEN
    # ──────────────────────────────────────────────────────────────

    def _aufbau_tab_station(self):
        f = self.tab_station

        ttk.Label(f, text="Neue Messstation eintragen",
                  font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(22, 14), padx=20
        )

        # Formularfelder: (Beschriftung, interner Schlüssel)
        felder = [
            ("Stationsname:",       "name"),
            ("Ort:",                "ort"),
            ("Bundesland:",         "bundesland"),
            ("Höhe über NN (m):",   "hoehe"),
            ("Breitengrad:",        "breitengrad"),
            ("Längengrad:",         "laengengrad"),
        ]

        self.station_eingaben = {}
        for i, (beschriftung, key) in enumerate(felder, start=1):
            ttk.Label(f, text=beschriftung).grid(
                row=i, column=0, sticky="e", padx=16, pady=7
            )
            eingabe = ttk.Entry(f, width=34)
            eingabe.grid(row=i, column=1, padx=10, pady=7, sticky="w")
            self.station_eingaben[key] = eingabe

        ttk.Button(
            f,
            text="Station speichern",
            command=self._klick_station_speichern
        ).grid(row=len(felder) + 1, column=0, columnspan=2, pady=20)

        self.lbl_station_status = ttk.Label(f, text="")
        self.lbl_station_status.grid(row=len(felder) + 2, column=0, columnspan=2)

    def _klick_station_speichern(self):
        """
        ╔══ AUFGABE 2 ══════════════════════════════════════════════╗
        ║  Lese die Eingabefelder aus und speichere die neue        ║
        ║  Messstation in der Datenbank.                            ║
        ║                                                           ║
        ║  Schritte:                                                ║
        ║  1. Werte lesen:  wert = self.station_eingaben["name"]    ║
        ║                          .get().strip()                   ║
        ║  2. Pflichtfelder prüfen (name, ort, bundesland)          ║
        ║  3. Ort in Tabelle 'orte' einfügen (INSERT INTO ...)      ║
        ║  4. Station in 'messstationen' einfügen                   ║
        ║  5. Statuslabel aktualisieren                             ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 2

    # ──────────────────────────────────────────────────────────────
    # TAB 3: MESSUNG EINTRAGEN
    # ──────────────────────────────────────────────────────────────

    def _aufbau_tab_messung(self):
        f = self.tab_messung

        ttk.Label(f, text="Neue Messung eintragen",
                  font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(22, 14), padx=20
        )

        # Station auswählen (Dropdown/Combobox)
        ttk.Label(f, text="Station:").grid(row=1, column=0, sticky="e", padx=16, pady=7)
        self.messung_station_var = tk.StringVar()
        self.messung_station_ids = {}   # Mapping: Anzeigename → station_id

        self.combo_station = ttk.Combobox(
            f,
            textvariable=self.messung_station_var,
            width=32,
            state="readonly"
        )
        self.combo_station.grid(row=1, column=1, padx=10, pady=7, sticky="w")

        # Refresh-Button neben dem Dropdown
        ttk.Button(f, text="↺", command=self._stationen_laden, width=3).grid(
            row=1, column=2, padx=4
        )

        # Messfelder
        felder = [
            ("Datum (JJJJ-MM-TT):",          "datum"),
            ("Uhrzeit (HH:MM):",              "uhrzeit"),
            ("Temperatur (°C):",              "temp"),
            ("Niederschlag (mm):",            "niederschlag"),
            ("Luftfeuchtigkeit (%):",         "feuchte"),
            ("Windgeschwindigkeit (km/h):",   "wind"),
        ]

        self.messung_eingaben = {}
        for i, (beschriftung, key) in enumerate(felder, start=2):
            ttk.Label(f, text=beschriftung).grid(
                row=i, column=0, sticky="e", padx=16, pady=7
            )
            eingabe = ttk.Entry(f, width=34)
            eingabe.grid(row=i, column=1, padx=10, pady=7, sticky="w")
            self.messung_eingaben[key] = eingabe

        # Vorausfüllen mit sinnvollen Standardwerten
        self.messung_eingaben["datum"].insert(0, str(date.today()))
        self.messung_eingaben["uhrzeit"].insert(0, "12:00")
        self.messung_eingaben["niederschlag"].insert(0, "0.0")

        ttk.Button(
            f,
            text="Messung speichern",
            command=self._klick_messung_speichern
        ).grid(row=len(felder) + 2, column=0, columnspan=2, pady=20)

        self.lbl_messung_status = ttk.Label(f, text="")
        self.lbl_messung_status.grid(row=len(felder) + 3, column=0, columnspan=2)

    def _stationen_laden(self):
        """
        ╔══ AUFGABE 4a ══════════════════════════════════════════════╗
        ║  Lade alle Stationen aus der DB und befülle das Dropdown.  ║
        ║                                                            ║
        ║  Schritte:                                                 ║
        ║  1. DB verbinden, alle Stationen abfragen (JOIN mit orte)  ║
        ║  2. self.messung_station_ids befüllen:                     ║
        ║       { "München Stadtmitte": 1, ... }                    ║
        ║  3. self.combo_station["values"] = [liste der namen]       ║
        ╚════════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 4a

    def _klick_messung_speichern(self):
        """
        ╔══ AUFGABE 4b ══════════════════════════════════════════════╗
        ║  Lese alle Messfelder aus und speichere die Messung in     ║
        ║  der Tabelle 'messungen'.                                  ║
        ║                                                            ║
        ║  Hinweis: Die station_id bekommst du über:                 ║
        ║    name = self.messung_station_var.get()                   ║
        ║    sid  = self.messung_station_ids[name]                   ║
        ╚════════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 4b

    # ──────────────────────────────────────────────────────────────
    # TAB 4: CSV-IMPORT
    # ──────────────────────────────────────────────────────────────

    def _aufbau_tab_csv(self):
        f = self.tab_csv

        ttk.Label(f, text="Messwerte aus CSV-Datei importieren",
                  font=("Arial", 13, "bold")).pack(pady=(30, 8))

        ttk.Label(
            f,
            text=(
                "Erwartetes CSV-Format (erste Zeile = Kopfzeile):\n"
                "station_id, datum, uhrzeit, temperatur_c, "
                "niederschlag_mm, luftfeuchtigkeit_pct, windgeschwindigkeit_kmh"
            ),
            foreground="gray",
            wraplength=600,
            justify="center"
        ).pack(pady=6)

        ttk.Button(
            f,
            text="CSV-Datei auswählen und importieren ...",
            command=self._klick_csv_importieren
        ).pack(pady=22)

        self.lbl_csv_status = ttk.Label(f, text="")
        self.lbl_csv_status.pack()

        self.csv_fortschritt = ttk.Progressbar(f, length=420, mode="determinate")
        self.csv_fortschritt.pack(pady=8)

    def _klick_csv_importieren(self):
        """
        ╔══ AUFGABE 3 ══════════════════════════════════════════════╗
        ║  1. Dateiauswahl-Dialog öffnen:                           ║
        ║       pfad = filedialog.askopenfilename(                  ║
        ║           filetypes=[("CSV-Dateien", "*.csv")])           ║
        ║  2. CSV mit csv.DictReader einlesen                       ║
        ║  3. Für jede Zeile einen INSERT in 'messungen' ausführen  ║
        ║  4. Fortschrittsbalken aktualisieren                      ║
        ║  5. Statusmeldung: "X Messungen importiert."              ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 3

    # ──────────────────────────────────────────────────────────────
    # TAB 5: DATEN ANZEIGEN
    # ──────────────────────────────────────────────────────────────

    def _aufbau_tab_anzeige(self):
        f = self.tab_anzeige

        # Werkzeugleiste oben
        toolbar = ttk.Frame(f)
        toolbar.pack(fill="x", padx=10, pady=6)

        ttk.Button(
            toolbar, text="Alle Messungen laden",
            command=self._klick_messungen_laden
        ).pack(side="left")

        self.lbl_anzeige_info = ttk.Label(toolbar, text="", foreground="gray")
        self.lbl_anzeige_info.pack(side="left", padx=12)

        # Treeview (Tabelle)
        spalten = (
            "ID", "Station", "Datum", "Uhrzeit",
            "Temp. (°C)", "Niederschlag (mm)", "Feuchte (%)", "Wind (km/h)"
        )
        breiten = [45, 190, 100, 75, 95, 140, 95, 95]

        self.tabelle = ttk.Treeview(f, columns=spalten, show="headings", height=22)
        for spalte, breite in zip(spalten, breiten):
            self.tabelle.heading(spalte, text=spalte)
            self.tabelle.column(spalte, width=breite, anchor="center")

        # Scrollbars
        sb_v = ttk.Scrollbar(f, orient="vertical",   command=self.tabelle.yview)
        sb_h = ttk.Scrollbar(f, orient="horizontal", command=self.tabelle.xview)
        self.tabelle.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)

        self.tabelle.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 5))
        sb_v.pack(side="right",  fill="y",  pady=(0, 5))
        sb_h.pack(side="bottom", fill="x")

    def _klick_messungen_laden(self):
        """
        ╔══ AUFGABE 5 ══════════════════════════════════════════════╗
        ║  Lade alle Messungen aus der DB (JOIN mit messstationen)  ║
        ║  und zeige sie im Treeview an.                            ║
        ║                                                           ║
        ║  Vorhandene Einträge zuerst löschen:                      ║
        ║    self.tabelle.delete(*self.tabelle.get_children())      ║
        ║                                                           ║
        ║  Zeile einfügen:                                          ║
        ║    self.tabelle.insert("", "end", values=(id, name, ...)) ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 5

    # ──────────────────────────────────────────────────────────────
    # TAB 6: AUSWERTUNG
    # ──────────────────────────────────────────────────────────────

    def _aufbau_tab_auswertung(self):
        f = self.tab_auswertung

        ttk.Label(f, text="Statistische Auswertung",
                  font=("Arial", 13, "bold")).pack(pady=(30, 12))

        # Station auswählen
        auswahl_frame = ttk.Frame(f)
        auswahl_frame.pack()

        ttk.Label(auswahl_frame, text="Station:").pack(side="left")
        self.auswertung_station_var = tk.StringVar()
        self.auswertung_station_ids = {}

        self.combo_auswertung = ttk.Combobox(
            auswahl_frame,
            textvariable=self.auswertung_station_var,
            width=30,
            state="readonly"
        )
        self.combo_auswertung.pack(side="left", padx=6)

        ttk.Button(
            auswahl_frame, text="↺",
            command=self._auswertung_stationen_laden, width=3
        ).pack(side="left")

        ttk.Button(
            auswahl_frame, text="Auswerten",
            command=self._klick_auswerten
        ).pack(side="left", padx=10)

        # Textfeld für die Ausgabe
        self.auswertung_text = tk.Text(
            f,
            height=16, width=55,
            state="disabled",
            font=("Courier New", 11),
            padx=12, pady=10
        )
        self.auswertung_text.pack(pady=16)

    def _auswertung_stationen_laden(self):
        """
        ╔══ AUFGABE 6a ══════════════════════════════════════════════╗
        ║  Analog zu _stationen_laden(), aber für                    ║
        ║  self.combo_auswertung und self.auswertung_station_ids.    ║
        ╚════════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 6a

    def _klick_auswerten(self):
        """
        ╔══ AUFGABE 6b ══════════════════════════════════════════════╗
        ║  Berechne für die gewählte Station per SQL-Aggregation:    ║
        ║    - Anzahl Messungen                                      ║
        ║    - Zeitraum (MIN/MAX Datum)                              ║
        ║    - Temperatur: MIN, MAX, AVG                             ║
        ║    - Gesamtniederschlag: SUM                               ║
        ║    - Luftfeuchtigkeit: AVG                                 ║
        ║    - Windgeschwindigkeit: AVG                              ║
        ║                                                            ║
        ║  Ergebnis in self.auswertung_text ausgeben:                ║
        ║    self.auswertung_text.config(state="normal")             ║
        ║    self.auswertung_text.delete("1.0", "end")               ║
        ║    self.auswertung_text.insert("end", "dein text\n")       ║
        ║    self.auswertung_text.config(state="disabled")           ║
        ╚════════════════════════════════════════════════════════════╝
        """
        pass   # TODO: Aufgabe 6b


# ══════════════════════════════════════════════════════════════════
# PROGRAMM STARTEN
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = WetterApp()
    app.mainloop()
