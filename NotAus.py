from PyQt6.QtWidgets import QWidget, QLCDNumber, QSlider, QDial, QPushButton
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6 import uic

class NotAus(QWidget):

    signalNotaus = pyqtSignal(bool)
    slotNotauspressed = pyqtSlot()

    def __init__(self, parent=None):
        super(NotAus, self).__init__(parent)

        uic.loadUi("notaus.ui", self)

        self.notaus = self.findChild(QPushButton, "notaus")
        self.notaus.clicked.connect(self.notauspressed)


    def notauspressed(self):

            self.signalNotaus.emit(True)



