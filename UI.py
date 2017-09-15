import sys
import os.path

from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMenu, QFileDialog
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi

from todoSql import ToDoDB


class MainDialog(QMainWindow):
    def __init__(self):
        super(MainDialog, self).__init__()

        loadUi("main.ui", self)

        # Check if DB exists and make it if it doesnt
        if os.path.isfile("toDoData.tdl"):
            self.connect = ToDoDB("toDoData.tdl")
            self.taskList()
        else:
            self.connect = ToDoDB("toDoData.tdl")
            self.connect.createNewDB()

        # connecting ui events to functions
        self.actionNewTask.triggered.connect(self.newTask)
        self.actionSaveTask.triggered.connect(self.saveTask)
        self.actionOpenToDoList.triggered.connect(self.openToDoList)
        self.actionNewToDoList.triggered.connect(self.newToDoList)
        self.jobListWidget.currentItemChanged.connect(self.getTask)
        self.jobStatCoBox.activated.connect(self.saveTask)
        self.jobSortCoBox.activated.connect(self.taskList)
        self.addJournalBtn.clicked.connect(self.addJournal)


    # Right click menu stuff
    def contextMenuEvent(self, event):
        print("LOOK AT ME!!!")
        print(event)
        menu = QMenu(self)
        print(QCursor.pos())
        mRename = menu.addAction("Rename")
        mRename.triggered.connect(self.renameTask)
        mDelete = menu.addAction("Delete")
        mDelete.triggered.connect(self.deleteTask)
        menu.exec_(event.globalPos())


    def newToDoList(self):
        newListDB = QFileDialog.getSaveFileName(self, "New To Do List", "", "*To Do List (*.tdl)")
        if newListDB[0]:
            self.connect.closeDB()
            newListDB = newListDB[0] + ".tdl"
            self.connect = ToDoDB(newListDB)
            self.connect.createNewDB()
            self.clearAllFields()


    def openToDoList(self):
        openListDB = QFileDialog.getOpenFileName(self, "Open To Do List", "", "To Do List (*.tdl)")
        if openListDB[0]:
            self.connect.closeDB()
            self.connect = ToDoDB(openListDB[0])
            self.taskList()


    def newTask(self):
        self.saveTask()
        self.jobListWidget.clearSelection()
        self.jobNameEdit.setText("")
        self.jobTextEdit.setText("")
        self.journalListWidget.clear()


    def saveTask(self):
        taskName = self.jobNameEdit.text()
        taskBody = self.jobTextEdit.toHtml()
        taskStatus = self.jobStatCoBox.currentText()
        if len(taskName) > 0:
            self.connect.addData(taskName, taskBody, taskStatus)
            self.taskList()
            self.connect.saveDB()
        else:
            print("need an error message to pop up and say, hey there is no name for this task")


    def taskList(self):
        listView = self.jobListWidget
        listView.clear()

        sorting = self.jobSortCoBox.currentText()
        itemList = self.connect.getDataName(sorting)

        for item in itemList:
            item = item[0]
            item = QListWidgetItem(item)
            listView.addItem(item)


    def getTask(self):
        try: # added to stop crash when the list was cleared and an item selected
            taskName = self.jobListWidget.currentItem().text()
            self.jobNameEdit.setText(taskName)
            taskBody = self.connect.getDataBody(taskName)
            self.jobTextEdit.setText(taskBody[0])
            self.jobStatCoBox.setCurrentIndex(self.jobStatCoBox.findText(taskBody[1]))
            self.getJournal(taskName)
        
        except:
            print("Error getting body text from DB")


    def deleteTask(self):
        taskName = self.jobListWidget.currentItem().text()
        self.connect.deleteData(taskName)
        self.taskList()


    def deleteJournal(self):
        print("this does nothing yet")


    def renameTask(self):
        taskName = self.jobListWidget.currentItem()
        self.jobListWidget.editItem(taskName)

    
    def getJournal(self, taskName):
        journalBody = self.connect.getJournal(taskName)
        listView = self.journalListWidget
        listView.clear()

        for entry in journalBody:
            #entry = entry[0]
            print(entry[1])
            entry = QListWidgetItem(entry[0])
            listView.addItem(entry)


    def addJournal(self):
        taskName = self.jobListWidget.currentItem().text()
        journalBody = self.journalLineEdit.text()
        if len(journalBody) > 0:
            self.connect.addJournal(taskName, journalBody)
            self.connect.saveDB()
            self.getJournal(taskName)
            self.journalLineEdit.setText("")
        else:
            print("Need to type something into the journal text thingy!")


    def clearAllFields(self):
        self.jobListWidget.clear()
        self.journalListWidget.clear()
        self.jobNameEdit.clear()
        self.jobTextEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())
