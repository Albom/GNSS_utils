
'''
(c) 2018 Oleksandr Bogomaz

IONEX files parsing.
'''

from _datetime import datetime, timedelta

IONEX_VERSION_TYPE = 'IONEX VERSION / TYPE'
LAT_LON1_LON2_DLON_H = 'LAT/LON1/LON2/DLON/H'
END_OF_HEADER = 'END OF HEADER'
START_OF_TEC_MAP = 'START OF TEC MAP'
EPOCH_OF_CURRENT_MAP = 'EPOCH OF CURRENT MAP'
END_OF_TEC_MAP = 'END OF TEC MAP'


def read_ionex(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    length = len(lines)
    n = 0
    while n < length:
        line = lines[n]
        n += 1
        description = line[60:-1].strip()
        if description == END_OF_HEADER:
            break

    result = []

    is_tec = False
    while n < length:
        line = lines[n]
        n += 1
        description = line[60:-1].strip()
        if description == START_OF_TEC_MAP:
            k = int(line[:6])
            data = []
            is_tec = True

        if description == EPOCH_OF_CURRENT_MAP:
            year = int(line[:6])
            month = int(line[6:12])
            day = int(line[12:18])
            hh = int(line[18:24])
            next_day = False
            if hh >= 24:
                hh -= 24
                next_day = True
            mm = int(line[24:30])
            ss = int(line[30:36])
            date = datetime(year, month, day, hh, mm, ss)
            if next_day:
                date = date + timedelta(days=1)

        if description == LAT_LON1_LON2_DLON_H:
            if is_tec:
                lat = float(line[2:8])
                lon1 = float(line[8:14])
                lon2 = float(line[14:20])
                dlon = float(line[20:26])
                h = float(line[26:32])
                n_tec = int((lon2 - lon1) / dlon) + 1
                tec = []
                while len(tec) < n_tec:
                    line = lines[n]
                    n += 1
                    t = line.split()
                    for v in t:
                        tec.append(int(v))
            data.append({'params': (lat, lon1, lon2, dlon, h),
                        'tec': tuple(tec)})

        if description == END_OF_TEC_MAP:
            is_tec = False
            result.append({'i': k, 'date': date, 'data': tuple(data)})

    return tuple(result)

