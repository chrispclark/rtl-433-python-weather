from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtWidgets import (QWidget, QSlider, QApplication,
                             QHBoxLayout, QVBoxLayout)
import sys

class cPrg(QtWidgets):
    def __init__(self, initialValue=0, parent=None):
        super(cPrg, self).__init__(parent)
        self.textas = 'bandom'
        self.lineWidth = 0
        self.startAngle = 0
        self.endAngle = 0
        self.setValue(initialValue)
 
    def setValue(self, val):
        val = float(min(max(val, 0), 1))
        self._value = -270 * val
        self.update()
 
    def setLineWidth(self, lineWidth):
        self.lineWidth = lineWidth
 
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        rect = e.rect()
        outerRadius = min(self.width(), self.height())
         
        r = QtCore.QRectF(.5,.5,outerRadius-20,outerRadius-20)                            #<-- create rectangle
 
        startAngle = 270 * 16  # <-- set start angle to draw arc
        endAngle = -270 * 16  # <-- set end arc angle
 
        painter.setPen(QPen(QtGui.QColor('#000000'), 3))#self.lineWidth))  # <-- arc color
        # painter.setBrush(QtCore.Qt.HorPattern)
        painter.drawArc(r, startAngle, endAngle)  # <-- draw arc
 
        # arc prg
        painter.save()
        painter.setPen(QPen(QtGui.QColor('#ffffff'), 10))
        painter.drawArc(r, startAngle, self._value * 16)
        painter.restore()
 
        painter.end()
        super(cPrg, self).paintEvent(e)
        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = cPrg(QApplication)
        sys.exit(app.exec_())