from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSlot, pyqtSignal
from Controller import Controller
from Heater import Heater


class HeatControlWidget(QWidget):
    slotReferenceValueKitchen = pyqtSlot(int)
    slotRealValueKitchen = pyqtSlot()
    slotReferenceValueLiving = pyqtSlot(int)
    slotRealValueLiving = pyqtSlot()

    signalRealValueKitchenChanged = pyqtSignal(int)
    signalRealValueLivingChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(HeatControlWidget, self).__init__(parent)

        self.heater = Heater(self)
        self.controller = Controller(self)

        # Kitchen
        self.timerKitchen = QTimer(self)
        self.timerKitchen.timeout.connect(self.slotRealValueKitchen)
        self.referenceValueKitchen = 0
        self.realValueKitchen = 0

        self.controller.changedTempKitchen.connect(self.slotReferenceValueKitchen)
        self.signalRealValueKitchenChanged.connect(self.heater.textKitchen)

        self.controller.changedTempOffice.connect(self.heater.textOffice)
        self.controller.changedTempLiving.connect(self.heater.textLiving)

        # Living
        self.timerKitchen = QTimer(self)
        self.timerKitchen.timeout.connect(self.slotRealValueKitchen)
        self.referenceValueKitchen = 0
        self.realValueKitchen = 0

        self.controller.changedTempKitchen.connect(self.slotReferenceValueKitchen)
        self.signalRealValueKitchenChanged.connect(self.heater.textKitchen)

        self.controller.changedTempOffice.connect(self.heater.textOffice)
        self.controller.changedTempLiving.connect(self.heater.textLiving)

        myLayout = QHBoxLayout(self)

        myLayout.addWidget(self.controller)
        myLayout.addWidget(self.heater)

        self.setLayout(myLayout)

    def slotReferenceValueKitchen(self, referenceValue: int):
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