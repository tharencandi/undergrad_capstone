from flask import Flask, g
import sys, os
import sqlite3
from db import init_db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__=="__main__":
    # create app and init db
    app = Flask(__name__)
    init_db(app)

    app.run()