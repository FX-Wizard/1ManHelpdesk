#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
__license__ = 'MIT'
__copyright__ = '2009, John Schember '
__docformat__ = 'restructuredtext en'
 
import re
import sys
 
import enchant
 
from PyQt4.Qt import QAction
from PyQt4.Qt import QApplication
from PyQt4.Qt import QEvent
from PyQt4.Qt import QMenu
from PyQt4.Qt import QMouseEvent
from PyQt4.Qt import QPlainTextEdit
from PyQt4.Qt import QSyntaxHighlighter
from PyQt4.Qt import QTextCharFormat
from PyQt4.Qt import QTextCursor
from PyQt4.Qt import Qt
from PyQt4.QtCore import pyqtSignal
 
class SpellTextEdit(QPlainTextEdit):
 
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)
 
        # Default dictionary based on the current locale.
        self.dict = enchant.Dict()
        self.highlighter = Highlighter(self.document())
        self.highlighter.setDict(self.dict)
 
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QPlainTextEdit.mousePressEvent(self, event)
 
    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()
 
        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
 
        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if self.textCursor().hasSelection():
            text = unicode(self.textCursor().selectedText())
            if not self.dict.check(text):
                spell_menu = QMenu('Spelling Suggestions')
                for word in self.dict.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                if len(spell_menu.actions()) != 0:
                    popup_menu.insertSeparator(popup_menu.actions()[0])
                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
 
        popup_menu.exec_(event.globalPos())
 
    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()
 
        cursor.removeSelectedText()
        cursor.insertText(word)
 
        cursor.endEditBlock()
 
 
class Highlighter(QSyntaxHighlighter):
 
    WORDS = u'(?iu)[\w\']+'
 
    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)
 
        self.dict = None
 
    def setDict(self, dict):
        self.dict = dict
 
    def highlightBlock(self, text):
        if not self.dict:
            return
 
        text = unicode(text)
 
        format = QTextCharFormat()
        format.setUnderlineColor(Qt.red)
        format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
 
        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), format)
 
 
class SpellAction(QAction):
 
    '''
    A special QAction that returns the text in a signal.
    '''
 
    correct = pyqtSignal(unicode)
 
    def __init__(self, *args):
        QAction.__init__(self, *args)
 
        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))
 
 
def main(args=sys.argv):
    app = QApplication(args)
 
    spellEdit = SpellTextEdit()
    spellEdit.show()
 
    return app.exec_()
 
if __name__ == '__main__':
    sys.exit(main())