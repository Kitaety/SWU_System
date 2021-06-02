from Utils.DataContainer import instance as DataContainer
from PyQt5.QtWidgets import QFrame, QAction, QActionGroup, QMenu, QPushButton, QLabel, QWidget, QToolButton
from PyQt5.QtCore import Qt, QDate, QTime, QTimer
from Widgets.SWUStyle import *
from Utils.Serial import getPorts
# ---------------------------------------------------------------------------------------------------------------------
# SWUButton


class SWUButton(QPushButton):
    def __init__(self, parent, text: str, posX: int, posY: int, w: int, h: int, flat: bool):
        super(SWUButton, self).__init__(parent=parent, text=text)
        self.move(posX, posY)
        self.setFixedSize(w, h)
        self.setFlat(flat)
        self.setStyleSheet(ButtonStyle)
        self.setFont(getFont(20, 'Medium'))


# ---------------------------------------------------------------------------------------------------------------------
# SWUMenuButton

class SWUMenuButton(SWUButton):
    def __init__(self, parent, text: str, posX: int, posY: int):
        super(SWUMenuButton, self).__init__(
            parent, text, posX, posY, tb_width, tb_height, True)
        self.setStyleSheet(ButtonMenuStyle)
        self.setFont(getFont(24, 'Medium'))
        self.make_flat_check()

    def make_flat_check(self):
        self.setFlat(True)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)

# ---------------------------------------------------------------------------------------------------------------------
# SWUTimePanel


class SWUTimePanel(QWidget):
    def __init__(self, parent=None, ax: int = 0, ay: int = 0):
        super().__init__(parent)
        self.setStyleSheet(SecondaryBackgroundColor)

        self.frame = QFrame(self)
        self.frame.setGeometry(ax, ay, 255, 80)

        self.date = QLabel(self.frame)
        self.time = QLabel(self.frame)

        self.date.setStyleSheet('QLabel {color: '+TextPrimaryColor+';}')
        self.date.setFont(getFont(20, 'Medium'))
        self.date.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.date.setGeometry(100, 0, 120, 30)

        self.time.setStyleSheet('QLabel {color: '+TextPrimaryColor+';}')
        self.time.setFont(getFont(24, 'Medium'))
        self.time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.time.setGeometry(100, 40, 120, 30)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setTime)
        self.timer.start(1000)

        self.setTime()

    def setTime(self):
        # Refresh date
        now_date = QDate.currentDate()
        self.date.setText(now_date.toString("dd.MM.yyyy"))
        # Refresh time
        now_time = QTime.currentTime()
        self.time.setText(now_time.toString("hh:mm:ss"))

# ---------------------------------------------------------------------------------------------------------------------
# SWUCombobox


class SWUCombobox(QWidget):
    def __init__(self, parent=None, ax: int = 0, ay: int = 0,):
        super().__init__(parent)

        self.Frame = QFrame(self)
        self.my_toolbtn = QToolButton(self)
        self.my_menu = QMenu(self)
        self.group = QActionGroup(self.my_menu)
        self.port_list = getPorts()
        widget_width = 200
        widget_height = 50

        self.my_toolbtn.setGeometry(ax, ay, widget_width, widget_height)

        self.init_widget()

    def init_widget(self):

        self.my_toolbtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.my_toolbtn.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup)
        self.my_toolbtn.setFont(getFont(24, 'Regular'))
        self.my_toolbtn.setText(DataContainer.currentPort)
        self.my_toolbtn.setStyleSheet(QToolButtonStyle)
        self.current_port = DataContainer.currentPort
        self.my_toolbtn.setText(self.current_port)
        # Setting Menu Action

        for index in list(range(0, len(self.port_list))):
            self.action = QAction(self.port_list[index],
                                  checkable=True,
                                  checked=self.current_port == self.port_list[index])
            self.my_menu.addAction(self.action)
            self.group.addAction(self.action)

        self.my_menu.setFont(getFont(24, 'Regular'))
        self.my_menu.setStyleSheet(QMenuStyle)
        self.my_toolbtn.setMenu(self.my_menu)
        self.group.setExclusive(True)
        self.group.triggered.connect(self.on_triggered)

    def on_triggered(self, action):
        port = action.text()
        self.my_toolbtn.setText(port)
        DataContainer.setPort(port)

# ---------------------------------------------------------------------------------------------------------------------
# Section title class


class Label(QWidget):
    def __init__(self, string, parent=None, w: int = 300, h: int = 50, textAlignment=Qt.AlignCenter):
        super().__init__(parent)
        self.w = w
        self.h = h
        self.string = string
        self.Frame = QFrame(self)
        self.Text = QLabel(self.Frame)
        self.Text.setAlignment(textAlignment | Qt.AlignVCenter)
        self.init_widget()

    def init_widget(self):
        self.setFixedSize(self.w, self.h)
        self.Frame.setStyleSheet(
            SecondaryBackgroundColor+";"+"color:"+TextPrimaryColor+";")
        self.Frame.setFixedSize(self.w, self.h)
        self.Text.move(20, 0)
        self.Text.setFont(getFont(20, 'Medium'))
        self.Text.setFixedSize(self.w, self.h)
        self.Text.setText(self.string)

    def setText(self, text):
        self.Text.setText(text)
