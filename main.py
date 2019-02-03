#!/home/chrissy/.local/share/virtualenvs/weather-zRfsec3r/bin/python

import sys
import platform
import os
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import time
from PyQt5 import QtWidgets, QtCore
import messageReceiveQueue

from loguru import logger

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
        results = z.StartUp()
        logger.info("The results: " + str(results))
        while True:
            for result in range(0, 10):
                time.sleep(1)
                self.signal.emit(result)

class StartApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, rtl = None):
        super(StartApp, self).__init__(parent)
        self.setupUi(self)
        self.rtl = rtl

        self.MessageCountTimer = QTimer()
        # Connect it to f
        self.MessageCountTimer.timeout.connect(self.getMessageCount)
        self.MessageCountTimer.start(1000)

        self.MessageDataTimer = QTimer()
        # Connect it to f
        self.MessageDataTimer.timeout.connect(self.getMessageData)
        self.MessageDataTimer.start(1000*5)
        self.pushButton_Quit.clicked.connect(QtWidgets.qApp.quit)


    def getMessageData(self):
        z = messageReceiveQueue.RunIt()
        x = z.MessageCount()
        if x >0:
            results = z.StartUp()
            self.textEdit_Log.append("{0}".format(results))
            logger.info("The results: " + str(results))
            logger.info(results["time"])
            logger.info(results["model"])
            logger.info(results["id"])
            logger.info(results["temperature_C"])
        else:
            logger.warning("Queue is Empty")

    def getMessageCount(self):
        z = messageReceiveQueue.RunIt()
        s = z.MessageCount()
        self.lcdNumberCounter.display(s)
        
        # logger.info("Message Count: " + str(s))
        # self.update_timer.start(30)


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
