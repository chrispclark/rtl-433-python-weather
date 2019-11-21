# Logic to draw compass taken from David Boddie example on https://wiki.python.org/moin/PyQt/Compass widget
# updated for pyqt5.


from PyQt5 import QtWidgets, QtCore, QtGui
# from mainwindow import Ui_MainWindow
from PyQt5.QtGui import QPainter, QPolygon, QFont, QFontMetricsF, QPen, QPalette, QColor
from PyQt5.QtCore import QPoint, Qt


class Compasswidget(QtWidgets.QLabel):

    def __init__(self, parent):
        super(Compasswidget, self).__init__(parent)

        self.setStyleSheet('QFrame {background-color:(239,100,100);}')
        self.resize(230, 230)
        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                           225: "SW", 270: "W", 315: "NW"}

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(168, 34, 3))
        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.drawMarkings(painter)
        self.drawNeedle(painter)
        painter.end()

    def drawMarkings(self, painter):

        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)

        painter.setFont(font)
        painter.setPen(self.palette().color(QPalette.Shadow))

        i = 0
        while i < 360:
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i]) / 2.0, -52,
                                 self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)

            painter.rotate(15)
            i += 15

        painter.restore()

    def drawNeedle(self, painter):

        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins) / 120.0,
                        (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(self.palette().brush(QPalette.Shadow))

        painter.drawPolygon(
            QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),
            QPoint(0, 45), QPoint(-10, 0)])
            )

        painter.setBrush(self.palette().brush(QPalette.Highlight))

        painter.drawPolygon(
            QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),
            QPoint(0, -30), QPoint(-5, -25)])
            )

        painter.restore()

    #def sizeHint(self):
    #    return QSize(150, 150)

    #def angle(self):
    #    return self._angle

    def setAngle(self, angle):
        # print(self._angle)
        if angle != self._angle:
            self._angle = angle
            self.update()