#!/home/chrissy/.local/share/virtualenvs/weather-zRfsec3r/bin/python

import sys
import platform
import os
from PyQt5.QtCore import QThread, pyqtSignal, QTimer,  QLineF
from PyQt5.QtWidgets import (QApplication,  QGraphicsScene, QGraphicsView, QMainWindow, QPushButton, QGraphicsEllipseItem, QGraphicsLineItem)
import time
from PyQt5 import QtWidgets, QtCore, QtGui
import messageReceiveQueue
import pyqtgraph as pg
import databaseActions
import numpy as np
from loguru import logger

pg.setConfigOption('background', 'w')

command = 'rtl_433 -q'

Compass = {
    'E': 'East',
    'W': 'West',
    'N': 'North',
    'S': 'South',
    'NW': 'North West',
    'NE': 'North East',
    'SE': 'South East',
    'SW': 'South West',
    'WSW': 'West South West',
    'ESE': 'East South East',
}

logger.info("Running Version: " + platform.python_version())
logger.info("Path= " + os.getcwd())

from mainwindow import Ui_MainWindow


class ThreadIt(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)

    # The run method below gets called when we start the thread

    @QtCore.pyqtSlot()
    def run(self):
        z = messageReceiveQueue.RunIt()
        results = z.StartUp
        logger.info("The results: " + str(results))
        while True:
            for result in range(0, 10):
                #time.sleep(1)
                self.signal.emit(result)

class StartApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, rtl = None):
        super(StartApp, self).__init__(parent)
        self.setupUi(self)
        self.rtl = rtl

        self.MessageCountTimer = QTimer()
        self.MessageCountTimer.timeout.connect(self.getMessageCount)
        self.MessageCountTimer.start(1000)
        self.MessageDataTimer = QTimer()
        self.MessageDataTimer.timeout.connect(self.getMessageData)
        self.MessageDataTimer.start(1000*5)
        self.pushButton_Quit.clicked.connect(QtWidgets.qApp.quit)
        self.DrawIt(create=True)

        #self.TheCompass(self,45,100)
        #self.DrawIt()
        '''
        from math import cos, sin, pi
        # center of circle, angle in degree and radius of circle
        center = [0, 0]
        angle = 180+90+45
        radius = 18
        x = center[0] + (radius * cos(angle * pi / 180))
        y = center[1] + (radius * sin(angle * pi /180))
        self.graphicsView_Direction.plot([0,x],[0,y], pen=pg.mkPen('b', width=5)) # This is the line
        self.graphicsView_Direction.setTitle("Weather Direction")
        self.graphicsView_Direction.setLabel('bottom', 'X axis')
        self.graphicsView_Direction.setLabel('left', 'Y axis')
        self.graphicsView_Direction.setAspectLocked()

        # Add polar grid lines
        for r in range(2, 20, 2):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen(1.2))
            self.graphicsView_Direction.addItem(circle)
        '''


    def getMessageData(self):
        z = messageReceiveQueue.RunIt()
        x = z.MessageCount()
        results = z.StartUp
        print(results)

        if x >0:
            if 'Fine Offset Electronics WH1080/WH3080 Weather Station' in results.values():
                #logger.warning(results)
                # self.textEdit_Log.append("{0}".format(results)) # Log Results to textbox
                #logger.info("The results: " + str(results))
                #logger.info(results["time"])
                self.labelTime.setText(results["time"])
                self.lcdNumberTemperature.display(results["temperature_C"])
                self.lcdNumber_WindSpeed.display(results["speed"])
                self.lcdNumberGust.display(results["gust"])
                self.lcdNumberDirectionDeg.display(results["direction_deg"])
                self.lcdNumberRain.display(results["rain"])
                self.labelDirectionStr.setText(results["direction_str"])
                self.lcdNumberDirectionDeg.display(results["direction_deg"])
                #logger.info(results["model"])
                #logger.info(results["id"])
                #logger.info(results["temperature_C"])
                self.updateDirection(results)
            else:
                if 'Fine Offset Electronics, WH2 Temperature/Humidity sensor' not in results.values():
                    self.textEdit_Log.append("{0}".format(results))

        # Create the temperature graph
        temperatureC = databaseActions.returnTemp()
        x: range = range(0, len(temperatureC))
        pg.setConfigOption('background', 'w')
        #logger.info(type(temperatureC))
        #logger.info(x)
        #logger.info(temperatureC)
        self.graphicsViewTemperature.plot(x, temperatureC)
        self.DrawIt(create=False)

    def updateDirection(self, results):
        # Create the wind direction graph
        #logger.info(type(results["direction_deg"]))
        #scene = QtWidgets.QGraphicsScene()
        #self.graphicsView_Direction.setScene(scene)
        #logger.info(int(results["direction_deg"]))
        #logger.info(type(int(results["direction_deg"])))
        from math import cos, sin, pi

        # center of circle, angle in degree and radius of circle
        center = [0, 0]
        angle = int(results["direction_deg"])
        angle = angle * (pi / 180)
        logger.info("Angle: " + str(angle))
        radius = 18
        #x = center[0] + (radius * cos(angle * pi / 180))
        #y = center[1] + (radius * sin(angle * pi / 180))
        i = 18
        x = 0 + radius * cos(2 * pi * i / 8)
        y = 0 + radius * sin(2 * pi * i / 8)
        print(x)
        print(y)
        self.graphicsView_Direction.clear()
        self.graphicsView_Direction.plot([0, x], [0, y], pen=pg.mkPen('b', width=5, style=QtCore.Qt.DashLine))  # This is the line
        self.graphicsView_Direction.setTitle("Weather Direction")
        self.graphicsView_Direction.setLabel('bottom', 'X axis')
        self.graphicsView_Direction.setLabel('left', 'Y axis')
        self.graphicsView_Direction.setAspectLocked()
        #logger.info("done")
        # Add polar grid lines
        for r in range(2, 20, 2):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen('r', width=1 ))
            self.graphicsView_Direction.addItem(circle)
        pass


    def DrawIt(self, create):
        scene = QtWidgets.QGraphicsScene()
        self.DirectionGraphicsView.setScene(scene)
        if create:
            pen = QtGui.QPen(QtCore.Qt.green)
            scene.addEllipse(0, 0, 180, 180, pen)
        else:
            scene = QtWidgets.QGraphicsScene()
            pen = QtGui.QPen(QtCore.Qt.red, 5)
            vLine = QLineF(0,0,90,90)
            scene.addLine(vLine, pen)

    def TheCompass(self, painter, yaw, r):
        i = r.center().x()
        # print(yaw)
        yaw_pix = int(yaw * 6)
        pos_pix = yaw_pix + r.center().x()
        deg_pix = 0

        if (yaw < 0):
            yaw += 360

        painter.drawLine(r.center().x(), 10, r.center().x(), 35)
        painter.drawText(r.center().x() - 10, 50, str(int(yaw)))

        if (pos_pix <= r.right()):
            shift = r.center().x() - pos_pix
        else:
            pos_pix = r.center().x() - (pos_pix - r.center().x())
            shift = r.center().x() - pos_pix
        if (shift >= 0):
            while (i <= r.right() + shift):
                j = r.center().x() - (i - r.center().x())
                if (i <= r.right() + shift) and ((i - r.center().x()) % 90 == 0):
                    angle = deg_pix / 6
                    painter.drawLine(i + shift, 15, i + shift, 30)
                    painter.drawText(i + shift, 15, str(int(angle)))
                    if (i != j):
                        painter.drawLine(j + shift, 15, j + shift, 30)
                        painter.drawText(j + shift, 15, str(int(360 - angle)))

                painter.drawLine(i + shift, 20, i + shift, 30)
                painter.drawLine(j + shift, 20, j + shift, 30)
                i += 30
                deg_pix += 30
        else:
            while (i <= r.right() - shift):
                j = r.center().x() - (i - r.center().x())
                if (i <= r.right() - shift) and ((i - r.center().x()) % 90 == 0):
                    angle = deg_pix / 6
                    painter.drawLine(i + shift, 15, i + shift, 30)
                    painter.drawText(i + shift, 15, str(int(angle)))
                    if (i != j):
                        painter.drawLine(j + shift, 15, j + shift, 30)
                        painter.drawText(j + shift, 15, str(int(360 - angle)))

                painter.drawLine(i + shift, 20, i + shift, 30)
                painter.drawLine(j + shift, 20, j + shift, 30)
                i += 30
                deg_pix += 30


    def getMessageCount(self):
        z = messageReceiveQueue.RunIt()
        s = z.MessageCount()
        self.lcdNumberCounter.display(s)

        # logger.info("Message Count: " + str(s))
        # self.update_timer.start(30)
        pass


    def finished(self, result):
        self.lcdNumberCounter.display(result)
        self.textEdit_Log.append("{0}".format(result))
        self.pushButton_Start.setEnabled(True)  # Enable the pushButton

    
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = StartApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
