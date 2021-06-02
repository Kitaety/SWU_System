from PyQt5.QtCore import Qt
from Data.Detector import Detector
from typing import List
from PyQt5.QtWidgets import QWidget
from Widgets.SWUWidgets import Label, SWUTimePanel
from Widgets.SWUStyle import *
from Utils.DataContainer import instance as DataContainer


class CommonPage(QWidget):
    def __init__(self, parent):
        super(CommonPage, self).__init__(parent=parent)
        self.setGeometry(0, tb_height, ms_width, ms_height)
        self.time = SWUTimePanel(self, 530, 10)

        self.detectorValueLabels: List[Label] = list()
        self.detectorNameLabels: List[Label] = list()

        for detector in DataContainer.detectors:
            d: Detector = detector
            labelName = Label(d.name, self, 350, textAlignment=Qt.AlignLeft)
            labelValue = Label(str(d.value), self, 150)

            labelName.move(10, 10 + (len(self.detectorNameLabels)*52))
            labelValue.move(360, 10 + (len(self.detectorNameLabels)*52))

            self.detectorNameLabels.append(labelName)
            self.detectorValueLabels.append(labelValue)

            d.updated.connect(labelValue.setText)
