import sys
import glob
import serial
import time
import re
import os
from serial.tools.list_ports import comports

def serial_ports():
    ports = comports()
    port = ''
    for p in ports:
        if p.description == "Feather M0":
            port = p.device
            break
    return port


def get_files(port):
    filenames = []
    filename_regex = re.compile('^DATA[0-9]+.CSV')
    row_regex = re.compile('.+,.+,.+,.+')
    ser = serial.Serial(port, 9600)
    ser.reset_input_buffer()
    ser.write(b"send files")
    time.sleep(10)

    while True:
        ser_bytes = ser.readline()
        try:
            decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        except:
            decoded_bytes = ''
        if filename_regex.match(decoded_bytes):
            if decoded_bytes in filenames:
                break
            filenames.append(decoded_bytes)
            with open(decoded_bytes, "w") as f:
                ser_bytes = ser.readline()
                decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
                while row_regex.match(decoded_bytes):
                    f.write(decoded_bytes + '\n')
                    ser_bytes = ser.readline()
                    decoded_bytes = ser_bytes[0:len(
                        ser_bytes)-2].decode("utf-8")
            print(filenames[-1] + ' successfully downloaded!')


if __name__ == '__main__':
    print("Welcome to the Direct Output Head Data Retrieval Tool!")
    port = ""
    while not port:
        port = input("Please enter the port name located in the bottom right corner of your Arduino IDE. If you would prefer for the program to search for it automatically, enter the word \"continue\" or enter \"quit\" to quit the program:\n").lower()
        if port == "continue":
            try:
                get_files(serial_ports())
            except:
                print(
                    "Sorry, the program was unable to find the appropriate port. Please try entering the port yourself.\n")
                port = ""
        elif port == "quit":
            print("Thanks for using the Direct Output Head Data Retrieval Tool!")
            sys.exit(0)
        else:
            try:
                get_files(port)
            except:
                print(
                    'That port was not accepted. Please try another port or allowing the program to search for a port.\n')
                port = ""
