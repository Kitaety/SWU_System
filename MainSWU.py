#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Utils.DataContainer import instance as DataContainer
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup
from Widgets.SWUWidgets import SWUMenuButton
from Widgets.SWUStyle import *
from Widgets.StackedWidget import *
from Widgets.InfoPanel import InfoPanel
# ----------------------------------------------------------------------------------------------------------------------
# MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, display_width, display_height)
        self.setWindowTitle('SWU')
        self.setStyleSheet(SecondaryBackgroundColor)

        # Top button menu
        self.btnCommon = SWUMenuButton(self, 'Общие', 0, 0)
        self.btnData = SWUMenuButton(self, 'Данные', 200, 0)
        self.btnGraph = SWUMenuButton(self, 'Графики', 400, 0)
        self.btnSettings = SWUMenuButton(self, 'Настройки', 600, 0)

        self.bgMenu = QButtonGroup(self)
        self.bgMenu.setExclusive(True)
        self.bgMenu.addButton(self.btnCommon, id=0)
        self.bgMenu.addButton(self.btnData, id=1)
        self.bgMenu.addButton(self.btnGraph, id=2)
        self.bgMenu.addButton(self.btnSettings, id=3)
        self.bgMenu.buttonClicked.connect(self.SetPage)

        self.btnCommon.setChecked(True)

        # Stacked Widget 'Main'
        self.stackMain = MyStackedWidget(self)
        self.stackMain.setGeometry(0, tb_height, ms_width, ms_height)
        self.stackMain.setObjectName("StackMain")
        self.stackMain.setCurrentIndex(0)
        self.stackMain.settings.minimizedBtn.clicked.connect(
            self.showMinimized)

        self.infoPanel = InfoPanel(self)
        self.infoPanel.setGeometry(0, tb_height+ms_height, display_width, 20)

    def SetPage(self):
        self.stackMain.setCurrentIndex(self.bgMenu.checkedId())
# ---------------------------------------------------------------------------------------------------------------------


def main():
    DataContainer.loadData()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    w = MainWindow()
    w.showFullScreen()
    sys.exit(app.exec_())


def exit():
    sys.exit()
