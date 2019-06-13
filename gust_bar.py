#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a custom widget.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
import sys

from PyQt5 import QtWidgets
from loguru import logger


class GustWidget(QtWidgets.QLabel):
    def __init__(self, parent):
        super(GustWidget, self).__init__(parent)

        self.initUI()

    def initUI(self):

        # self.setMinimumSize(600,41)
        self.resize(800, 30)

        temperature_default = 300
        base = 800 / 22
        # logger.info("Base: " + str(base))
        self._temperature = temperature_default
        # print(self._temperature)
        self.num = [
            "5",
            "10",
            "15",
            "20",
            "25",
            "30",
            "35",
            "40",
            "45",
            "50",
            "55",
            "60",
            "65",
            "70",
            "75",
            "80",
            "85",
            "90",
            "95",
            "100",
            "110",
            "120",
            "130",
        ]
        #logger.info("speed: " + (str(len(self.num))))

    """
    def setValue(self, value):

        self.value = value
    """

    def paintEvent(self, e):

        #logger.info("In paint event")
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):

        MAX_CAPACITY = 700
        OVER_CAPACITY = 750

        font = QFont("Serif", 7, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()
        #logger.info(w)
        #logger.info(h)

        step = int(round(w / 16))
        """
        till = int(((w / OVER_CAPACITY) * self._value))
        full = int(((w / OVER_CAPACITY) * MAX_CAPACITY))

        if self._value >= MAX_CAPACITY:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))  # light yellow
            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))    # pink
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till - full, h)

        else:
        """
        till = self._temperature
        qp.setPen(QColor(255, 255, 255))  # white
        # qp.setBrush(QColor(255, 255, 100))  #  yellow
        qp.setBrush(QColor(103, 103, 248))  # blue
        qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)  # black

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)

        j = 0

        for i in range(step, len(self.num) * step, step):
            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i - fw / 2, h / 2, str(self.num[j]))
            j = j + 1

        # self.changeValue(55 * 10)

    def changeValue(self, value):
        #logger.info("changeValue")
        if value != self._temperature:
            self._temperature = value
            self.update()
            # self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SpeedWidget(QApplication)
    sys.exit(app.exec_())
