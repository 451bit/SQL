-- Schuldatenbank: "Kantine & Schülerausweis"
-- Alltagnah: Schüler, Klassen, Kantinenbestellungen, Fächer, Noten

PRAGMA foreign_keys = ON;

-- Tabelle: klassen
CREATE TABLE IF NOT EXISTS klassen (
    klasse_id   INTEGER PRIMARY KEY,
    bezeichnung TEXT    NOT NULL,
    stufe       INTEGER NOT NULL,
    klassenlehrer TEXT  NOT NULL
);

-- Tabelle: schueler
CREATE TABLE IF NOT EXISTS schueler (
    schueler_id  INTEGER PRIMARY KEY,
    vorname      TEXT    NOT NULL,
    nachname     TEXT    NOT NULL,
    klasse_id    INTEGER NOT NULL REFERENCES klassen(klasse_id),
    geburtsdatum TEXT    NOT NULL,
    geschlecht   TEXT    NOT NULL
);

-- Tabelle: faecher
CREATE TABLE IF NOT EXISTS faecher (
    fach_id   INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    kuerzel   TEXT NOT NULL
);

-- Tabelle: noten
CREATE TABLE IF NOT EXISTS noten (
    noten_id    INTEGER PRIMARY KEY,
    schueler_id INTEGER NOT NULL REFERENCES schueler(schueler_id),
    fach_id     INTEGER NOT NULL REFERENCES faecher(fach_id),
    note        REAL    NOT NULL,
    datum       TEXT    NOT NULL,
    art         TEXT    NOT NULL  -- 'Klassenarbeit', 'Test', 'Muendlich'
);

-- Tabelle: produkte (Kantine)
CREATE TABLE IF NOT EXISTS produkte (
    produkt_id  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    kategorie   TEXT    NOT NULL,
    preis       REAL    NOT NULL
);

-- Tabelle: bestellungen (Kantine)
CREATE TABLE IF NOT EXISTS bestellungen (
    bestell_id  INTEGER PRIMARY KEY,
    schueler_id INTEGER NOT NULL REFERENCES schueler(schueler_id),
    produkt_id  INTEGER NOT NULL REFERENCES produkte(produkt_id),
    datum       TEXT    NOT NULL,
    menge       INTEGER NOT NULL DEFAULT 1
);

-- ========== Daten ==========

INSERT INTO klassen VALUES
(1, '9a', 9, 'Frau Müller'),
(2, '9b', 9, 'Herr Schmidt'),
(3, '10a', 10, 'Frau Keller'),
(4, '10b', 10, 'Herr Weber');

INSERT INTO schueler VALUES
(1,  'Leon',    'Bauer',     1, '2010-03-14', 'm'),
(2,  'Sophie',  'Wagner',    1, '2010-07-22', 'w'),
(3,  'Finn',    'Schulz',    1, '2011-01-05', 'm'),
(4,  'Mia',     'Koch',      1, '2010-11-18', 'w'),
(5,  'Jonas',   'Fischer',   1, '2010-09-30', 'm'),
(6,  'Emma',    'Schneider', 2, '2010-06-12', 'w'),
(7,  'Luca',    'Hoffmann',  2, '2011-02-28', 'm'),
(8,  'Hannah',  'Richter',   2, '2010-04-03', 'w'),
(9,  'Noah',    'Klein',     2, '2010-08-17', 'm'),
(10, 'Lena',    'Wolf',      2, '2011-03-09', 'w'),
(11, 'Tim',     'Braun',     3, '2009-05-21', 'm'),
(12, 'Laura',   'Krause',    3, '2009-12-14', 'w'),
(13, 'Max',     'Lange',     3, '2009-07-07', 'm'),
(14, 'Julia',   'Schwarz',   3, '2009-10-25', 'w'),
(15, 'Paul',    'Zimmermann',3, '2009-02-19', 'm'),
(16, 'Anna',    'Neumann',   4, '2009-08-08', 'w'),
(17, 'Elias',   'Hartmann',  4, '2009-11-30', 'm'),
(18, 'Sarah',   'Walter',    4, '2009-04-16', 'w'),
(19, 'Felix',   'König',     4, '2009-06-02', 'm'),
(20, 'Marie',   'Schmitt',   4, '2009-09-11', 'w');

INSERT INTO faecher VALUES
(1, 'Mathematik',  'Ma'),
(2, 'Deutsch',     'De'),
(3, 'Englisch',    'En'),
(4, 'Informatik',  'Inf'),
(5, 'Sport',       'Sp');

