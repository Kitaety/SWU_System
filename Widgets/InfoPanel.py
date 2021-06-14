from Widgets.SWUStyle import SecondaryBackgroundColor, TextPrimaryColor, PrimaryColor, getFont
from PyQt5.QtWidgets import QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt, QTimer
from Utils.DataContainer import instance as DataContainer


class InfoPanel(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setStyleSheet(SecondaryBackgroundColor)
        # self.setStyleSheet('background-color:{}'.format(PrimaryColor))
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 800, 30)

        self.titleNetworkState = QLabel('Network: ', self.frame)
        self.titleNetworkState.setStyleSheet(
            'QLabel {color: '+TextPrimaryColor+';}')
        self.titleNetworkState.setFont(getFont(15, 'Medium'))
        self.titleNetworkState.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.titleNetworkState.setGeometry(10, 0, 70, 30)

        self.networkStateLabel = QLabel(self.frame)
        self.networkStateLabel.setStyleSheet(
            'QLabel {color: '+TextPrimaryColor+';}')
        self.networkStateLabel.setFont(getFont(15, 'Medium'))
        self.networkStateLabel.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.networkStateLabel.setGeometry(80, 0, 50, 30)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateNetworkState)
        self.timer.start(1000)
        self.updateNetworkState()

    def updateNetworkState(self):
        self.networkStateLabel.setText(DataContainer.networkState)
