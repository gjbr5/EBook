import sqlite3

class database:
    def __init__(self):
        self.conn = sqlite3.connect('list.db', check_same_thread=False)
        self.c = self.conn.cursor()
        
    def execute(self, query):
        return self.c.execute(query)
        
    def __del__(self):
        self.conn.close()

