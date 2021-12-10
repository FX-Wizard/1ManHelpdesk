from PySide2.QtWidgets import QListWidget
from PySide2.QtWidgets import QMenu

class JournalWidget(QListWidget):
    def __init__(self, parent=None):
        super(JournalWidget, self).__init__(parent)


    def contextMenuEvent(self, event):
        menu = QMenu(self)
        mEdit = menu.addAction("Edit")
        mEdit.triggered.connect(lambda: print("nothing to see here"))
        mDelete = menu.addAction("Delete")
        mDelete.triggered.connect(lambda: print("nothing to see here"))
        menu.exec_(event.globalPos())