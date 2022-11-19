from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSlot, pyqtSignal
from Controller import Controller
from Heater import Heater
from Burner import Burner
from NotAus import NotAus


class HeatControlWidget(QWidget):
    slotReferenceValueKitchen = pyqtSlot(int)
    slotRealValueKitchen = pyqtSlot()

    slotReferenceValueLiving = pyqtSlot(int)
    slotRealValueLiving = pyqtSlot()

    slotReferenceValueOffice = pyqtSlot(int)
    slotRealValueOffice = pyqtSlot()

    signalRealValueKitchenChanged = pyqtSignal(int)
    signalRealValueLivingChanged = pyqtSignal(int)
    signalRealValueOfficeChanged = pyqtSignal(int)

    slotRealValueOutside = pyqtSlot(int)
    signalRealValueOutsideChnged = pyqtSignal(int)

    signalRuecklauf = pyqtSignal(int)
    signalVorlauf = pyqtSignal(int)

    def __init__(self, parent=None):
        super(HeatControlWidget, self).__init__(parent)

        self.heater = Heater(self)
        self.controller = Controller(self)
        self.burner = Burner(self)
        self.notaus = NotAus(self)
        self.signalVorlauf.connect(self.burner.valueVorlauf)
        self.signalRuecklauf.connect(self.burner.valueRuecklauf)

        # Kitchen
        self.timerKitchen = QTimer(self)
        self.timerKitchen.timeout.connect(self.slotRealValueKitchen)
        self.referenceValueKitchen = 0
        self.realValueKitchen = 0

        self.controller.changedTempKitchen.connect(self.slotReferenceValueKitchen)
        self.signalRealValueKitchenChanged.connect(self.heater.textKitchen)

        # Living
        self.timerLiving = QTimer(self)
        self.timerLiving.timeout.connect(self.slotRealValueLiving)
        self.referenceValueLiving = 0
        self.realValueLiving = 0

        self.controller.changedTempLiving.connect(self.slotReferenceValueLiving)
        self.signalRealValueLivingChanged.connect(self.heater.textLiving)


        # Office
        self.timerOffice = QTimer(self)
        self.timerOffice.timeout.connect(self.slotRealValueOffice)
        self.referenceValueOffice = 0
        self.realValueOffice = 0

        self.controller.changedTempOffice.connect(self.slotReferenceValueOffice)
        self.signalRealValueOfficeChanged.connect(self.heater.textOffice)
        self.signalRealValueOutsideChnged.connect(self.burner.slotValueFrostschutz)


        myLayout = QHBoxLayout(self)

        myLayout.addWidget(self.controller)
        myLayout.addWidget(self.heater)
        myLayout.addWidget(self.burner)
        myLayout.addWidget(self.notaus)

        self.setLayout(myLayout)

    def slotRealValueOutside(self, wert):
        temp = wert
        if temp < 5:
            self.signalRealValueOutsideChnged.emit(True)

    def slotReferenceValueKitchen(self, referenceValue: int):
        self.ruecklauf()
        self.referenceValueKitchen = referenceValue

        if self.timerKitchen.isActive() == False:
            self.timerKitchen.start(1 * 1000)

    def slotRealValueKitchen(self):
        if self.referenceValueKitchen > self.realValueKitchen:
            self.realValueKitchen += 1
        elif self.referenceValueKitchen < self.realValueKitchen:
            self.realValueKitchen -= 1
        else:
            self.timerKitchen.stop()

        self.signalRealValueKitchenChanged.emit(self.realValueKitchen)
        #print("Signal emited:", self.realValueKitchen)

    def slotReferenceValueLiving(self, referenceValue: int):
        self.ruecklauf()
        self.referenceValueLiving = referenceValue

        if self.timerLiving.isActive() == False:
            self.timerLiving.start(1 * 1000)

    def slotRealValueLiving(self):
        if self.referenceValueLiving > self.realValueLiving:
            self.realValueLiving += 1
        elif self.referenceValueLiving < self.realValueLiving:
            self.realValueLiving -= 1
        else:
            self.timerLiving.stop()

        self.signalRealValueLivingChanged.emit(self.realValueLiving)

    def slotReferenceValueOffice(self, referenceValue: int):
        self.ruecklauf()
        self.referenceValueOffice = referenceValue

        if self.timerOffice.isActive() == False:
            self.timerOffice.start(1 * 1000)

    def slotRealValueOffice(self):
        if self.referenceValueOffice > self.realValueOffice:
            self.realValueOffice += 1
        elif self.referenceValueOffice < self.realValueOffice:
            self.realValueOffice -= 1
        else:
            self.timerOffice.stop()

        self.signalRealValueOfficeChanged.emit(self.realValueOffice)

    def ruecklauf(self):
        if self.referenceValueOffice > self.referenceValueKitchen and self.referenceValueOffice > self.referenceValueLiving:
            self.tmpRuecklauf = self.referenceValueOffice + 5
            self.tmpVorlauf = self.tmpRuecklauf + 10
            self.signalRuecklauf.emit(self.tmpRuecklauf)
            self.signalVorlauf.emit(self.tmpVorlauf)

        if self.referenceValueLiving > self.referenceValueKitchen and self.referenceValueLiving > self.referenceValueOffice:
            self.tmpRuecklauf = self.referenceValueLiving + 5
            self.tmpVorlauf = self.tmpRuecklauf + 10
            self.signalRuecklauf.emit(self.tmpRuecklauf)
            self.signalVorlauf.emit(self.tmpVorlauf)

        if self.referenceValueKitchen > self.referenceValueLiving and self.referenceValueKitchen > self.referenceValueOffice:
            self.tmpRuecklauf = self.referenceValueKitchen + 5
            self.tmpVorlauf = self.tmpRuecklauf + 10
            self.signalRuecklauf.emit(self.tmpRuecklauf)
            self.signalVorlauf.emit(self.tmpVorlauf)