INSERT INTO noten VALUES
-- 9a
(1,  1, 1, 2.0, '2025-10-15', 'Klassenarbeit'),
(2,  1, 2, 3.0, '2025-10-20', 'Klassenarbeit'),
(3,  1, 3, 2.0, '2025-11-05', 'Test'),
(4,  1, 4, 1.0, '2025-11-12', 'Klassenarbeit'),
(5,  2, 1, 4.0, '2025-10-15', 'Klassenarbeit'),
(6,  2, 2, 2.0, '2025-10-20', 'Klassenarbeit'),
(7,  2, 3, 3.0, '2025-11-05', 'Test'),
(8,  2, 4, 2.0, '2025-11-12', 'Klassenarbeit'),
(9,  3, 1, 3.0, '2025-10-15', 'Klassenarbeit'),
(10, 3, 2, 3.0, '2025-10-20', 'Klassenarbeit'),
(11, 3, 3, 4.0, '2025-11-05', 'Test'),
(12, 3, 4, 3.0, '2025-11-12', 'Klassenarbeit'),
(13, 4, 1, 1.0, '2025-10-15', 'Klassenarbeit'),
(14, 4, 2, 2.0, '2025-10-20', 'Klassenarbeit'),
(15, 4, 3, 1.0, '2025-11-05', 'Test'),
(16, 4, 4, 2.0, '2025-11-12', 'Klassenarbeit'),
(17, 5, 1, 5.0, '2025-10-15', 'Klassenarbeit'),
(18, 5, 2, 4.0, '2025-10-20', 'Klassenarbeit'),
(19, 5, 3, 3.0, '2025-11-05', 'Test'),
(20, 5, 4, 4.0, '2025-11-12', 'Klassenarbeit'),
-- 9b
(21, 6, 1, 2.0, '2025-10-15', 'Klassenarbeit'),
(22, 6, 2, 1.0, '2025-10-20', 'Klassenarbeit'),
(23, 6, 3, 2.0, '2025-11-05', 'Test'),
(24, 6, 4, 1.0, '2025-11-12', 'Klassenarbeit'),
(25, 7, 1, 3.0, '2025-10-15', 'Klassenarbeit'),
(26, 7, 2, 4.0, '2025-10-20', 'Klassenarbeit'),
(27, 7, 3, 3.0, '2025-11-05', 'Test'),
(28, 7, 4, 5.0, '2025-11-12', 'Klassenarbeit'),
(29, 8, 1, 2.0, '2025-10-15', 'Klassenarbeit'),
(30, 8, 2, 2.0, '2025-10-20', 'Klassenarbeit'),
(31, 8, 3, 1.0, '2025-11-05', 'Test'),
(32, 8, 4, 2.0, '2025-11-12', 'Klassenarbeit'),
(33, 9, 1, 4.0, '2025-10-15', 'Klassenarbeit'),
(34, 9, 2, 3.0, '2025-10-20', 'Klassenarbeit'),
(35, 9, 3, 4.0, '2025-11-05', 'Test'),
(36, 9, 4, 3.0, '2025-11-12', 'Klassenarbeit'),
(37, 10, 1, 1.0, '2025-10-15', 'Klassenarbeit'),
(38, 10, 2, 2.0, '2025-10-20', 'Klassenarbeit'),
(39, 10, 3, 2.0, '2025-11-05', 'Test'),
(40, 10, 4, 1.0, '2025-11-12', 'Klassenarbeit'),
-- 10a
(41, 11, 1, 3.0, '2025-10-16', 'Klassenarbeit'),
(42, 11, 2, 2.0, '2025-10-21', 'Klassenarbeit'),
(43, 11, 3, 3.0, '2025-11-06', 'Test'),
(44, 11, 4, 2.0, '2025-11-13', 'Klassenarbeit'),
(45, 12, 1, 2.0, '2025-10-16', 'Klassenarbeit'),
(46, 12, 2, 1.0, '2025-10-21', 'Klassenarbeit'),
(47, 12, 3, 2.0, '2025-11-06', 'Test'),
(48, 12, 4, 1.0, '2025-11-13', 'Klassenarbeit'),
(49, 13, 1, 4.0, '2025-10-16', 'Klassenarbeit'),
(50, 13, 2, 5.0, '2025-10-21', 'Klassenarbeit'),
(51, 13, 3, 4.0, '2025-11-06', 'Test'),
(52, 13, 4, 3.0, '2025-11-13', 'Klassenarbeit'),
(53, 14, 1, 1.0, '2025-10-16', 'Klassenarbeit'),
(54, 14, 2, 2.0, '2025-10-21', 'Klassenarbeit'),
(55, 14, 3, 1.0, '2025-11-06', 'Test'),
(56, 14, 4, 2.0, '2025-11-13', 'Klassenarbeit'),
(57, 15, 1, 5.0, '2025-10-16', 'Klassenarbeit'),
(58, 15, 2, 4.0, '2025-10-21', 'Klassenarbeit'),
(59, 15, 3, 5.0, '2025-11-06', 'Test'),
(60, 15, 4, 4.0, '2025-11-13', 'Klassenarbeit'),
-- 10b
(61, 16, 1, 2.0, '2025-10-16', 'Klassenarbeit'),
(62, 16, 2, 3.0, '2025-10-21', 'Klassenarbeit'),
(63, 16, 3, 2.0, '2025-11-06', 'Test'),
(64, 16, 4, 3.0, '2025-11-13', 'Klassenarbeit'),
(65, 17, 1, 3.0, '2025-10-16', 'Klassenarbeit'),
(66, 17, 2, 4.0, '2025-10-21', 'Klassenarbeit'),
(67, 17, 3, 3.0, '2025-11-06', 'Test'),
(68, 17, 4, 2.0, '2025-11-13', 'Klassenarbeit'),
(69, 18, 1, 1.0, '2025-10-16', 'Klassenarbeit'),
(70, 18, 2, 2.0, '2025-10-21', 'Klassenarbeit'),
(71, 18, 3, 1.0, '2025-11-06', 'Test'),
(72, 18, 4, 2.0, '2025-11-13', 'Klassenarbeit'),
(73, 19, 1, 4.0, '2025-10-16', 'Klassenarbeit'),
(74, 19, 2, 3.0, '2025-10-21', 'Klassenarbeit'),
(75, 19, 3, 4.0, '2025-11-06', 'Test'),
(76, 19, 4, 5.0, '2025-11-13', 'Klassenarbeit'),
(77, 20, 1, 2.0, '2025-10-16', 'Klassenarbeit'),
(78, 20, 2, 1.0, '2025-10-21', 'Klassenarbeit'),
(79, 20, 3, 2.0, '2025-11-06', 'Test'),
(80, 20, 4, 1.0, '2025-11-13', 'Klassenarbeit');

