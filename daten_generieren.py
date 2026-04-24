# daten_generieren.py
# ─────────────────────────────────────────────────────────────────
# Erzeugt realistische Beispieldaten für die Wetterdatenbank
# und speichert sie als zwei CSV-Dateien:
#
#   messstationen.csv  – 5 Wetterstationen in Deutschland
#   messungen.csv      – 1 Jahr Tagesmessungen (5 × 365 = 1825 Zeilen)
#
# Starte mit:  python daten_generieren.py
# ─────────────────────────────────────────────────────────────────

import csv
import random
from datetime import date, timedelta

random.seed(42)   # Fester Zufallsseed → immer dieselben Daten


# ══════════════════════════════════════════════════════════════════
# STATIONSDATEN
# Spalten: station_id, name, ort, bundesland, hoehe_m,
#          breitengrad, laengengrad
# ══════════════════════════════════════════════════════════════════

STATIONEN = [
    (1, "München Stadtmitte",    "München",   "Bayern",             520,  48.137, 11.576),
    (2, "Zugspitze Gipfel",      "Grainau",   "Bayern",            2962,  47.421, 10.985),
    (3, "Hamburg Fuhlsbüttel",   "Hamburg",   "Hamburg",             15,  53.633,  9.998),
    (4, "Berlin Tempelhof",      "Berlin",    "Berlin",              48,  52.468, 13.404),
    (5, "Freiburg Hauptbahnhof", "Freiburg",  "Baden-Württemberg",  278,  48.000,  7.842),
]


# ══════════════════════════════════════════════════════════════════
# KLIMAPROFILE
# Durchschnittstemperatur pro Monat in °C (Index 0 = Januar)
# ══════════════════════════════════════════════════════════════════

TEMP_PROFIL = {
    "München":   [-1,  1,  5, 10, 15, 18, 20, 20, 15,  9,  3,  0],
    "Zugspitze": [-10, -9, -6, -2,  2,  5,  7,  7,  4, -1, -5, -9],
    "Hamburg":   [  2,  3,  6, 10, 14, 17, 19, 19, 15, 11,  6,  3],
    "Berlin":    [  1,  2,  6, 11, 16, 19, 21, 21, 16, 10,  5,  2],
    "Freiburg":  [  4,  5,  9, 13, 18, 21, 23, 23, 18, 13,  7,  4],
}

# Regenwahrscheinlichkeit pro Monat (0.0 = nie, 1.0 = immer)
REGEN_PROFIL = {
    "München":   [0.40, 0.40, 0.40, 0.45, 0.50, 0.55, 0.55, 0.50, 0.45, 0.40, 0.40, 0.40],
    "Zugspitze": [0.60, 0.60, 0.60, 0.65, 0.70, 0.75, 0.75, 0.70, 0.65, 0.60, 0.60, 0.60],
    "Hamburg":   [0.55, 0.50, 0.50, 0.45, 0.45, 0.50, 0.50, 0.50, 0.50, 0.50, 0.55, 0.55],
    "Berlin":    [0.40, 0.35, 0.40, 0.40, 0.45, 0.50, 0.45, 0.40, 0.40, 0.40, 0.40, 0.40],
    "Freiburg":  [0.40, 0.40, 0.40, 0.40, 0.45, 0.45, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40],
}


# ══════════════════════════════════════════════════════════════════
# GENERIERUNGSFUNKTIONEN
# ══════════════════════════════════════════════════════════════════

def temp_generieren(ort, monat_index):
    """
    Erzeugt eine realistische Tagestemperatur.
    Basis ist der Monatsdurchschnitt aus TEMP_PROFIL,
    mit einer zufälligen Abweichung (Normalverteilung, σ = 4).
    """
    basis = TEMP_PROFIL[ort][monat_index]
    return round(basis + random.gauss(0, 4), 1)


def niederschlag_generieren(ort, monat_index):
    """
    Erzeugt einen realistischen Tagesniederschlag.
    Mit der Wahrscheinlichkeit aus REGEN_PROFIL fällt Regen;
    die Menge folgt einer Exponentialverteilung (viele kleine,
    wenige große Werte).
    """
    if random.random() < REGEN_PROFIL[ort][monat_index]:
        return round(random.expovariate(1 / 8), 1)   # Durchschnitt ~8 mm
    return 0.0


def messungen_generieren(start_datum, anzahl_tage):
    """
    Erzeugt für alle Stationen jeweils eine Tagesmessung.
    Gibt eine Liste von Dictionaries zurück.
    """
    messungen = []

    for station_id, name, ort, bundesland, hoehe, breite, laenge in STATIONEN:
        aktuelles_datum = start_datum

        for _ in range(anzahl_tage):
            monat_index = aktuelles_datum.month - 1   # 0-basiert (Jan=0)

            messungen.append({
                "station_id":              station_id,
                "datum":                   str(aktuelles_datum),
                "uhrzeit":                 "12:00",
                "temperatur_c":            temp_generieren(ort, monat_index),
                "niederschlag_mm":         niederschlag_generieren(ort, monat_index),
                "luftfeuchtigkeit_pct":    random.randint(35, 98),
                "windgeschwindigkeit_kmh": round(max(0, random.gauss(15, 8)), 1),
            })

            aktuelles_datum += timedelta(days=1)

    return messungen


# ══════════════════════════════════════════════════════════════════
# HAUPTPROGRAMM
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generiere Beispieldaten ...\n")

    # ── Stationen als CSV ────────────────────────────────────────
    with open("messstationen.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "station_id", "name", "ort", "bundesland",
            "hoehe_m", "breitengrad", "laengengrad"
        ])
        writer.writerows(STATIONEN)

    print(f"  ✓  messstationen.csv  ({len(STATIONEN)} Stationen)")

    # ── Messungen als CSV (1 Jahr) ───────────────────────────────
    messungen = messungen_generieren(date(2024, 1, 1), 365)

    with open("messungen.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(messungen[0].keys()))
        writer.writeheader()
        writer.writerows(messungen)

    print(f"  ✓  messungen.csv      ({len(messungen)} Messungen)")
    print(f"\nFertig! Importiere die Dateien mit der Wetter-App (Tab 'CSV-Import').")
