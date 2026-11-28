#! /usr/bin/python3
"""
Gera uma base de dados SQLite TEMPORÁRIA (billionaires_mock.db) com dados fictícios
inspirados no Billionaires Statistics Dataset para desenvolvimento e testes da app Flask.

NOTA: Substituir/apagar quando a Pessoa 2 entregar o esquema final e billionaires.db.
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'billionaires_mock.db')


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS billionaires;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS industries;
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    gdp_billion_usd REAL,
    population INTEGER,
    tax_rate REAL,
    cpi REAL
);

CREATE TABLE industries (
    industry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE organizations (
    organization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    industry_id INTEGER NOT NULL,
    hq_country_id INTEGER NOT NULL,
    FOREIGN KEY (industry_id) REFERENCES industries(industry_id),
    FOREIGN KEY (hq_country_id) REFERENCES countries(country_id)
);

CREATE TABLE billionaires (
    billionaire_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    net_worth_million INTEGER NOT NULL CHECK (net_worth_million >= 0),
    age INTEGER CHECK (age > 0),
    gender TEXT CHECK (gender IN ('M', 'F')),
    self_made INTEGER NOT NULL CHECK (self_made IN (0, 1)),
    source TEXT NOT NULL,
    citizenship_country_id INTEGER NOT NULL,
    residence_country_id INTEGER NOT NULL,
    industry_id INTEGER NOT NULL,
    organization_id INTEGER,
    FOREIGN KEY (citizenship_country_id) REFERENCES countries(country_id),
    FOREIGN KEY (residence_country_id) REFERENCES countries(country_id),
    FOREIGN KEY (industry_id) REFERENCES industries(industry_id),
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);
"""


COUNTRIES = [
    (1, 'France', 'Europe', 2957.9, 67750000, 45.0, 110.05),
    (2, 'United States', 'North America', 25462.7, 333287557, 37.0, 117.24),
    (3, 'Spain', 'Europe', 1427.4, 47415750, 47.0, 110.96),
    (4, 'Mexico', 'North America', 1414.2, 127504125, 35.0, 141.54),
    (5, 'India', 'Asia', 3385.1, 1417173173, 42.7, 180.44),
    (6, 'China', 'Asia', 17963.2, 1412175000, 45.0, 125.08),
    (7, 'Portugal', 'Europe', 255.2, 10352042, 48.0, 107.84),
]

INDUSTRIES = [
    (1, 'Fashion & Retail'),
    (2, 'Automotive'),
    (3, 'Technology'),
    (4, 'Finance & Investments'),
    (5, 'Telecom'),
    (6, 'Diversified'),
]

ORGANIZATIONS = [
    (1, 'LVMH', 1, 1),
    (2, 'Tesla', 2, 2),
    (3, 'Amazon', 3, 2),
    (4, 'Oracle', 3, 2),
    (5, 'Berkshire Hathaway', 4, 2),
    (6, 'Microsoft', 3, 2),
    (7, 'Inditex', 1, 3),
    (8, 'América Móvil', 5, 4),
    (9, 'Reliance Industries', 6, 5),
    (10, 'L\'Oréal', 1, 1),
    (11, 'ByteDance', 3, 6),
    (12, 'Amorim Investimentos', 6, 7),
]

BILLIONAIRES = [
    (1, 1, 'Bernard Arnault & family', 211000, 74, 'M', 0, 'LVMH', 1, 1, 1, 1),
    (2, 2, 'Elon Musk', 180000, 51, 'M', 1, 'Tesla, SpaceX', 2, 2, 2, 2),
    (3, 3, 'Jeff Bezos', 114000, 59, 'M', 1, 'Amazon', 2, 2, 3, 3),
    (4, 4, 'Larry Ellison', 107000, 78, 'M', 1, 'Oracle', 2, 2, 3, 4),
    (5, 5, 'Warren Buffett', 106000, 92, 'M', 1, 'Berkshire Hathaway', 2, 2, 4, 5),
    (6, 6, 'Bill Gates', 104000, 67, 'M', 1, 'Microsoft', 2, 2, 3, 6),
    (7, 8, 'Carlos Slim Helu & family', 93000, 83, 'M', 1, 'Telecom', 4, 4, 5, 8),
    (8, 9, 'Mukesh Ambani', 83400, 65, 'M', 0, 'Diversified', 5, 5, 6, 9),
    (9, 11, 'Francoise Bettencourt Meyers & family', 80500, 69, 'F', 0, 'L\'Oréal', 1, 1, 1, 10),
    (10, 13, 'Amancio Ortega', 77300, 87, 'M', 1, 'Zara', 3, 3, 1, 7),
    (11, 26, 'Zhang Yiming', 45000, 39, 'M', 1, 'TikTok', 6, 6, 3, 11),
    (12, 534, 'Maria Fernanda Amorim & family', 5000, 88, 'F', 0, 'Energy, investments', 7, 7, 6, 12),
]


def build():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.executemany(
            'INSERT INTO countries (country_id, name, region, gdp_billion_usd, population, tax_rate, cpi) VALUES (?, ?, ?, ?, ?, ?, ?)',
            COUNTRIES,
        )
        conn.executemany(
            'INSERT INTO industries (industry_id, name) VALUES (?, ?)',
            INDUSTRIES,
        )
        conn.executemany(
            'INSERT INTO organizations (organization_id, name, industry_id, hq_country_id) VALUES (?, ?, ?, ?)',
            ORGANIZATIONS,
        )
        conn.executemany(
            """
            INSERT INTO billionaires (
                billionaire_id, rank, full_name, net_worth_million, age, gender,
                self_made, source, citizenship_country_id, residence_country_id,
                industry_id, organization_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            BILLIONAIRES,
        )
        conn.commit()
        fk_errors = conn.execute('PRAGMA foreign_key_check').fetchall()
        assert not fk_errors, f'Foreign key errors: {fk_errors}'
        print(f'Mock DB criada com sucesso em: {DB_PATH}')
    finally:
        conn.close()


if __name__ == '__main__':
    build()
