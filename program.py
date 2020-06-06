from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
                             QMessageBox, QTextEdit)
from encodings.cp437 import decoding_map
from PyQt5.Qt import *
from PyQt5 import QtGui
import sys
import traceback
import re
import requests
baseLastPrice = "https://www.albion-online-data.com/api/v2/stats/prices/"
font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
font.setPointSize(10)
town_checked = []
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)

    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)

    sys.exit()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI()


    def setupUI(self):
        self.setupLabel()
        self.setupEditor()
        self.setupTable()
        self.setupButtons()
        self.setupSpinBox()
        self.setupCheckBox()
        self.setupComboBox()
        self.edit_string_name()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.editor, 0,0)
        grid.addWidget(self.buttonRequest, 0,1)
        grid.addWidget(self.table,2,0)
        grid.addWidget(self.label, 1,0)
        grid.addWidget(self.searchItem,1,1)
        grid.addWidget(self.groupTownBox, 1, 2)
        grid.addWidget(self.spinQualities,1,3)
        self.centralWidget.setLayout(grid)
    def setupSpinBox(self):
        self.spinQualities = QSpinBox(self)
        self.spinQualities.setMaximum(5)
        self.spinQualities.setMinimum(1)
        self.spinQualities.textChanged.connect(self.edit_string_name)
    def setupComboBox(self):
        self.searchItem = QLineEdit(self)
        strList = []
        file = open("items.txt", "r")
        for item in file:
            strList.append(item[:-1])
        completer = QCompleter(strList, self.searchItem)
        self.searchItem.setCompleter(completer)
        self.searchItem.setText("T1_HIDE")
        self.searchItem.textChanged.connect(self.edit_string_name)
        self.buttonRequest.setAutoDefault(True)  # click on <Enter>
        self.searchItem.returnPressed.connect(self.responseFromEdit)

    def setupTable(self):
        self.table = QTableWidget(self)
        self.table.setMaximumHeight(100)
    def setupCheckBox(self):
        self.groupTownBox = QGroupBox(self)
        self.groupTownBox.title()
        vbox = QVBoxLayout()
        self.groupTownBox.setLayout(vbox)
        check_0 = QCheckBox("BlackMarket")
        check_0.setChecked(True)
        vbox.addWidget(check_0)
        town_checked.append(check_0)
        check_1 = QCheckBox("BridgeWatch")
        town_checked.append(check_1)
        vbox.addWidget(check_1)
        check_2 = QCheckBox("Caerleon")
        town_checked.append(check_2)
        vbox.addWidget(check_2)
        check_3 = QCheckBox("ForestCross")
        town_checked.append(check_3)
        vbox.addWidget(check_3)
        check_4 = QCheckBox("FortSterling")
        town_checked.append(check_4)
        vbox.addWidget(check_4)
        check_5 = QCheckBox("Lymhurst")
        town_checked.append(check_5)
        vbox.addWidget(check_5)
        check_6 = QCheckBox("Martlock")
        town_checked.append(check_6)
        vbox.addWidget(check_6)
        check_7 = QCheckBox("Thetford")
        town_checked.append(check_7)
        vbox.addWidget(check_7)
        for item in town_checked:
            item.stateChanged.connect(self.edit_string_name)
    def setupEditor(self):
        self.editor = QLineEdit(self)
        self.editor.setFont(font)

    def setupButtons(self):
        self.buttonRequest = QPushButton("Request", self)
        self.buttonRequest.clicked.connect(self.responseFromEdit)

    def setupLabel(self):
        self.label = QLabel(self)
        self.label.setFont(font)
        self.label.setText("Wait request")
    def responseFromEdit(self):
        try:
            response = requests.get(self.editor.text())
            if response.status_code != 200:
                self.label.setText("Error request")
            else:
                self.label.setText("Nice request")
                result = response.json()
                self.table.setRowCount(len(result))
                max = len(result)*35
                if max > 100:
                    self.table.setMaximumHeight(max)
                self.table.setMinimumWidth(1000)
                self.table.setColumnCount(len(result[0]))
                headers = []
                for item in result[0]:
                    headers.append(item)
                self.table.setHorizontalHeaderLabels(headers)
                i = 0
                k = 0
                for item in result:
                    for bot_item in item:
                        self.table.setItem(i, k, QTableWidgetItem(str(item[bot_item])))
                        k += 1
                    k = 0
                    i += 1
                self.table.resizeColumnsToContents()
                self.table.resizeRowsToContents()
        except:
            self.label.setText("Error way")
    def edit_string_name(self):
        stringTowns = "?locations="
        for item in town_checked:
            if item.isChecked():
                stringTowns += item.text() +","
        stringQuality ="&qualities=" + self.spinQualities.text()
        self.editor.setText(baseLastPrice + self.searchItem.text() + stringTowns + stringQuality)
        #self.responseFromEdit()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 1024)
    window.show()
    sys.exit(app.exec_())
