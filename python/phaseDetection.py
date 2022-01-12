import math
import asyncio
import enum


class Phases(enum.Enum):
    FlatFoot = 1
    ToeOff = 2
    Swing = 3
    HeelStrike = 4


delay_after_ff = 20
delay_after_to = 5
delay_after_sw = 15
delay_after_hs = 10

threshold_after_to = 15
threshold_after_swing = 25
acc_threshold = -8


async def detect_phase(window, split, ac_offset, gy_offset, prev_phase, phase_count, ser):
    '''
    detect phase based on previous phase and magnitudes of AcZ and GyY averages
    '''
    window.pop(0)
    window.append(split)
    ac_avg, gy_avg = await get_averages(window, ac_offset, gy_offset)
    curr_phase = await get_curr_phase(prev_phase, ac_avg, gy_avg, phase_count)

    if curr_phase == prev_phase:
        phase_count += 1
        print('Phase: ' + str(Phases(prev_phase)) + '; Count: ' + str(phase_count) + '; AcZ_avg: ' + str(ac_avg))
    else:
        phase_count = 0

    if await will_fall(curr_phase, phase_count, ac_avg):
        print('Fall detected')
        await run_motor(ser, 0.05)  # ensure it vibrates for at least 5 periods (50 ms)
    else:
        await motor_off(ser)

    return window, curr_phase, phase_count


async def get_averages(window, ac_offset, gy_offset):
    ac_avg = sum([i[2] for i in window]) / len(window)
    gy_avg = sum([i[4] for i in window]) / len(window)
    return (ac_avg - ac_offset), (gy_avg - gy_offset)


async def get_curr_phase(prev_phase, ac_avg, gy_avg, phase_count):
    # temporary thresholds
    if Phases(prev_phase) == Phases.FlatFoot and phase_count > delay_after_ff:
        print('Looking for Toe off phase...')
        if gy_avg > 2 and ac_avg < 1:
            return prev_phase + 1
    elif Phases(prev_phase) == Phases.ToeOff and phase_count > delay_after_to:
        print('Looking for Swing phase...')
        if ac_avg > 2:
            return prev_phase + 1
    elif Phases(prev_phase) == Phases.Swing and phase_count > delay_after_sw:
        print('Looking for Heel strike phase...')
        if ac_avg > 1 and gy_avg > 1:
            return prev_phase + 1
    elif Phases(prev_phase) == Phases.HeelStrike and phase_count > delay_after_hs:
        print('Looking for Flatfoot phase...')
        if -1 < ac_avg < 1 and -1 < gy_avg < 1:
            return 1
    return prev_phase


async def will_fall(curr_phase, phase_count, ac_avg):
    if Phases(curr_phase) == Phases.ToeOff and phase_count > threshold_after_to:
        # detect fall after Toe off if user doesn't lift foot up enough
        return True
    elif Phases(curr_phase) == Phases.Swing and phase_count > threshold_after_swing:
        # detect fall after Swing if user doesn't continue to swing their foot past mid swing
        if ac_avg < acc_threshold:
            return True
    return False


async def run_motor(ser, duration):
    print('Fall detected.')
    ser.write(b'H')
    await asyncio.sleep(duration)


async def motor_off(ser):
    ser.write(b'L')
