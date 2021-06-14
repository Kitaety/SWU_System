#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QLocale


# ---------------------------------------------------------------------------------------------------------------------
BackgroundColor = "background-color: rgb(30,30,30)"
SecondaryBackgroundColor = "background-color: rgb(48,48,48)"
PrimaryColor = 'rgb(0,174,219)'
TextPrimaryColor = 'rgb(194,194,194)'


russian_loc = QLocale(QLocale.Russian, QLocale.CyrillicScript, QLocale.Ukraine)
path = os.path.dirname(os.path.abspath(__file__))
# ---------------------------------------------------------------------------------------------------------------------
# Display size
display_width = 800
display_height = 480
# TopButtonMenu widget size
tb_width = display_width/4
tb_height = 64
# MainStack widget size
ms_width = 800
ms_height = 386
# ---------------------------------------------------------------------------------------------------------------------
# Font settings


def getFont(size, weight):
    font = QFont()
    font.setFamily('Roboto')
    font.setPointSizeF(size*0.75)
    if weight == 'Bold':
        font.setWeight(QFont.Bold)
    elif weight == 'Medium':
        font.setWeight(QFont.Medium)
    elif weight == 'Regular':
        font.setWeight(QFont.Normal)
    else:
        font.setWeight(QFont.Normal)

    return font
# ---------------------------------------------------------------------------------------------------------------------


ButtonStyle = """
    QPushButton{
        """+SecondaryBackgroundColor+""";
        color:"""+TextPrimaryColor+""";
        border: 10px;
    }
    QPushButton:pressed{
        border: 0px;
        background-color:"""+PrimaryColor+""";
        color: white;
    }
"""
ButtonMenuStyle = """
    QPushButton{
        color:"""+PrimaryColor+""";
        border-bottom: 2px solid """+PrimaryColor+""";
        border-top: none;
        border-left: none;
        border-right: none;
        border-style: outset;
    }
    QPushButton:checked {
        border: 0px;
        background-color:"""+PrimaryColor+""";
        color: white;
    }
"""

ComboBoxStyle = """
    QComboBox{
        """+SecondaryBackgroundColor+""";
        color:"""+TextPrimaryColor+""";
        border: 10px;
    }
"""
QToolButtonStyle = """
            QToolButton {
            """+SecondaryBackgroundColor+""";
            color:"""+TextPrimaryColor+""";
            border-radius: 0px;
            }
            QToolButton:hover {
            background: #393939;
            color: #91979F;
            }
            QToolButton:menu-indicator {image: none;}
            """
QMenuStyle = """
            QMenu {
            background-color: #4F4F4F;
            border: none;
            width: 200px;
            }
            QMenu::item {
            color: #FFFFFF;
            height: 40px;
            width: 200px;
            margin: 0px;
            padding-left: 30px;
            }
            QMenu::item:selected {
            background: #2699FB;
            }
        """
