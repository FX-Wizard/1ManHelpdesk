import sqlite3
import datetime


class ToDoDB:
    def __init__(self, dbName):

        self.dbName = dbName

        try:
            self.db = sqlite3.connect(dbName)
            self.cur = self.db.cursor()
        except:
            print("cannot connect to DB: " + dbName)


    def saveDB(self):
        try:
            self.db.commit()
        except:
            print("unable to save DB")


    def addData(self, title, body, status):
        self.cur.execute("SELECT title FROM List WHERE title = ?", (title,))
        titleExitst = self.cur.fetchone()
        if titleExitst:
            self.cur.execute("UPDATE List SET body = ?, status = ?, title = ? WHERE title = ?", (body, status, title, title))
        else:
            time = self.getDateTime()
            self.cur.execute("INSERT INTO List (title, body, status, datetime) values (?, ?, ?, ?)", (title, body, status, time))

    
    def addJournal(self, title, body):
        time = self.getDateTime()
        self.cur.execute("INSERT INTO journal (title, body, datetime) values (?, ?, ?)", (title, body, time))


    def getDataName(self, sorting):
        if sorting == "Open":
            self.cur.execute('SELECT title FROM List WHERE status="Have not looked at" OR status="Pending" OR status="In Progress"')
            return self.cur.fetchall()
        elif sorting == "Completed":
            self.cur.execute('SELECT title FROM List WHERE status = "Complete"')
            return self.cur.fetchall()
        else:
            taskNames = self.cur.execute("SELECT title FROM List")
            return taskNames
        

    def getDataBody(self, name):
        self.cur.execute("SELECT body, status FROM List WHERE title=?", (name,))
        taskBody = self.cur.fetchone()
        return taskBody


    def getJournal(self, name):
        self.cur.execute("SELECT body, datetime FROM journal WHERE title=?", (name,))
        journalBody = self.cur.fetchall()
        return journalBody


    def createNewDB(self):
        try:
            self.cur.execute("CREATE TABLE List (Id INT, title TEXT, datetime INT, body TEXT, status TEXT, priority TEXT)")
            self.cur.execute("CREATE TABLE journal (Id INT, title TEXT, datetime INT, body TEXT)")
        except:
            print("error")


    def getDateTime(self):
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return time


    def deleteData(self, name):
        self.cur.execute("DELETE FROM List WHERE title = ?", (name,))
        self.saveDB()

    
    def closeDB(self):
        self.db.commit()
        self.db.close()
