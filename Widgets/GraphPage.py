from PyQt5.QtWidgets import QWidget
from Widgets.SWUWidgets import SWUButton
from Widgets.SWUStyle import *


class GraphPage(QWidget):
    def __init__(self, parent):
        super(GraphPage, self).__init__(parent=parent)
        self.setGeometry(0, tb_height, ms_width, ms_height)
