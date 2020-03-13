import sys
import glob
import serial
import time
import re

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/c*')
    else:
        raise EnvironmentError('Unsupported platform')

    logger_port = ''
    for port in ports:
        if 'usbmodem' in port:
            try:
                s = serial.Serial(port)
                s.close()
                logger_port = port
            except (OSError, serial.SerialException):
                pass
    return logger_port


def get_files(port):
    filenames = []
    filename_regex = re.compile('^DATA[0-9]+.CSV')
    row_regex = re.compile('.+,.+,.+,.+')
    ser = serial.Serial(port, 9600)
    ser.reset_input_buffer()
    ser.write(b"send files")
    time.sleep(20)

    while True:
        ser_bytes = ser.readline()
        print(ser_bytes)
        try: 
            decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        except:
            decoded_bytes = ''
        print(decoded_bytes)
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
                    decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        # with open("test_data.csv", "a") as f:
        #     writer = csv.writer(f, delimiter=",")
        #     writer.writerow([time.time(), decoded_bytes])
if __name__ == '__main__':
    get_files(serial_ports())
