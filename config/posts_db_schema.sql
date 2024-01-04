CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    nazov TEXT,
    obrazok TEXT,
    alt TEXT,
    datum DATE,
    text TEXT,
    autor TEXT DEFAULT 'Neznámy'
);