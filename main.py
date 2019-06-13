#!/home/chrissy/.local/share/virtualenvs/weather-zRfsec3r/bin/python

import sys
import platform
import os
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5 import QtWidgets, QtCore
import messageReceiveQueue
import pyqtgraph as pg
import databaseActions
from loguru import logger
from compasswidget import Compasswidget
from mainwindow import Ui_MainWindow
from temperature_bar import *
from speed_bar import *
from gust_bar import *
from rainfull_bar import *

pg.setConfigOption("background", "#efefef")
pg.setConfigOption('foreground', 'k')

# command = "rtl_433 -q"
'''
Compass = {
    "E": "East",
    "W": "West",
    "N": "North",
    "S": "South",
    "NW": "North West",
    "NE": "North East",
    "SE": "South East",
    "SW": "South West",
    "WSW": "West South West",
    "ESE": "East South East",
}


Device = {
    '0' : 'WH1080/WH3080',
}
'''

logger.info("Running Version: " + platform.python_version())
logger.info("Path= " + os.getcwd())

'''
class ThreadIt(QThread):
    signal = pyqtSignal("PyQt_PyObject")

    def __init__(self):
        QThread.__init__(self)

    # The run method below gets called when we start the thread

    @QtCore.pyqtSlot(int)
    def run(self):
        z = messageReceiveQueue.RunIt()
        results = z.StartUp
        logger.info("The results: " + str(results))
        while True:
            for result in range(0, 10):
                # time.sleep(1)
                self.signal.emit(result)
'''

class StartApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, rtl=None):
        self.progressBarQueueValue = 0
        self.NumberTotalMessageCount = 0
        super(StartApp, self).__init__(parent)
        self.setupUi(self)
        self.rtl = rtl

        # self.setStyleSheet(open("style.qss", "r").read())

        # initialise the compass
        self.CompassPlot = Compasswidget(self.labelCompass)

        self.progressBarTemperature = TemperatureWidget(self.labelTemperatureBar)
        self.progressBarSpeed = SpeedWidget(self.labelSpeedBar)
        self.progressBarGust = GustWidget(self.labelGustBar)
        self.progressBarRainfall = RainfallWidget(self.labelRainfallBar)

        # Check MQ message count every 2 second
        self.MessageCountTimer = QTimer()
        self.MessageCountTimer.timeout.connect(self.getMessageCount)
        self.MessageCountTimer.start(1000 * 2)

        # Get message data every 2 seconds

        self.MessageDataTimer = QTimer()
        self.MessageDataTimer.timeout.connect(self.getMessageData)
        self.MessageDataTimer.start(1000 * 2)


        # self.progressBarTemperature.changeValue(250)

        # Allow us to quit the application
        self.pushButton_Quit.clicked.connect(QtWidgets.qApp.quit)

    def getMessageData(self):
        self.progressBarQueueValue += 1
        self.NumberTotalMessageCount += 1
        if (self.progressBarQueueValue == 11):
            self.progressBarQueueValue = 0

        # logger.info (self.progressBarQueueValue)

        # initialise message receive queue
        messageQueue = messageReceiveQueue.RunIt()
        messageQueueCount = messageQueue.MessageCount()
        results : dict = messageQueue.StartUp

        self.progressBarQueue.setValue(self.progressBarQueueValue)
        self.lcdNumberTotalMessageCount.display(self.NumberTotalMessageCount)

        if messageQueueCount > 0:
            self.labelError.setText("")
            value = results['DetectedModelType']
            if ( value ==  "WH1080/WH3080" ):
                # logger.warning(results)
                # self.textEdit_Log.append("{0}".format(results)) # Log Results to textbox
                # logger.info("The results: " + str(results))
                # logger.info(results["time"])
                self.labelTime.setText(results["time"])
                self.lcdNumberTemperature.display(results["temperature_C"])
                self.lcdNumber_WindSpeed.display(results["speed"])
                self.lcdNumberGust.display(results["gust"])
                self.lcdNumberDirectionDeg.display(results["direction_deg"])
                self.lcdNumberRain.display(results["rain"])
                self.labelDirectionStr.setText(results["direction_str"])
                self.lcdNumberDirectionDeg.display(results["direction_deg"])
                # logger.info(results["model"])
                # logger.info(results["id"])
                # logger.info(results["temperature_C"])
                angle = int(results["direction_deg"])
                # logger.info("Angle: " + str(angle))
                self.CompassPlot.setAngle(angle)
                temp = int(results["temperature_C"])
                speed = int(results["speed"])
                gust = int(results["gust"])
                rain = int(results["rain"])
                # self.progressBarTemperature.setValue(temp)

                value = temp * 10
                self.progressBarTemperature.changeValue(value)
                value = speed * 10
                self.progressBarSpeed.changeValue(value)
                value = gust * 10
                self.progressBarGust.changeValue(value)
                value = rain
                self.progressBarRainfall.changeValue(value)

            else:
                if (
                    "Fine Offset Electronics, WH2 Temperature/Humidity sensor"
                    not in results.values()
                ):
                    self.textEdit_Log.append("{0}".format(results))
        else:
            self.labelError.setText(str(results))

        # Create the temperature graph
        temperatureC = databaseActions.returnTemp()
        x: range = range(0, len(temperatureC))
        self.graphicsViewTemperature.plot(x, temperatureC, pen='k')

        # Create the rain graph
        rain = databaseActions.returnRain()
        x: range = range(0, len(rain))
        self.graphicsViewRainfall.plot(x, rain, pen='k')

    def getMessageCount(self) -> object:
        messageQueue = messageReceiveQueue.RunIt()
        messageCount: object = messageQueue.MessageCount()
        self.lcdNumberCounter.display(messageCount)

        # logger.info("Message Count: " + str(s))
        # self.update_timer.start(30)

    """
    def finished(self, result):
        self.lcdNumberCounter.display(result)
        self.textEdit_Log.append("{0}".format(result))
        self.pushButton_Start.setEnabled(True)  # Enable the pushButton
    """


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = StartApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
