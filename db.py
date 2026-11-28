import logging
import os
import re
import sqlite3

# TODO: Alterar para 'billionaires.db' quando a Pessoa 2 entregar a BD final
DB_FILE = 'billionaires_mock.db'

DB = {}


def connect():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILE)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    DB['conn'] = conn
    logging.info('Connected to database: %s', path)


def execute(sql, args=None):
    if 'conn' not in DB:
        connect()
    sql = re.sub(r'\s+', ' ', sql).strip()
    logging.info('SQL: %s | Args: %s', sql, args)
    # Cursor novo por pedido para evitar conflitos quando o browser faz vários pedidos ao mesmo tempo
    cursor = DB['conn'].cursor()
    if args is not None:
        return cursor.execute(sql, args)
    return cursor.execute(sql)


def close():
    if 'conn' in DB:
        DB['conn'].close()
        del DB['conn']
