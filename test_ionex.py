
'''
(c) 2018 Oleksandr Bogomaz

Test of IONEX files parsing.
'''

import gnss.ionex as ionex

if __name__ == '__main__':
    d = ionex.read_ionex('d:/codg3600.17i')
    lat = 50.0
    long = 35.0
    for r in d:
        print("\"" + str(r['date']) + "\"", end=' ')
        for t in r['data']:
            if abs(t['params'][0] - lat) < 1:
                n_long = 0
                while n_long*t['params'][3]+t['params'][1] <= t['params'][2]:
                    if abs(n_long*t['params'][3]+t['params'][1]-long) < 5:
                        break
                    n_long += 1
                print(t['tec'][n_long]/10.0)
