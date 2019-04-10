from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(269, 232)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.TextBox.setGeometry(QtCore.QRect(74, 40, 113, 20))
        self.TextBox.setObjectName("TextBox")
        self.StartButt = QtWidgets.QPushButton(self.centralwidget)
        self.StartButt.setGeometry(QtCore.QRect(94, 72, 75, 23))
        self.StartButt.setObjectName("StartButt")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButt.setText(_translate("MainWindow", "Start"))