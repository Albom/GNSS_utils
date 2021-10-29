
'''
(c) 2018-2021 Oleksandr Bogomaz

Test of IONEX files parsing.
'''

import gnss.ionex as ionex

if __name__ == '__main__':
    d = ionex.read_ionex('data/uqrg0380.18i')
    ionex.gnuplot(d, 0, 'tec.txt')

    lat = 50.0
    long = 35.0
    for r in d:
        print("\"" + str(r['date']) + "\"", end=' ')
        for t in r['data']:
            if abs(t['params'][0] - lat) < 1:
                n_long = 0
                params = t['params']
                while n_long * params[3] + params[1] <= params[2]:
                    if abs(n_long * params[3] + params[1] - long) < 5:
                        break
                    n_long += 1
                print(t['tec'][n_long] / 10.0)
