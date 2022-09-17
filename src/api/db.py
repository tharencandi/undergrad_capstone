from flask import g
import sqlite3

DATABASE="database.db"
SCHEMAS="schemas.sql"

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db
  
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db(flask_app):
    with app.context():
        db = get_db()
        with app.open_resources(SCHEMAS, mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

