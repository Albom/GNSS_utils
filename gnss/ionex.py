
'''
(c) 2018-2021 Oleksandr Bogomaz

IONEX files parsing.
'''


from datetime import datetime, timedelta
from unlzw3 import unlzw

IONEX_VERSION_TYPE = 'IONEX VERSION / TYPE'
LAT_LON1_LON2_DLON_H = 'LAT/LON1/LON2/DLON/H'
END_OF_HEADER = 'END OF HEADER'
START_OF_TEC_MAP = 'START OF TEC MAP'
EPOCH_OF_CURRENT_MAP = 'EPOCH OF CURRENT MAP'
END_OF_TEC_MAP = 'END OF TEC MAP'


def read_ionex(filename):
    if filename.endswith('.Z'):
        with open(filename, 'rb') as file:
            compressed_data = file.read()
            uncompressed_data = unlzw(compressed_data).decode('utf-8')
            lines = uncompressed_data.replace('\r\n', '\n').split('\n')
    else:
        with open(filename, 'rt', encoding='utf-8') as file:
            lines = file.readlines()
    length = len(lines)
    n = 0
    while n < length:
        line = lines[n]
        n += 1
        description = line[60:].strip()
        if description == END_OF_HEADER:
            break
    result = []

    is_tec = False
    while n < length:
        line = lines[n]
        n += 1
        description = line[60:].strip()
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
                        'tec': tec})

        if description == END_OF_TEC_MAP:
            is_tec = False
            result.append({'i': k, 'date': date, 'data': data})

    return result


# plot 'tec.txt' using 2:1:3 w image, 'world_110m.txt' with line
def gnuplot(tec_maps, record, filename, append=False):
    with open(filename, 'a' if append else 'w', encoding='utf-8') as file:
        one_map = tec_maps[record]
        for d in one_map['data']:
            for n_long, tec in enumerate(d['tec']):
                lat = d['params'][0]
                long = d['params'][1] + n_long * d['params'][3]
                tec /= 10.0
                file.write('{} {} {}\n'.format(lat, long, tec))
            file.write('\n')
