import requests
from cStringIO import StringIO
import sys

cookies = {'Units':'english'}
url_formatted = 'http://www.wunderground.com/history/airport/{airport_code}/{year}/{month}/{day}/MonthlyHistory.html?req_statename=South%20Africa&reqdb.zip=00000&format=1'
wmo_url = 'http://www.wunderground.com/history/wmo/{wmo}/{year}/{month}/{day}/MonthlyHistory.html?req_city=Sutherland&req_statename=South%20Africa&reqdb.zip=00000&reqdb.magic=1&reqdb.wmo=&format=1'

def iter_lines(s):
    string_io = StringIO(s)
    while True:
        line = string_io.readline()
        if line != '':
            yield line.strip('\n')
        else:
            raise StopIteration

def process_content(cont):
    output_buffer=''
    for l in iter_lines(cont):
        html_removed = l.replace('<br />', '')
        if 'Temp' in html_removed or html_removed == '':
            continue
        output_buffer+= html_removed+'\n'
    return output_buffer

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s [airport_code_or_wmo_station] [another] [another] ...' % sys.argv[0]
        sys.exit(0)

    stations = sys.argv[1:]
    for year in range(1995,2017):
        for city in stations:
            output_file = open(city + '.csv','a')
            for month in range(1,13):
                try:
                    # covers WMO codes
                    if city.isdigit():
                        r = requests.get(wmo_url.format(wmo=city, year=year, month=month, day=1), cookies=cookies)
                    else:
                        r = requests.get(url_formatted.format(airport_code=city, year=year, month=month, day=1), cookies=cookies)
                except:
                    errfile = 'errors.txt'
                    ef = open(errfile, 'a')
                    ef.write('FAILED TO GET %s %s %s \n' % (year, month, city))
                    ef.close()
                    continue
                output_chunk = process_content(r.content)
                output_file.write(output_chunk)
                print r.content
            output_file.close()
