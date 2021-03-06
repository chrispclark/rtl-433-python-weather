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


class RainfallWidget(QtWidgets.QLabel):
    def __init__(self, parent):
        super(RainfallWidget, self).__init__(parent)

        self.initUI()

    def initUI(self):

        # self.setMinimumSize(600,41)
        self.resize(900, 30)

        rainfall_default = 300
        base = 800 / 22
        # logger.info("Base :" + str(base))
        self._rainfall = rainfall_default
        logger.info("Rainfall: " + str(self._rainfall))
        self.num = [
            "50",
            "100",
            "150",
            "200",
            "250",
            "300",
            "350",
            "400",
            "450",
            "500",
            "550",
            "600",
            "650",
            "700",
            "750",
            "800",
            "850",
            "900",
            "950",
            "1000",
            "1100",
            "1200",
            "1300",
        ]
        #logger.info("speed: " + (str(len(self.num))))

    """
    def setValue(self, value):

        self.value = value
    """

    def paintEvent(self, e):

        # logger.info("In paint event")
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
        # logger.info(w)
        # logger.info(h)

        step = int(round(w / 18)) # sets the step for writing the rainfall text
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
        till = self._rainfall
        qp.setPen(QColor(255, 255, 255))  # white
        # qp.setBrush(QColor(255, 255, 100))  #  yellow
        qp.setBrush(QColor(103, 103, 248))  # blue
        logger.info("Rainfall till " + str(till))
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
        if value != self._rainfall:
            self._rainfall = value
            self.update()
            # self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RainfallWidget(QApplication)
    sys.exit(app.exec_())
