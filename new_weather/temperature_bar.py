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

class TemperatureWidget(QtWidgets.QLabel):
    def __init__(self, parent):
        super(TemperatureWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        # self.setMinimumSize(600,41)
        self.resize(800, 30)

        temperature_default = 300
        self._temperature = temperature_default
        # print(self._temperature)
        # self.num = ["-10","-5","0", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65",  "70",""]
        #self.num = ["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70"]
        self.num = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        logger.info("List Len = {0}".format(str(len(self.num))))

    '''
    def setValue(self, value):

        self.value = value
    '''

    def paintEvent(self, e):

        #logger.info("In paint event")
        
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):

        MAX_CAPACITY = 700
        OVER_CAPACITY = 750

        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()
        logger.info(w)
        #logger.info(h)Rijsttafel

        #step = (int(round(w ) / len(self.num))) # lays out the text labels for temperature markers
        step = (int(round(w ) / 16)) # lays out the text labels for temperature markers
        logger.info("Step Size =" + str(step))
        '''
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
        '''

        # Draw the rectangles on the widget to show temperature
        #
        # Size = 800
        # till = actual temperature
        # temperature = 15, each step is 800/15 = 53.3

        till = self._temperature
        logger.info("Temperature = " + str(till))
        qp.setPen(QColor(255, 255, 255))    # white
        #qp.setBrush(QColor(255, 255, 100))  #  yellow
        qp.setBrush(QColor(103, 103, 248))  # blue
        qp.drawRect(0, 0, till, h) # Draws the rectangle inside the widget
        logger.info("till = " +str(till) + " " + str(h))

        pen = QPen(QColor(20, 20, 20), 1,       # black
                   Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        logger.info("rect : " +str(w) + " " + str(h))
        qp.drawRect(0, 0, w - 1, h - 1)     # Draws the border around the widget

        j = 0

        # draw the text on the widget
        for i in range(step, len(self.num) * step, step):
            logger.info("Temperature Step = " + str(i))
            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i - fw / 2, h / 2, str(self.num[j]))
            logger.info("Temperature num = " + str(self.num[j]) + " "+ str( i - fw / 2) + " " + str(h / 2))
            j = j + 1
        
        #self.changeValue(55 * 10)

    def changeValue(self, value):
        #logger.info("changeValue")
        if value != self._temperature:
            self._temperature = value
            self.update()
            # self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TemperatureWidget(QApplication)
    sys.exit(app.exec_())
