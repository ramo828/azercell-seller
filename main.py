from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtGui import QTextCursor
from ui import Ui_MainWindow
import sys
import threading as td
from library import Azercell

class Pencere(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Follow Bot")
        self.setupUi(self)
        self.az = Azercell()
        self.price_min.valueChanged.connect(self.setMinPrice)
        self.min_price.textChanged.connect(self.setMinSlider)
        self.price_max.valueChanged.connect(self.setMaxPrice)
        self.max_price.textChanged.connect(self.setMaxSlider)
        self.search.clicked.connect(self.searching)
        self.az.log.connect(self.writeEnd)
        self.az.debug.connect(self.writeDebug)



    def setMinPrice(self, value):
        print("ok ", value)
        self.min_price.setText(str(value))
    
    def setMinSlider(self, value):
        if(value == ''):
            value = 0
        self.price_min.setValue(int(value))
    
    def setMaxPrice(self, value):
        print("ok ", value)
        self.max_price.setText(str(value))
    
    def setMaxSlider(self, value):
        if(value == ''):
            value = 0
        self.price_max.setValue(int(value))

    def searching(self):
        self.thread = td.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        self.terminal.clear()
        self.debug.clear()
        self.az.prefix = 10
        self.az.splitPrice(number=self.number.text().replace("-",""),
        min=int(self.min_price.text()),
        max=int(self.max_price.text()))


    def writeEnd(self,message):
            cursor1 = QTextCursor(self.terminal.textCursor())
            cursor1.movePosition(cursor1.MoveOperation.Down)
            self.terminal.setTextCursor(cursor1)
            self.terminal.insertPlainText(message)

    
    def writeDebug(self,message):
            cursor1 = QTextCursor(self.debug.textCursor())
            cursor1.movePosition(cursor1.MoveOperation.Down)
            self.debug.setTextCursor(cursor1)
            self.debug.insertPlainText(message)

app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec())
