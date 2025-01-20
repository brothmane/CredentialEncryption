from cryptography.fernet import Fernet
from db_mgmt import Account

db_name = "file.db"

class SessionVar:
    def __init__(self):
        self.db_name = db_name
        self.db_btn_state = "active"
        self.db_created = False
        self.tbl_dycript_state = False
        self.check_db()

    def check_db(self):
        account = Account(self.db_name)
        account.check_table()
        if account.exists_table:
            self.db_btn_state = "disabled"
            self.db_created = True

class AccountControl:
    def __init__(self):
        self.db_name = db_name
        self.name = None
        self.site = None
        self.password = None

    def set(self, name=str, site=str, password=str, key=str):
        try:
            fernet = Fernet(key.encode())
            self.name = fernet.encrypt(name.encode())
            self.site = site
            self.password = fernet.encrypt(password.encode())
            return True
        except:
            return False

    def create_db(self):
        account = Account(self.db_name)
        return account.create_table()
    
    def add(self):
        account = Account(self.db_name)
        account.set(self.name, self.site, self.password)
        return account.save()
            
    def edit(self, id, encrypt=False):
        if encrypt:
            account = Account(self.db_name)
            account.set(self.name, self.site, self.password)
            return account.update(id)
        
        else:
            return {"status": False, "msg": "Please encrypt data"}
        
    def remove(self, id):
        if id:
            account = Account(self.db_name)
            return account.delete(id)
        else:
            return {"status": False, "msg": "Please enter id"}
        
    def getall(self, key=None):
        account = Account(self.db_name)
        rtn_results = []
        account.check_table()    
        if not account.exists_table:
            return rtn_results
        if key:
            fernet = Fernet(key.encode())
            if account.getall()["status"]:
                results = account.result
                for result in results:
                    rtn_results.append({"id": result[0],
                                        "user": fernet.decrypt(result[2]).decode(),
                                        "site": result[1],
                                        "password": fernet.decrypt(result[3]).decode()})
                return rtn_results        
            else:
                return rtn_results  
        else:
            if account.getall()["status"]:
                results = account.result
                for result in results:
                    rtn_results.append({"id": result[0],
                                        "site": result[1],
                                        "user": result[2].decode(),
                                        "password": result[3].decode()})
                return rtn_results        
            else:
                return rtn_results
            

    def decrypt(self, Key=None):
        if Key:
            try:
                return self.getall(Key)
            except:
                return None
        else:
            return None

   