import sqlite3
import pathlib

p = pathlib.Path(__file__).resolve().parents[1] / 'data' / 'app.db'
print('DB path:', str(p))
print('Exists:', p.exists())
if p.exists():
    conn = sqlite3.connect(str(p))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print('Tables:', tables)
    conn.close()
