import serial
from time import sleep
import os




ser = None


# connect to the 3D printer
def connect(port = '/dev/ttyUSB0', baud_rate=115200):

    # open the serial connection
    ser = serial.Serial(port,baud_rate)
    sleep(2)

    # check if the connection is successful
    print(ser.name)


def wait(x):
    sleep(x)

# connect to the 3D printer
def disconnect():
    ser = None

# run the input filename
def run(filename):

    if ser is None:
        print("NO SERIAL CONNECTION")
        return False

    # read the input file
    file = open(os.path.join("files",filename),'r')

    ser.reset_input_buffer()

    ser.write(b'G00 F5000;\n')
    ser.read_until()
    ser.write(b'G01 F3600;\n')
    ser.read_until()

    # send the file to print
    for line in file:
        print(line)
        ser.write((line+"\n").encode('utf-8'))
        # get the ok message
        ser.read_until()

    sleep(5)
    ser.flush_input_buffer()

    ser.write(b'G28;/n')
    sleep(10)
    ser.close()
    file.close()



if __name__ == "__main__":
    main()
