import sqlite3
import os
import pathlib


def init_db():
    # Ensure data dir exists and determine DB path
    base_dir = pathlib.Path(__file__).resolve().parents[1]
    data_dir = base_dir / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / 'app.db'

    # Connect to SQLite (file will be created if not exists)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Execute create_tables.sql and seed_data.sql if present
    sql_dir = base_dir / 'sql' / 'Estruturas'
    create_file = sql_dir / 'create_tables.sql'
    seed_file = sql_dir / 'seed_data.sql'

    # Also apply SQL files from the Tabelas folder if present
    tabelas_dir = sql_dir / 'Tabelas'
    if tabelas_dir.exists():
        for f in tabelas_dir.glob('*.sql'):
            with f.open('r', encoding='utf-8') as fh:
                try:
                    cursor.executescript(fh.read())
                except sqlite3.OperationalError as e:
                    print(f'Warning executing {f.name}:', e)

    if create_file.exists():
        with create_file.open('r', encoding='utf-8') as f:
            sql = f.read()
            try:
                cursor.executescript(sql)
            except sqlite3.OperationalError as e:
                print('Warning executing create_tables.sql:', e)

    if seed_file.exists():
        with seed_file.open('r', encoding='utf-8') as f:
            sql = f.read()
            try:
                cursor.executescript(sql)
            except sqlite3.OperationalError as e:
                print('Warning executing seed_data.sql:', e)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()