
'''
(c) 2017 Oleksandr Bogomaz

RINEX files parsing.
'''

from gnss.header import Header as Header
from _datetime import datetime


def read_obs(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    header = Header()
    n = 0
    while True:
        line = lines[n]
        n += 1
        description = line[60:-1].strip()
        if description == Header.END_OF_HEADER:
            break
        elif description == Header.RINEX_VERSION_TYPE:
            header.set_version(line[:9].strip())
            header.set_type(line[20:21])
            if header.get_type() != 'O':
                return {}
        elif description == Header.APPROX_POSITION_XYZ:
            d = 14
            header.set_pos({'x': float(line[:d]),
                            'y': float(line[d:2 * d]),
                            'z': float(line[2 * d:3 * d])})
        elif description == Header.TYPES_OF_OBSERV:
            num_of_obs = line[:6].strip()
            num_of_obs = int(num_of_obs) if len(num_of_obs) > 0 else 0
            if num_of_obs > 0:
                header.set_num_of_obs(num_of_obs)
            for i in range(0, 9):
                if len(header.get_types_of_obs()) < header.get_num_of_obs():
                    obs = line[6 + 6 * i:6 + 6 * (i + 1)].strip()
                    header.add_types_of_obs(obs)

    while n < len(lines):
        line = lines[n]
        num_of_sat = int(line[30:32])
        year = int(line[1:3])
        year += 2000 if year < 80 else 1900
        month = int(line[4:6])
        day = int(line[7:9])
        hh = int(line[10:12])
        mm = int(line[13:14])
        ss = float(line[15:26])
        date = datetime(year, month, day, hh, mm, int(ss), int((ss % 1) * 1e6))
        print(date.isoformat(), num_of_sat)
        n += num_of_sat * 2 + 1 + (1 if num_of_sat > 12 else 0)

    return {'header': header}
