import os
import sys
import requests
from requests.packages import urllib3
import time
import json
import csv
from datetime import datetime
from datetime import timedelta


# Arguments ---------------------------------------------------------------

with open('inputfile.json', 'r') as infile:
    inputfile = json.load(infile)

stn_id = int(inputfile['stn_id'])
start_yr = int(inputfile['start_year'])
end_yr = int(inputfile['end_year'])
date_cd = inputfile['date_cd']
fname = 'data/' + inputfile['destination']
columns = ['STN_ID', 'TM'] + inputfile['features']

with open('api_key', 'r') as key:
    api_key = key.readline()


# Preparation -------------------------------------------------------------

# disable warning caused by option `verify = False` in requests.get()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not os.path.exists('data'):
    os.mkdir('data')

end_of_month = {
    1: 31, 2: 28, 3: 31,  4: 30,  5: 31,  6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}

def set_url(start_dt, end_dt, stn_id, date_cd, key):
    if date_cd == 'DAY':
        n = (ed - st).days + 1
    else:
        n = ((ed - st).days + 1) * 24
    start_dt = start_dt.strftime('%Y%m%d')
    end_dt = end_dt.strftime('%Y%m%d')
    url = (
        'https://data.kma.go.kr/apiData/getData?' +
        'type=json' +
        '&dataCd=ASOS' +
        '&dateCd=' + date_cd +
        '&startDt=' + start_dt +
        '&startHh=00' +
        '&endDt=' + end_dt +
        '&endHh=23' +
        '&stnIds=' + str(stn_id) +
        '&schListCnt=' + str(n) +
        '&pageIndex=1' +
        '&apiKey=' + key
    )
    return url


# Collect -----------------------------------------------------------------

with open(fname, 'w+') as outfile:
    csv_w = csv.writer(outfile)
    csv_w.writerow(columns)

for yr in range(start_yr, end_yr + 1):
    print('year', yr)
    for mn in range(1, 13):
        print('  month', mn)

        # set dates
        st = datetime(yr, mn, 1)
        ed = datetime(yr, mn, end_of_month[mn])
        if (mn == 2 and yr % 4 == 0):
            ed += timedelta(days = 1)

        # send request
        url = set_url(st, ed, stn_id, date_cd, api_key)
        response = requests.get(url, verify = False)
        time.sleep(1)

        # collect data
        data = response.json()[3]['info']
        with open(fname, 'a') as outfile:
            csv_w = csv.writer(outfile)
            for row in data:
                csv_w.writerow(map(lambda x: row.get(x, ''), columns))

        # check collected data are valid
        if date_cd == 'DAY':
            tms = map(lambda d: datetime.strptime(d['TM'], '%Y-%m-%d'), data)
            n_expected = (ed - st).days + 1
        else:
            tms = map(lambda d: datetime.strptime(d['TM'], '%Y-%m-%d %H:%M'), data)
            n_expected = ((ed - st).days + 1) * 24

        ## check date
        for tm in tms:
            if tm.year != yr:
                print('Warning: inconsistent year detected.')
            if tm.month != mn:
                print('Warning: inconsistent month detected.')

        ## check number of rows
        n_collected = len(data)
        if n_collected != n_expected:
            print('Warning: Number of rows does not match with the expected.')
            print('expected  :', n_expected)
            print('collected :', n_collected)
