import sqlite3 
from datetime import datetime
import os

# by default file name
abs_path  = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
cloud_file = os.path.join(dir_path , "..\\data" , "cloud.db")
cloud_dir = os.path.dirname(cloud_file)

tellmetime = lambda : datetime.now().strftime("%d-%m-%y %H:%M:%S")


class cloudError(Exception):
    pass

class createTable:

    def __init__(self):

        # check whether the folder is exist or not
        if not os.path.isdir(cloud_dir):
            os.makedirs(cloud_dir,exist_ok=True) 
            
        # open the database
        self.connection = sqlite3.connect(cloud_file)
        self.cursor = self.connection.cursor()

    def __del__(self):
        # closing the database
        self.connection.commit()
        self.connection.close()

    def todo(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            tag TEXT DEFAULT 'IN-COMPLETED',
            datetime TEXT NOT NULL
        );
        '''
        self.cursor.execute(sql)
        self.connection.commit()
        return

    def dropTable(self, tableName):
        sql = f"""
        DROP TABLE {tableName}; 
        """
        self.cursor.execute(sql)
        self.connection.commit()
        return 
    
class TODO(createTable):

    def __init__(self):
        super().__init__()
        self.todo()
    
    def addData(self, task:str ,status:str , tag = None): 
        
        if tag is not None:
            sql = f"""INSERT INTO todos (task, status, tag, datetime) VALUES (?, ?, '{tag}', ?)"""
        else:
            sql = """INSERT INTO todos (task, status, datetime) VALUES (?, ?, ?)"""
        
        try:
            self.cursor.execute(sql, (task, status, tellmetime()))
        except Exception as e:
            print("error : ",e)
        # Commit to save the changes
        self.connection.commit()  
        
    def viewDatas(self,condition = None):
        sql = """SELECT * FROM todos"""  
        if condition != None:
            sql += " WHERE " + condition

        self.cursor.execute(sql)
        returnData = []
        for data in self.cursor.fetchall():
            returnData.append(data)
        return returnData

    def deleteData(self,**kwargs):
        # kwargs -> accept n number of args and store it as dict
        if "id" in kwargs:
            sql = """DELETE FROM todos WHERE id=?"""
            self.cursor.execute(sql, (kwargs["id"], ))
        elif "task" in kwargs:
            sql = """DELETE FROM todos WHERE task=?"""
            self.cursor.execute(sql, (kwargs["task"], ))
        else:
            raise Exception(f"argument key is wrong \n {kwargs}")
    
    def searchData(self,**kwargs):

        sql = ''

        if "id" in kwargs:
            sql = f"""SELECT * FROM todos WHERE id={kwargs["id"]}"""  
        elif "task" in kwargs:
            sql = f"""SELECT * FROM todos WHERE task='{kwargs["task"]}'"""  
        elif "status" in kwargs:
            sql = f"""SELECT * FROM todos WHERE status='{kwargs["status"]}'"""  
        
        self.cursor.execute(sql)
        returnData = []
        for data in self.cursor.fetchall():
            returnData.append(data)
        return returnData

    def updateData(self,id,**kwargs):

        if len(kwargs) == 0:
            raise cloudError("for updating todo table , no value is passed")

        keys = [
            f"{key}='{value}'" for key,value in kwargs.items()
        ]

        sql = f"""UPDATE todos SET {",".join(keys)} WHERE id = {id} """
    
        self.cursor.execute(sql)#,values)
        self.connection.commit()
