from PyQt6.QtWidgets import QWidget, QLCDNumber, QSlider, QDial
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6 import uic

class Burner(QWidget):
    slotValueFrostschutz = pyqtSlot(int)
    valueVorlauf = pyqtSlot(int)

    def __init__(self, parent=None):
        super(Burner, self).__init__(parent)

        uic.loadUi("burner.ui", self)

        self.dial_vorlauf = self.findChild(QDial, "dial_vorlauf")
        self.dial_ruecklauf = self.findChild(QDial, "dial_ruecklauf")
        self.dial_warmwasser = self.findChild(QDial, "dial_warmwasser")
        self.dial_frostschutz = self.findChild(QDial, "dial_frostschutz")

        self.lcdNumberVorlauf = self.findChild(QLCDNumber, "lcdNumberVorlauf")
        self.lcdNumberRuecklauf = self.findChild(QLCDNumber, "lcdNumberRuecklauf")

        self.dial_vorlauf.valueChanged.connect(self.valueVorlauf)
        self.dial_frostschutz.valueChanged.connect(self.slotValueFrostschutz)

    def valueVorlauf(self, soll):
        text = soll
        self.lcdNumberVorlauf.display(text)

    def valueRuecklauf(self, soll):
        text = soll
        self.lcdNumberRuecklauf.display(text)

    def valueWarmwasser(self, soll):
        pass

    def slotValueFrostschutz(self, liv, off, slee):
        self.living = liv
        self.office = off
        self.kit = slee
        print(self.living, self.kit, self.office)