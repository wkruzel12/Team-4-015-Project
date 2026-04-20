DROP VIEW IF EXISTS menu_catalog;

CREATE TABLE IF NOT EXISTS bases (
    base_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    option_group TEXT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0,
    alt_price REAL,
    calories INTEGER NOT NULL DEFAULT 0,
    protein INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS proteins (
    protein_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL DEFAULT 'shared',
    name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0,
    alt_price REAL,
    calories INTEGER NOT NULL DEFAULT 0,
    protein INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS cheeses (
    cheese_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL DEFAULT 'shared',
    name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0,
    alt_price REAL,
    calories INTEGER NOT NULL DEFAULT 0,
    protein INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS toppings (
    topping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL DEFAULT 'shared',
    name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0,
    alt_price REAL,
    calories INTEGER NOT NULL DEFAULT 0,
    protein INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS extras (
    extra_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL DEFAULT 'shared',
    extra_type TEXT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0,
    alt_price REAL,
    calories INTEGER NOT NULL DEFAULT 0,
    protein INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE VIEW menu_catalog AS
SELECT
    'bases:' || base_id AS item_id,
    category,
    CASE option_group
        WHEN 'size' THEN 'entree'
        ELSE option_group
    END AS section,
    name,
    price,
    alt_price,
    calories,
    protein,
    description,
    active
FROM bases
UNION ALL
SELECT
    'proteins:' || protein_id AS item_id,
    category,
    'protein' AS section,
    name,
    price,
    alt_price,
    calories,
    protein,
    description,
    active
FROM proteins
UNION ALL
SELECT
    'cheeses:' || cheese_id AS item_id,
    category,
    'cheese' AS section,
    name,
    price,
    alt_price,
    calories,
    protein,
    description,
    active
FROM cheeses
UNION ALL
SELECT
    'toppings:' || topping_id AS item_id,
    category,
    'topping' AS section,
    name,
    price,
    alt_price,
    calories,
    protein,
    description,
    active
FROM toppings
UNION ALL
SELECT
    'extras:' || extra_id AS item_id,
    category,
    extra_type AS section,
    name,
    price,
    alt_price,
    calories,
    protein,
    description,
    active
FROM extras;
