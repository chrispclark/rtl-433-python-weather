## #!/home/chrissy/.local/share/virtualenvs/weather-zRfsec3r/bin/python

import datetime

from process import *
# from dateutil.relativedelta import relativedelta
import os
import platform

# import sys
import matplotlib.dates as mdates  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
# import qdarkstyle  # type: ignore
# import snoop  # type: ignore
from loguru import logger  # type: ignore
# from matplotlib.dates import DateFormatter  # type: ignore
from matplotlib.ticker import MaxNLocator  # type: ignore
from PyQt5 import QtWidgets  # type: ignore
from PyQt5.Qt import PYQT_VERSION_STR  # type: ignore
from PyQt5.QtCore import QT_VERSION_STR, QTimer  # type: ignore
import sys

# import heartrate; heartrate.trace(browser=True)

import databaseActions
import messageReceiveQueue
from compasswidget import Compasswidget
from gust_bar import GustWidget
from mainwindow import Ui_MainWindow
from rainfull_bar import RainfallWidget
from speed_bar import SpeedWidget
from temperature_bar import TemperatureWidget

logger.info("Running Version: " + platform.python_version())
logger.info("Path= " + os.getcwd())
logger.info("Qt version:", QT_VERSION_STR)
logger.info("PyQt version:", PYQT_VERSION_STR)

class StartApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, rtl=None):
        self.progressBarQueueValue = 0
        self.NumberTotalMessageCount = 0
        self.firstloop = True
        super(StartApp, self).__init__(parent)
        self.setupUi(self)
        """
        doc string
        """
        
        # Allow us to quit the application
        self.pushButton_Quit.clicked.connect(QtWidgets.qApp.quit)
        
        self.initialise_rtl()
        self.settimers()
    
    def initialise_rtl(self):
        # self.setStyleSheet(open("style.qss", "r").read())

        # initialise the compass
        self.CompassPlot = Compasswidget(self.labelCompass)

        # initialise message receive queue
        self.messageQueue = messageReceiveQueue.RunIt()

        # initialise the matplot cavas
        self.axRain, self.axTemp = self.plot_canvas_setup()
        self.plot_canvas()
        
        # initialise the bars
        self.progressBarTemperature = TemperatureWidget(self.labelTemperatureBar)
        messageCount: object = self.messageQueue.MessageCount()
        self.lcdNumberCounter.display(messageCount)
        self.progressBarSpeed = SpeedWidget(self.labelSpeedBar)
        self.progressBarGust = GustWidget(self.labelGustBar)
        self.progressBarRainfall = RainfallWidget(self.labelRainfallBar)
        
    def settimers(self):
        # Check MQ message count every 5 second
        # self.MessageCountTimer = QTimer()
        # self.MessageCountTimer.timeout.connect(self.getMessageCount)
        # self.MessageCountTimer.start(1000 * 5)

        # Get message data every 1 second
        self.MessageDataTimer = QTimer()
        self.MessageDataTimer.timeout.connect(self.getMessageData)
        self.MessageDataTimer.start(1000 * 1.0)
        # self.progressBarTemperature.changeValue(250)

        
        # Set up radio buttons
        self.radioButtonGraphDateAll.toggled.connect(self.onRadioBtn)
        self.radioButtonGraphDateMonth.toggled.connect(self.onRadioBtn)
        self.radioButtonGraphDateWeek.toggled.connect(self.onRadioBtn)

    def onRadioBtn(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            logger.info("You Have Selected " + radioBtn.text())

    def getMessageData(self):
        self.progressBarQueueValue += 1
        self.NumberTotalMessageCount += 1
        if self.progressBarQueueValue == 11:
            self.progressBarQueueValue = 0

        messageQueueCount = self.messageQueue.MessageCount()
        results: dict = self.messageQueue.StartUp
        self.progressBarQueue.setValue(self.progressBarQueueValue)
        self.lcdNumberTotalMessageCount.display(self.NumberTotalMessageCount)

        messageCount: object = self.messageQueue.MessageCount()
        self.lcdNumberCounter.display(messageCount)

        if messageQueueCount > 0:
            self.labelError.setText("")
            if (
                "Fine Offset Electronics WH1080/WH3080 Weather Station"
                in results.values()
            ):
                self.plot_canvas()
                # self.textEdit_Log.append("{0}".format(results)) # Log Results to textbox
                # logger.info("The results: " + str(results))
                # logger.info(results["time"])
                self.labelTime.setText(results["time"])
                self.lcdNumberTemperature.display(results["temperature_C"])
                self.lcdNumber_WindSpeed.display(results["speed"])
                self.lcdNumberGust.display(results["gust"])
                self.lcdNumberDirectionDeg.display(results["direction_deg"])
                self.lcdNumberRain.display(results["rain"])
                # self.labelDirectionStr.setText(results["direction_str"])
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

    def plot_canvas(self):
        datemax = datetime.datetime.now()
        graphButton = self.buttonGroup.checkedId()
        # print(graphButton)
        # Create the rain graph
        rain, rainTime = databaseActions.returnRain()
        rainTimeMonth = []
        self.axRain.cla()
        for dates in rainTime:
            z = mdates.datestr2num(dates)
            rainTimeMonth.append(z)
        # print(min(rainTimeMonth))
        # print(max(rainTimeMonth))
        my_fmt = mdates.DateFormatter("%d/%m")
        self.axTemp.xaxis.set_major_locator(MaxNLocator(nbins=30))
        self.axRain.xaxis.set_major_formatter(my_fmt)
        self.axTemp.tick_params(axis="x", labelsize=6)
        self.axTemp.tick_params(axis="y", labelsize=6)
        if graphButton == -3:
            month = datetime.timedelta(weeks=5)
            datemin = datemax - month
            self.axRain.set_xlim(datemin, datemax)
            # logger.info(str(datemin) + ' 3 rain ' + (datemax))
        elif graphButton == -4:
            week = datetime.timedelta(weeks=1)
            datemin = datemax - week
            self.axRain.set_xlim(datemin, datemax)
            # logger.info(str(datemin) + ' 4 rain ' + str(datemax))
        self.axRain.plot(rainTimeMonth, rain, color="black", linewidth=0.5)
        # rainTimeMonth = []

        # Create the temperature graph
        temp, tempTime = databaseActions.returnTemp()
        tempTimeMonth = []
        self.axTemp.cla()
        for dates in tempTime:
            z = mdates.datestr2num(dates)
            tempTimeMonth.append(z)
        my_fmt = mdates.DateFormatter("%d/%m")
        self.axTemp.xaxis.set_major_locator(MaxNLocator(nbins=30))
        self.axTemp.xaxis.set_major_formatter(my_fmt)
        self.axTemp.tick_params(axis="x", labelsize=6)
        self.axTemp.tick_params(axis="y", labelsize=6)
        if graphButton == -3:
            month = datetime.timedelta(weeks=5)
            datemin = datemax - month
            self.axTemp.set_xlim(datemin, datemax)
            # logger.info(str(datemin) + ' 3 temp ' + str(datemax))
        elif graphButton == -4:
            week = datetime.timedelta(weeks=1)
            datemin = datemax - week
            self.axTemp.set_xlim(datemin, datemax)
            # logger.info(str(datemin) + ' 4 temp ' + str(datemax))
        self.axTemp.set_xlabel("Date", fontsize=6)
        self.axTemp.set_ylabel("Temperature", fontsize=6)
        self.axTemp.plot(tempTimeMonth, temp, color="black", linewidth=0.5)
        tempTimeMonth = []
        # self.axRain.clear()

    def plot_canvas_setup(self) -> object:
        plt.tick_params(axis="both", which="minor", labelsize=6)
        plt.tick_params(axis="both", which="major", labelsize=6)
        plt.tight_layout()
        plt.ion()
        # plt.show(block=False)
        print(plt.style.available)
        plt.axis("off")  # Turn off auto labels on axis
        plt.style.use("ggplot")
        self.axTemp = self.canvasMatplot.figure.add_subplot(211)
        self.axTemp.set_xlabel("Date", fontsize=6)
        self.axTemp.set_ylabel("Temperature", fontsize=6)
        self.axTemp.xaxis.set_major_locator(MaxNLocator(nbins=30))
        self.axTemp.tick_params(axis="x", labelsize=6)
        self.axTemp.tick_params(axis="y", labelsize=6)

        self.axRain = self.canvasMatplot.figure.add_subplot(212)
        self.axRain.set_xlabel("Date", fontsize=6)
        self.axRain.set_ylabel("Rain Inches", fontsize=6)
        self.axRain.xaxis.set_major_locator(MaxNLocator(nbins=30))
        self.axRain.tick_params(axis="x", labelsize=6)
        self.axRain.tick_params(axis="y", labelsize=6)
        return self.axRain, self.axTemp


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = StartApp()
    form.show()
    # app.setStyleSheet(dark_stylesheet)
    app.exec_()


if __name__ == "__main__":
    main()
