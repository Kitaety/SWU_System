from PyQt5.QtWidgets import QWidget
from Widgets.SWUWidgets import SWUButton
from Widgets.SWUStyle import *


class DataPage(QWidget):
    def __init__(self, parent):
        super(DataPage, self).__init__(parent=parent)
        self.setGeometry(0, tb_height, ms_width, ms_height)
