import serial
from PyQt5.QtCore import pyqtSignal, QThread
from time import perf_counter


class Serial(QThread):
    serialEvent = pyqtSignal(str)

    def __init__(self, port):
        super(Serial, self).__init__()
        self.running = True

        self.ser = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2)

    def stop(self):
        self.running = False

    def run(self):
        print("starting serial watcher")
        # tick = 0

        with self.ser:
            while self.running:
                buffered = self.ser.inWaiting()
                if buffered > 0:
                    # print(buffered)
                    s = self.ser.readline().decode().strip()
                    # tock = perf_counter()
                    # print(tock - tick)
                    # tick = tock
                    self.process(s)
            print("serial watcher finished")

    def process(self, s):
        self.serialEvent.emit(s)

    def readUntil(self, char):
        string = ""
        while True:
            byte = self.ser.read().decode()
            if byte == char:
                return string
            string += byte

    def write(self, string):
        try:
            self.ser.write(string.encode())
        except Exception as s:
            print("Writing Error", s)

    def clear(self):
        buffered = self.ser.inWaiting()
        if buffered > 0:
            print("clearing", self.ser.read(buffered).decode())

    def flushInput(self):
        self.ser.flushInput()

    def setDTR(self, dtr):
        self.ser.setDTR(dtr)
