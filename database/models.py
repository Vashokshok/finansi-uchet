import sqlite3


conn = sqlite3.connect('finansi.db')
cur = conn.cursor()


cur.execute(''' 
CREATE TABLE IF NOT EXISTS finans(
            user_id INTEGER,
            id INTEGER PRIMARY KEY,
            date INTEGER,
            nazvanie TEXT,
            summa INTEGER,
            opisanie TEXT
            )''')


conn.commit()
conn.close()