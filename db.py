import sqlite3

conn = sqlite3.connect('hadiths_db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS hadith (
                    id INTEGER PRIMARY KEY,
                    narrator TEXT,
                    text_details TEXT
                )''')

