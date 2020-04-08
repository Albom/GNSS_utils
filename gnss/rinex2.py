
'''
(c) 2017-2019 Oleksandr Bogomaz

RINEX 2 files parsing.
'''

from datetime import datetime
from gnss.header import Header as Header
import re


def read_obs(filename, header_only=False):
    header = Header()
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    length = len(lines)
    n = 0
    while True:
        line = lines[n]
        n += 1
        description = line[60:].strip()
        if description == Header.END_OF_HEADER:
            break
        elif description == Header.RINEX_VERSION_TYPE:
            header.set_version(line[:9].strip())
            if not header.get_version().startswith('2'):
                return {'header': header}
            header.set_type(line[20:21])
            if header.get_type() != 'O':
                return {'header': header}
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
            for i in range(9):
                if len(header.get_types_of_obs()) < header.get_num_of_obs():
                    obs = line[6 + 6 * i:6 + 6 * (i + 1)].strip()
                    header.add_types_of_obs(obs)
        elif description == Header.LEAP_SECONDS:
            header.set_leap_seconds(int(line[: 6].strip()))

    if header_only:
        return {'header': header}

    data = []
    while n < length:
        line = lines[n]

        # skip comments
        description = line[60:].strip()
        if description == Header.COMMENT:
            n += 1
            continue

        # skip bad lines
        if not re.match(' \d\d', line):
            n += 1
            continue

        year = int(line[1:3])
        year += 2000 if year < 80 else 1900
        month = int(line[4:6])
        day = int(line[7:9])
        hh = int(line[10:12])
        mm = int(line[13:15])
        ss = float(line[15:26])
        date = datetime(year, month, day, hh, mm, int(ss), int((ss % 1) * 1e6))

        num_of_sat = int(line[30:32])
        satellites = []
        while len(satellites) < num_of_sat:
            s = line[32:].strip()
            ns = len(s)//3
            for i in range(ns):
                sat = line[32 + i * 3:35 + i * 3]
                if sat:
                    satellites.append(sat)
            n += 1
            line = lines[n]

        all_parameters = {}
        for s in satellites:
            param = []
            while len(param) < header.get_num_of_obs():
                for i in range(5):
                    if (len(param) < header.get_num_of_obs()):
                        obs = line[i * 16:i * 16 + 14].strip()
                        obs = float(obs) if obs else None
                        param.append(obs)
                if (n < length - 1):
                    n += 1
                    line = lines[n]
            all_parameters[s] = param

        data.append({'date': date,
                     'num': num_of_sat,
                     'sat': satellites,
                     'param': all_parameters})

    return {'header': header, 'data': data}


def read_nav(filename):

    def d2float(d):
        return float(d.strip().replace('D', 'E').replace('d', 'E'))

    header = Header()
    with open(filename) as file:
        lines = file.readlines()
    length = len(lines)
    n = 0
    while True:
        line = lines[n]
        n += 1
        description = line[60:].strip()
        if description == Header.END_OF_HEADER:
            break
        elif description == Header.RINEX_VERSION_TYPE:
            header.set_version(line[:9].strip())
            if not header.get_version().startswith('2'):
                return {'header': header}
            header.set_type(line[20:21])
            if header.get_type() != 'N':
                return {'header': header}
        elif description == Header.ION_ALPHA:
            a = [d2float(line[2 + i*12: 2 + i*12 + 12]) for i in range(4)]
            header.set_ion_alpha(a)
        elif description == Header.ION_BETA:
            b = [d2float(line[2 + i*12: 2 + i*12 + 12]) for i in range(4)]
            header.set_ion_beta(b)
        elif description == Header.DELTA_UTC_A0_A1_T_W:
            a0 = d2float(line[3: 3 + 19])
            a1 = d2float(line[3 + 19: 3 + 19*2])
            t = int(line[3 + 19*2: 3 + 19*2 + 9])
            w = int(line[3 + 19*2 + 9: 3 + 19*2 + 9*2])
            header.set_delta_utc({'A0': a0, 'A1': a1, 'T': t, 'W': w})
        elif description == Header.LEAP_SECONDS:
            header.set_leap_seconds(int(line[: 6].strip()))

    data = []
    while n < length:
        line = lines[n]
        bo = [x for x in lines[n+1: n+1+8]]
        n += 8

        sat = line[:2]

        year, month, day, hh, mm = [int(line[3+i*3:3+i*3+2]) for i in range(5)]
        year += 2000 if year < 80 else 1900
        ss = float(line[17:22])
        date = datetime(year, month, day, hh, mm, int(ss), int((ss % 1) * 1e6))
        sv_clock_bias, sv_clock_drift, sv_clock_drift_rate = \
            [d2float(line[22 + i*19: 22 + i*19 + 19]) for i in range(3)]

        iode, crs, delta_n, m0 = \
            [d2float(bo[0][3 + i*19: 3 + i*19 + 19]) for i in range(4)]

        cuc, e, cus, sqrt_a = \
            [d2float(bo[1][3 + i*19: 3 + i*19 + 19]) for i in range(4)]

        toe, cic, OMEGA, cis = \
            [d2float(bo[2][3 + i*19: 3 + i*19 + 19]) for i in range(4)]

        i0, crc, omega, OMEGA_DOT = \
            [d2float(bo[3][3 + i*19: 3 + i*19 + 19]) for i in range(4)]

        idot, codes_l2_channel, gps_week, l2_p_data_flag = \
            [d2float(bo[4][3 + i*19: 3 + i*19 + 19]) for i in range(4)]

        sv_accuracy, sv_health, tgd, iodc = \
            [d2float(bo[5][3 + i*19: 3 + i*19 + 19]) for i in range(4)]

        transmission_time, fit_interval = \
            [d2float(bo[6][3 + i*19: 3 + i*19 + 19]) for i in range(2)]

        parameters = {
            'sat': sat,
            'date': date,
            'sv_clock_bias': sv_clock_bias,
            'sv_clock_drift': sv_clock_drift,
            'sv_clock_drift_rate': sv_clock_drift_rate,
            'iode': iode,
            'crs': crs,
            'delta_n': delta_n,
            'm0': m0,
            'cuc': cuc,
            'e': e,
            'cus': cus,
            'sqrt_a': sqrt_a,
            'toe': toe,
            'cic': cic,
            'OMEGA': OMEGA,
            'cis': cis,
            'i0': i0,
            'crc': crc,
            'omega': omega,
            'OMEGA_DOT': OMEGA_DOT,
            'idot': idot,
            'codes_l2_channel': codes_l2_channel,
            'gps_week': gps_week,
            'l2_p_data_flag': l2_p_data_flag,
            'sv_accuracy': sv_accuracy,
            'sv_health': sv_health,
            'tgd': tgd,
            'iodc': iodc,
            'transmission_time': transmission_time,
            'fit_interval': fit_interval}

        data.append(parameters)

    return {'header': header, 'data': data}
