import sqlite3

class Account:
    def __init__(self, db_name=None):
        self.id = None
        self.user = None
        self.site = None
        self.password = None
        self.db_name = db_name
        self.result = None
        self.exists_table = None

    def set(self, user, site, password):
        self.user = user
        self.site = site
        self.password = password

    def connect(self):
        if self.db_name:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return True
        else:
            return False
    
    def check_table(self):
        if self.connect():
            cursor = self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='accounts';")
            self.exists_table = cursor.fetchall()[0][0]
            self.conn.commit()
            self.conn.close()
            return True
        else:
            return False

    def create_table(self):
        if self.connect():
            self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS accounts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                site TEXT,
                                user TEXT,
                                password TEXT
                                )
                                """)
            self.conn.commit()
            self.conn.close()
            return True
        else:
            return False
    
    def save(self):
        if self.connect():
            self.cursor.execute("""INSERT INTO accounts (site, user, password) VALUES(?, ?, ?);""", (self.site, self.user, self.password))
            self.conn.commit()
            self.conn.close()
            return {"status": True, "msg": "account create successfully"}
        else:
            return {"status": False, "msg": "error to connect database"}
    
    def update(self, id):
        if self.connect():
            self.cursor.execute("UPDATE accounts SET user=?, site=?, password=? WHERE id = ?;", (self.user, self.site, self.password, id,))
            self.conn.commit()
            self.conn.close()
            return {"status": True, "msg": "account updated successfully"}
        else:
            return {"status": False, "msg": "error to connect database"}
    
    def delete(self,id):
        if self.connect():
            self.cursor.execute("DELETE FROM accounts WHERE id = ?;", (id,))
            self.conn.commit()
            self.conn.close()
            return {"status": True, "msg": "account deleted successfully"}
        else:
            return {"status": False, "msg": "error to connect database"}

    def getall(self):
        if self.connect():
            cursor = self.cursor.execute("SELECT * FROM accounts;")
            self.result = cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            return {"status": True}
        else:
            return {"status": False, "msg": "error to connect database"}