INSERT INTO produkte VALUES
(1, 'Pizza Margherita',    'Hauptgericht', 3.50),
(2, 'Spaghetti Bolognese', 'Hauptgericht', 3.80),
(3, 'Gemüsecurry',         'Hauptgericht', 3.20),
(4, 'Schnitzel mit Pommes','Hauptgericht', 4.20),
(5, 'Fischstäbchen',       'Hauptgericht', 3.60),
(6, 'Apfelsaft',           'Getränk',      1.20),
(7, 'Wasser',              'Getränk',      0.80),
(8, 'Kakao',               'Getränk',      1.30),
(9, 'Muffin',              'Snack',        1.50),
(10,'Obstsalat',           'Snack',        1.80),
(11,'Chips',               'Snack',        1.00),
(12,'Schokoriegel',        'Snack',        0.90);

INSERT INTO bestellungen VALUES
-- Leon (1)
(1,  1,  1, '2025-11-03', 1), (2,  1,  6, '2025-11-03', 1),
(3,  1,  4, '2025-11-04', 1), (4,  1,  7, '2025-11-04', 1),
(5,  1,  1, '2025-11-05', 1), (6,  1,  9, '2025-11-05', 1),
(7,  1,  2, '2025-11-06', 1), (8,  1,  6, '2025-11-06', 1),
-- Sophie (2)
(9,  2,  3, '2025-11-03', 1), (10, 2,  8, '2025-11-03', 1),
(11, 2,  3, '2025-11-04', 1), (12, 2,  7, '2025-11-04', 1),
(13, 2, 10, '2025-11-05', 1), (14, 2,  8, '2025-11-05', 1),
-- Finn (3)
(15, 3,  4, '2025-11-03', 1), (16, 3,  6, '2025-11-03', 1),
(17, 3,  4, '2025-11-04', 1), (18, 3,  11,'2025-11-04', 2),
(19, 3,  5, '2025-11-05', 1), (20, 3,  7, '2025-11-05', 1),
-- Mia (4)
(21, 4,  3, '2025-11-03', 1), (22, 4,  10,'2025-11-03', 1),
(23, 4,  3, '2025-11-04', 1), (24, 4,  8, '2025-11-04', 1),
(25, 4,  1, '2025-11-05', 1), (26, 4,  7, '2025-11-05', 1),
-- Jonas (5)
(27, 5,  2, '2025-11-03', 1), (28, 5,  12,'2025-11-03', 2),
(29, 5,  4, '2025-11-04', 1), (30, 5,  6, '2025-11-04', 1),
(31, 5,  2, '2025-11-05', 1), (32, 5,  9, '2025-11-05', 1),
-- Emma (6)
(33, 6,  1, '2025-11-03', 1), (34, 6,  6, '2025-11-03', 1),
(35, 6,  5, '2025-11-04', 1), (36, 6,  8, '2025-11-04', 1),
(37, 6,  3, '2025-11-05', 1), (38, 6,  7, '2025-11-05', 1),
-- Luca (7)
(39, 7,  4, '2025-11-03', 1), (40, 7,  6, '2025-11-03', 1),
(41, 7,  4, '2025-11-04', 1), (42, 7,  12,'2025-11-04', 3),
(43, 7,  1, '2025-11-05', 1), (44, 7,  6, '2025-11-05', 1),
-- Hannah (8)
(45, 8,  2, '2025-11-03', 1), (46, 8,  7, '2025-11-03', 1),
(47, 8,  3, '2025-11-04', 1), (48, 8,  10,'2025-11-04', 1),
(49, 8,  2, '2025-11-05', 1), (50, 8,  8, '2025-11-05', 1),
-- Noah (9)
(51, 9,  4, '2025-11-03', 1), (52, 9,  6, '2025-11-03', 1),
(53, 9,  1, '2025-11-04', 1), (54, 9,  9, '2025-11-04', 1),
-- Lena (10)
(55,10,  3, '2025-11-03', 1), (56,10,  7, '2025-11-03', 1),
(57,10,  3, '2025-11-04', 1), (58,10, 10, '2025-11-04', 1),
(59,10,  5, '2025-11-05', 1), (60,10,  8, '2025-11-05', 1),
-- 10a: Tim (11) bis Paul (15)
(61,11,  2, '2025-11-03', 1), (62,11,  6, '2025-11-03', 1),
(63,11,  4, '2025-11-04', 1), (64,11,  7, '2025-11-04', 1),
(65,12,  1, '2025-11-03', 1), (66,12,  8, '2025-11-03', 1),
(67,12,  3, '2025-11-04', 1), (68,12, 10, '2025-11-04', 1),
(69,13,  4, '2025-11-03', 1), (70,13,  6, '2025-11-03', 1),
(71,13,  4, '2025-11-04', 1), (72,13, 11, '2025-11-04', 2),
(73,14,  2, '2025-11-03', 1), (74,14,  7, '2025-11-03', 1),
(75,14,  1, '2025-11-04', 1), (76,14,  9, '2025-11-04', 1),
(77,15,  5, '2025-11-03', 1), (78,15,  6, '2025-11-03', 1),
(79,15,  4, '2025-11-04', 1), (80,15,  8, '2025-11-04', 1),
-- 10b: Anna (16) bis Marie (20)
(81,16,  1, '2025-11-03', 1), (82,16,  6, '2025-11-03', 1),
(83,16,  3, '2025-11-04', 1), (84,16,  7, '2025-11-04', 1),
(85,17,  4, '2025-11-03', 1), (86,17, 12, '2025-11-03', 2),
(87,17,  2, '2025-11-04', 1), (88,17,  6, '2025-11-04', 1),
(89,18,  3, '2025-11-03', 1), (90,18,  8, '2025-11-03', 1),
(91,18,  3, '2025-11-04', 1), (92,18, 10, '2025-11-04', 1),
(93,19,  4, '2025-11-03', 1), (94,19,  6, '2025-11-03', 1),
(95,19,  5, '2025-11-04', 1), (96,19,  9, '2025-11-04', 1),
(97,20,  1, '2025-11-03', 1), (98,20,  7, '2025-11-03', 1),
(99,20,  2, '2025-11-04', 1),(100,20,  8, '2025-11-04', 1);
