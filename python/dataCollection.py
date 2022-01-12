from datetime import datetime


def read(ser):
    data = str(ser.readline())[2:][:-5] # the last bit gets rid of the new-line chars
    split = ""
    if data:
        split = [float(val) for val in data.split(',')]
    return data, split if split else data


async def csv(data, file, line=0):
    timestamp = datetime.strftime(datetime.now(), '%Y, %m, %d, %H, %M, %S.%f') + ','
    print('Line ' + str(line) + ': writing...' + timestamp + data)
    file.write(timestamp + data + '\n')
