import sqlite3

class DatabaseConnector:
    def __init__(self, db_name='your_database_name.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()


    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year INTEGER
            )
        ''')
        self.conn.commit()

    def insert_sample_data(self):
        data = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
            ('To Kill a Mockingbird', 'Harper Lee', 1960),
            ('1984', 'George Orwell', 1949)
        ]
        self.cursor.executemany("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", data)
        self.conn.commit()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
