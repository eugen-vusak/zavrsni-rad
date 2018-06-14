import sys
from PyQt5 import QtCore, QtWidgets
from collections import deque
import numpy as np

from Serial import Serial
import Neural_Networks as nn
import Data.gestures as gestures

np.set_printoptions(suppress=True)

GESTURE_SIZE = 360


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 312)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 401, 251))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 399, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(440, 40, 171, 41))
        self.textBrowser.setObjectName("textBrowser")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


def fill_frame(data):
    global serial
    global frame
    global old_gesture
    global old_vector
    global old_data
    global ui

    data = data.split(",")

    if len(data) == 6:
        # print("filling frame")
        frame.extend(data)

    if(len(frame) == GESTURE_SIZE):

        print("frame is full")

        serial.serialEvent.disconnect(fill_frame)

        print("guessing")

        vector = net.feedforward(np.asfarray(frame).reshape(GESTURE_SIZE, 1))
        print(vector)
        new_gesture = gestures.from_vector(vector)

        if new_gesture != old_gesture:
            old_gesture = new_gesture
            print(new_gesture)
            ui.textBrowser.setText(new_gesture)
            print(max(vector))

        old_data = None

        t = QtCore.QTimer()
        t.singleShot(2000, timeout_handler)


def timeout_handler():
    print("go")
    serial.serialEvent.connect(test_movement)


def shift_frame(data):
    global frame
    global serial
    global tick
    global net
    global old_gesture
    global old_vector

    data = data.split(",")

    if len(data) == 6:
        frame.extend(data)

    elif data[0] == "Device is ready":
        frame.clear()
        serial.serialEvent.disconnect(shift_frame)
        serial.serialEvent.connect(fill_frame)
        return
    else:
        # print("shift_frame_error", data)
        exit()

    vector = net.feedforward(np.asfarray(frame).reshape(GESTURE_SIZE, 1))
    new_gesture = gestures.from_vector(vector)
    if new_gesture and max(vector) > old_vector and new_gesture != old_gesture:
        old_gesture = new_gesture
        print(old_gesture)
        print(max(vector))
        frame.clear()
        serial.serialEvent.disconnect(shift_frame)
        serial.serialEvent.connect(fill_frame)


def almost_equal(arg1, arg2, tolerance=100):
    return abs(arg1 - arg2) <= tolerance


def disconnect():
    try:
        serial.serialEvent.disconnect(shift_frame)
        serial.serialEvent.disconnect(fill_frame)
    except Exception:
        pass


def test_movement(data):
    global old_data
    global serial
    global frame
    global listening
    global old_gesture
    global old_vector
    global ui

    # ("detecting movement: ", end="")

    try:
        data = list(map(int, data.split(",")))
    except Exception:
        pass

    # print(listening)

    if len(data) == 6:
        if old_data:
            for a1, a2 in zip(data, old_data):
                if not almost_equal(a1, a2):
                    # print("movement")
                    old_data = data

                    frame.clear()
                    serial.serialEvent.disconnect(test_movement)
                    serial.serialEvent.connect(fill_frame)
                    return

        old_data = data
        # print("not movement")
        # ui.textBrowser.setText("")


if __name__ == '__main__':

    net = nn.loadFromFile("Neural_Networks/.neuralnetwork.pkl")

    old_gesture = None
    old_vector = 0
    old_data = None
    listening = False

    serial = Serial("/dev/ttyUSB0")

    # reset Arduino
    serial.setDTR(False)
    serial.flushInput()
    serial.setDTR(True)

    serial.start()
    # tick = perf_counter()
    # serial.serialEvent.connect(shift_frame)
    # serial.serialEvent.connect(print)
    serial.serialEvent.connect(test_movement)

    frame = deque(maxlen=360)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    app.exec_()
