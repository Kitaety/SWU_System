from Widgets.CommonPage import *
from Widgets.DataPage import *
from Widgets.GraphPage import *
from Widgets.SettingsPage import *
from PyQt5.QtWidgets import QStackedWidget
from Widgets.SWUStyle import *


class MyStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.common = CommonPage(self)
        self.data = DataPage(self)
        self.graph = GraphPage(self)
        self.settings = SettingsPage(self)
        self.init_ui()

    def init_ui(self):
        self.resize(ms_width, ms_height)
        self.setStyleSheet(BackgroundColor)

        self.addWidget(self.common)
        self.addWidget(self.data)
        self.addWidget(self.graph)
        self.addWidget(self.settings)
