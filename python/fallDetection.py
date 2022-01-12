import math
import asyncio
import time


async def update_fall(split, window, theta_z_offset, line, ser):
    # fall detection analysis
    window.append(split)

    will_fall = False
    if line > 29:
        window.pop(0)
    if line > 28:
        will_fall = fall_detection(window, theta_z_offset)

    print(split[0])

    if will_fall:
        asyncio.run(run_motor(ser, 5))  # vibrate for 10 seconds

    return window


async def run_motor(ser, duration):
    print('Fall detected.')
    ser.write(b'H')
    await asyncio.sleep(duration)
    ser.write(b'L')


def fall_detection(window, theta_z_offset):
    window_copy = window[:]
    params = calc_params(window_copy)
    Az = window_copy[-1][2] / 16384
    print(Az, type(Az))
    theta_z = math.acos(Az) + theta_z_offset

    if params['acc']['range'] > 0.4 or params['ang']['range'] > 60:
        if theta_z <= 35:
            if params['acc']['max'] >= 2.5 or params['ang']['max'] >= 340:
                return 1

    return 0


