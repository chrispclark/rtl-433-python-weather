from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtCore
from ThreadSignalUI import Ui_MainWindow
from PyQt5 import QtWidgets

import sys
import time

from mainwindow import Ui_MainWindow

class WorkThread(QtCore.QObject):
    UpdateTextBoxSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        runningval = 0

        while runningval < 10:
            runningval += 1
            self.UpdateTextBoxSignal.emit(runningval)
            time.sleep(0.5)


class StartApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(StartApp, self).__init__(parent)
        self.setupUi(self)

        self.worker = WorkThread()
        self.workerThread = QtCore.QThread() 
        self.workerThread.started.connect(self.worker.run)
        self.worker.moveToThread(self.workerThread)
        self.worker.UpdateTextBoxSignal.connect(self.UpdateTextBoxFunction)

        self.StartButt.clicked.connect(self.StartThreading)

    def StartThreading(self, event):
        self.workerThread.start()

    def UpdateTextBoxFunction(self, value):
        self.TextBox.setText(str(value))


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = StartApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
