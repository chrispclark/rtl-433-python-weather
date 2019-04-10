from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QWidget, QApplication
import sys
import time

class A(QObject):
    def run(self):
        while 1:
            print('A', time.ctime())
            time.sleep(1)
class B(QObject):
    def run(self):
        while 1:
            print('B', time.ctime())
            time.sleep(1)
class C(QObject):
    def run(self):
        while 1:
            print('C', time.ctime())
            time.sleep(1)
class D(QObject):
    def run(self):
        while 1:
            print('D', time.ctime())
            time.sleep(1)

class window1(QWidget):
    def __init__ (self, parent = None):
        super().__init__ () #parent widget

        self.thread1 = QThread()
        obj1 = A()
        obj1.moveToThread(self.thread1)
        self.thread1.started.connect(obj1.run)
        self.thread1.start()

        self.thread2 = QThread()
        obj2 = B()
        obj2.moveToThread(self.thread2)
        self.thread2.started.connect(obj2.run) #this sets up a signal in the other direction??
        self.thread2.start()

        self.thread3 = QThread()
        obj3 = C()
        obj3.moveToThread(self.thread3)
        self.thread3.started.connect(obj3.run) #this sets up a signal in the other direction??
        self.thread3.start()

        self.thread4 = QThread()
        obj4 = D()
        obj4.moveToThread(self.thread4)
        self.thread4.started.connect(obj4.run)
        self.thread4.start()

        time.sleep(1)

app = QApplication(sys.argv) #every pyqt application must create an application object
w = window1()
w.show()
sys.exit(app.exec_())