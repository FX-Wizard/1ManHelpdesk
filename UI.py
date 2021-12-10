#!/usr/bin/python3

import sys

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QMainWindow, QListWidgetItem, QFileDialog
from PySide2.QtUiTools import QUiLoader

# from mainwindow import Ui_MainWindow
from todoSql import ToDoDB
from configini import INIHandler


class MainDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uiFileName = './ui/mainwindow.ui'
        uiFile = QtCore.QFile(uiFileName)
        if not uiFile.open(QtCore.QIODevice.ReadOnly):
            print(f'Cannot open {uiFileName}: {uiFile.errorString()}')

        loader = QUiLoader()
        self.ui = loader.load(uiFile)
        uiFile.close()
        if not self.ui:
            print(loader.errorString())

        self.ui.show()

        # Check if DB exists and make it if it doesnt
        self.config = INIHandler("config.ini")
        dbFile = self.config.ini.general.db
        print(dbFile)
        try:
            self.connect = ToDoDB(dbFile)
            self.taskList()
        except:
            self.connect = ToDoDB(dbFile)
            self.connect.createNewDB()

        # connecting ui events to functions
        self.ui.actionNewTask.triggered.connect(self.newTask)
        self.ui.actionSaveTask.triggered.connect(self.saveTask)
        self.ui.actionOpenToDoList.triggered.connect(self.openToDoList)
        self.ui.actionNewToDoList.triggered.connect(self.newToDoList)
        self.ui.jobListWidget.currentItemChanged.connect(self.getTask)
        self.ui.jobStatCoBox.activated.connect(self.saveTask)
        self.ui.jobSortCoBox.activated.connect(self.taskList)
        self.ui.addJournalBtn.clicked.connect(self.addJournal)

        # set jobListWidget context menu policy
        self.ui.jobListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.jobListWidget.customContextMenuRequested.connect(self.contextMenuEvent)


    # Right click menu stuff
    def contextMenuEvent(self, pos):
        menu = QtWidgets.QMenu(self)
        mRename = menu.addAction("Rename")
        mRename.triggered.connect(self.renameTask)
        mDelete = menu.addAction("Delete")
        mDelete.triggered.connect(self.deleteTask)
        menu.exec_(self.ui.mapToGlobal(pos))


    # def mousePressEvent(self, event):
    #     print(event)
    #     if event.button() == QtCore.Qt.RightButton:
    #         print("right click was pressed")
    #     #super(MainDialog, self).mousePressEvent(event)


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
        try:
            self.connect.closeDB()
            self.connect = ToDoDB(openListDB[0])
            self.config.ini.general.db = openListDB[0]
            self.config.save()
            self.taskList()
        except:
            AlertDialog('cannot open db file')
            # raise Exception("cannot open db file")


    def newTask(self):
        self.saveTask()
        self.ui.jobListWidget.clearSelection()
        self.ui.jobNameEdit.setText('')
        self.ui.jobTextEdit.setText('')
        self.ui.journalListWidget.clear()


    def saveTask(self):
        taskName = self.jobNameEdit.text()
        taskBody = self.jobTextEdit.toHtml()
        taskStatus = self.jobStatCoBox.currentText()
        if len(taskName) > 0:
            self.connect.addData(taskName, taskBody, taskStatus)
            self.taskList()
            self.connect.saveDB()
        else:
            AlertDialog('Please enter name for this task')


    def taskList(self):
        listView = self.ui.jobListWidget
        listView.clear()

        sorting = self.ui.jobSortCoBox.currentText()
        itemList = self.connect.getDataName(sorting)

        for item in itemList:
            item = item[0]
            item = QListWidgetItem(item)
            listView.addItem(item)


    def getTask(self):
        try: # added to stop crash when the list was cleared and an item selected
            taskName = self.ui.jobListWidget.currentItem().text()
            self.ui.jobNameEdit.setText(taskName)
            taskBody = self.connect.getDataBody(taskName)
            self.ui.jobTextEdit.setText(taskBody[0])
            self.ui.jobStatCoBox.setCurrentIndex(self.ui.jobStatCoBox.findText(taskBody[1]))
            self.getJournal(taskName)
        except:
            print("Error getting body text from DB")


    def deleteTask(self):
        taskName = self.ui.jobListWidget.currentItem().text()
        self.connect.deleteData(taskName)
        self.taskList()


    def deleteJournal(self):
        print("this does nothing yet")


    def renameTask(self):
        taskName = self.ui.jobListWidget.currentItem()
        self.ui.jobListWidget.editItem(taskName)

    
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
        taskName = self.ui.jobListWidget.currentItem().text()
        journalBody = self.ui.journalLineEdit.text()
        if len(journalBody) > 0:
            self.connect.addJournal(taskName, journalBody)
            self.connect.saveDB()
            self.getJournal(taskName)
            self.ui.journalLineEdit.setText('')
        else:
            AlertDialog('Need to type something into the journal text thingy!')


    def clearAllFields(self):
        self.ui.jobListWidget.clear()
        self.ui.journalListWidget.clear()
        self.ui.jobNameEdit.clear()
        self.ui.jobTextEdit.clear()


class AlertDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Alert!')

        self.layout = QtWidgets.QVBoxLayout()
        messageLabel = QtWidgets.QLabel(message)

        self.layout.addWidget(messageLabel)
        button = QDialogButtonBox.Ok
        buttonBox = QDialogButtonBox(button)
        buttonBox.accepted.connect(self.accept)
        self.layout.addWidget(buttonBox)

        self.setLayout(self.layout)
        self.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainDialog()
    
    sys.exit(app.exec_())