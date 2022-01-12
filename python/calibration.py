import asyncio
import math
import time

from dataCollection import read, csv

gravity = 9.81
accel_difference = 1  # can decrease to increase accuracy


def calibration(ser, file):
    calibration_window = []
    print('Calibrating...')
    while len(calibration_window) < 40:  # 40 for overhead space in case user moves
        data, split = read(ser)
        if data:
            asyncio.run(csv(data, file))
            calibration_window.append(split)
            if len(calibration_window) > 10:
                calibration_window.pop()
            if len(calibration_window) == 10:  # window size of 10
                ac_avg = sum([i[2] for i in calibration_window]) / len(calibration_window)
                gy_avg = sum(i[4] for i in calibration_window) / len(calibration_window)
                if abs(ac_avg - gravity) < accel_difference or abs(ac_avg + gravity) < accel_difference:
                    # the second part is in case the user put on upside down
                    calibration_done(ser, file)
                    return ac_avg, gy_avg, calibration_window
                else:
                    calibration_window.pop(0)


def calibration_done(ser, file):
    file.write('-,-,-,-,-,-,-,-,-,-,-,-\n')
    print('Calibration complete.')

    #  Vibration notification
    ser.write(b'H')
    time.sleep(1)
    ser.write(b'L')

