
'''
Drawbot class

This class handles the serial connection and basic methods to control the drawbot.
'''

import serial
import threading
from time import sleep
import os

class Drawbot:

    def __init__(self):
        self.ser = None
        self.thread = None
        self.stop_threads = False

    # connect to the 3D printer
    def connect(self, port = '/dev/ttyUSB0', baud_rate=115200):

        # open the serial connection
        self.ser = serial.Serial(port,baud_rate)
        sleep(2)

        print(self.ser)

    # only used for threading testing
    def wait(self, x):
        sleep(x)

    # connect to the 3D printer
    def disconnect(self):
        self.ser = None

    # check if the drawbot is connected
    def is_connected(self):
        return not self.ser is None

    # command the drawbot to home
    def home(self):
        self.ser.write(b'G28;\n')
        self.ser.read_until()
        self.ser.write(b'G00 Z0.5;\n')
        self.ser.read_until()

    # kill the running thread
    def stop(self):
        if self.is_running():
            self.stop_threads = True

    # run the input filename
    def run(self, filename):

        if self.ser is None:
            print("NO SERIAL CONNECTION")
            return False

        # read the input file
        file = open(os.path.join("files",filename),'r')

        self.ser.reset_input_buffer()

        self.ser.write(b'G00 F5000;\n')
        self.ser.read_until()
        self.ser.write(b'G01 F3600;\n')
        self.ser.read_until()

        # send the file to print
        for line in file:

            if self.stop_threads:
                print("STOPPED!")

                self.stop_threads = False
                break

            print(line)
            self.ser.write((line+"\n").encode('utf-8'))
            # get the ok message
            self.ser.read_until()

        print("DONE!c")
        self.ser.write(b'G28;/n')
        self.ser.read_until()
        self.ser.close()
        file.close()

    # run the gcode asynchronously
    def run_async(self, filename):

        if self.is_running():
            return False

        self.stop_threads = False
        
        self.thread = threading.Thread(target=self.run, args=(filename,))
        self.thread.start()

    # check if the thread is running
    def is_running(self):
        if self.thread is None:
            return False

        return self.thread.is_alive()