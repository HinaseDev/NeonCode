from ui import *
import os
import easygui
import mimetypes
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.formatters import HtmlFormatter


class QNeon(Ui_QNeonCode):
    def setupUi(self, QNeonCode, path=os.path.expanduser("~")):
        super().setupUi(QNeonCode)
        self.window = QNeonCode
        self.subpath = ""
        self.filenames = {}
        self.path = path
        self.populate()
        self.actionSave.triggered.connect(lambda: self.save())
        self.actionSave.setShortcut(QtGui.QKeySequence("Ctrl+S"))
        self.actionSave_as.triggered.connect(lambda: self.saveAs())
        self.actionSave_as.setShortcut(QtGui.QKeySequence("Ctrl+Shift+S"))
        self.openNow = ""
        self.actionNew_File.triggered.connect(lambda: self.new())
        self.actionNew_File.setShortcut(QtGui.QKeySequence("Ctrl+N"))
        self.actionOpen_Folder.triggered.connect(lambda: self.OpenFolder())
        self.actionOpen_Folder.setShortcut(QtGui.QKeySequence("Ctrl+K+O"))

    def populate(self):
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(QtCore.QDir.rootPath())
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(self.path))
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.hideColumn(4)
        self.treeView.clicked.connect(lambda: self.openF())
        self.window.update()
        self.textEdits = {}
        self.fsmodel = model

    def save(self):
        if self.openNow:
            with open(self.openNow, "w+") as f:
                f.write(self.textEdits[self.openNow].toPlainText())
        else:
            d = easygui.filesavebox("Enter Filename to be saved as", "Save as...", filetypes=[["*.py", "*.pyw", "Python File"], ["*.java", "*jav", "Java Source File"], ["*.js", "JavaScript File"], [
                                    "SQL Database Schema", "*.sql", "*.schem"], ["*.c", "C Source File"], ["*.h", "C/C++ Header"], ["*.cpp", "*.cxx", "*.c++", "C++ Source File"], ["*.hpp", "C++ Header File"]])
            if d:
                self.textEdits[d] = self.textEdits.pop("untitled")
                self.openNow = d
                self.save()

    def saveAs(self):

        d = easygui.filesavebox("Enter Filename to be saved as", "Save as...", filetypes=[["*.py", "*.pyw", "Python File"], ["*.java", "*jav", "Java Source File"], ["*.js", "JavaScript File"], [
                                "SQL Database Schema", "*.sql", "*.schem"], ["*.c", "C Source File"], ["*.h", "C/C++ Header"], ["*.cpp", "*.cxx", "*.c++", "C++ Source File"], ["*.hpp", "C++ Header File"]])
        if d:
            self.openNow = d
        self.treeView.reset()
        self.populate()

    def OpenFolder(self):
        dialog = QtWidgets.QFileDialog
        self.setupUi(self.window, dialog.getExistingDirectory())

    def new(self):
        path = "untitled"
        print(path)
        tab = QtWidgets.QWidget()
        self.tabs[path] = tab
        self.openNow = None
        self.textEdits[path] = QtWidgets.QTextEdit(tab)
        self.textEdits[path].setGeometry(QtCore.QRect(0, 0, 591, 491))
        self.textEdits[path].setObjectName("textEdit")
        self.tabWidget.addTab(tab, path)
        try:
            te: QtWidgets.QTextEdit = self.textEdits[path]
            te.setText("")
        except:
            self.textEdits[path].setText(
                f"MIMEType of {path} is not Text-Like.")

    def openF(self):

        index = self.treeView.selectedIndexes()[0]
        path = self.fsmodel.itemData(index)[0]
        print(path)
        if os.path.isdir(self.fsmodel.filePath(index)):
            return
        tab = QtWidgets.QWidget()
        self.tabs[path] = tab
        self.openNow = self.fsmodel.filePath(index)
        self.textEdits[path] = QtWidgets.QTextEdit(tab)
        self.textEdits[path].setGeometry(QtCore.QRect(0, 0, 591, 491))
        self.textEdits[path].setObjectName("textEdit")
        self.tabWidget.addTab(tab, os.path.basename(path))
        try:
            lexer = get_lexer_for_filename(path)
            if not lexer:
                lexer = guess_lexer(open(self.fsmodel.filePath(index)).read())
            print(lexer)
            text = open(self.fsmodel.filePath(index)).read()
            te: QtWidgets.QTextEdit = self.textEdits[path]
            te.setHtml(highlight(text, lexer, HtmlFormatter()))
        except:
            self.textEdits[path].setText(
                f"MIMEType of {path} is not Text-Like.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = QtWidgets.QMainWindow()
    QNeon().setupUi(win)
    win.show()
    exit(app.exec_())
