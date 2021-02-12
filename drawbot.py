import serial
from time import sleep
import os


# connect to the 3D printer
def connect(port = '/dev/ttyUSB0', baud_rate=115200):

    # open the serial connection
    ser = serial.Serial(port,baud_rate)
    sleep(2)

    # check if the connection is successful
    print(ser.name)

    # return the connection object
    return ser


# get all of the files in the target folder
def get_files():

    return next(os.walk(path)[2])


# allow the user to select a file
def enumerate_selection(items):


    for i,item in enumerate(items):
        print("\t", i, ": ", item)

    index = int(input("ENTER SELECTION"))

    print("SELECTED:", items[index])

    return index


def main():

    # make the serial connection
    ser = connect()

    # select a file
    files = next(os.walk("files"))[2]
    index = enumerate_selection(files)

    # read the input file
    file = open(os.path.join("files",files[index]),'r')

    ser.reset_input_buffer()

    ser.write(b'G00 F5000;\n')
    ser.read_until()
    ser.write(b'G01 F3600;\n')
    ser.read_until()


    print(file.name)

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
