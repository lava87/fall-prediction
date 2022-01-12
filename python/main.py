import asyncio
import serial
import math
import time

from dataCollection import csv, read
from phaseDetection import detect_phase
from calibration import calibration


# Set COM to the Arduino COM and set baud rate to same val in arduino (ie. Serial.begin(115200);)
arduino_port = 'COM5'  # COM3 is zoey, COM5 is valerie
baud = 115200
ser = serial.Serial(arduino_port, baud, timeout=.1)
ser.close()
ser.open()  # this will also reboot the arduino

file = open('fuzzyfootdata.csv', 'w')
file.write('Year,Month,Day,Hour,Min,Sec,AcX,AcY,AcZ,GyX,GyY,GyZ\n')

# Set number of samples
samples = 400
line = 0

# Initialize offsets and window
ac_offset, gy_offset, window = calibration(ser, file)
print(ac_offset)
print(gy_offset)
will_fall = 0
prev_phase = 1  # default with FlatFoot from Phases enum
phase_count = 0  # counts the number of previous phases that were the same

while line <= samples:
    # reading data - gotta change it for our data
    data, split = read(ser)

    if data:
        asyncio.run(csv(data, file, line))
        # detect phase
        window, prev_phase, phase_count = \
            asyncio.run(detect_phase(window, split, ac_offset, gy_offset, prev_phase, phase_count, ser))
        line += 1

ser.write(b'L')
file.close()
