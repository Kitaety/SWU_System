from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QCoreApplication
from Widgets.SWUWidgets import SWUButton, SWUCombobox, Label
from Widgets.SWUStyle import *
from Utils.DataContainer import instance as DataContainer


class SettingsPage(QWidget):
    def __init__(self, parent):
        super(SettingsPage, self).__init__(parent=parent)
        self.setGeometry(0, tb_height, ms_width, ms_height)

        self.exitBtn = SWUButton(
            self, 'Завершить работу', 590, display_height - tb_height - 90, 200, 50, False)
        self.exitBtn.clicked.connect(exit)

        self.minimizedBtn = SWUButton(
            self, 'Свернуть', 590, display_height - tb_height - 150, 200, 50, True)

        self.selectedPortBox = SWUCombobox(self, 10, 10)
        self.lab1 = Label("Выбор порта", self)
        self.lab1.setGeometry(210, 10, 48, 200)


def exit():
    DataContainer.dispose()
    QCoreApplication.instance().quit()
