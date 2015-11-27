#!/usr/bin/env python
# Tue Jun  2 15:22:28 EDT 2015
import csv
from collections import defaultdict, OrderedDict
import operator
import time


class ReadCSV(object):

    'Read the CSV file exported by Gluco Meter and extract date as Xaxis list and mgdl as Yaxis dictionary'

    version = '0.2'

    def __init__(self, d, f=None):
        self._d = d
        self._data = defaultdict(list)
        if f:
            self._read_csv(f)

    def _sortdate(self, d):
        '''
        Convert the key(time) into time structure and convert it into epoch time and
        use that to sort the dict
        '''
        try:
            for k in sorted(d, key=lambda k: int(time.mktime(time.strptime(k, self._d['datefmt'])))):
                yield k, d[k]
        except ValueError:
            # Invalid date format"
            print "Invalid date format ?"
            yield 0, []

    def _read_csv(self, file):
        """
        Read csv file and extract data from it
        """
        if not file:
            return self._read_unknown()

        return self._read_data(file)

    def _read_data(self, file):
        data = defaultdict(list)
        with open(file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            try:
                for count, row in enumerate(reader):
                    if count > self._d['lines_to_skip']:
                        data[row[self._d['csvcol']['date']]].append(
                            (row[self._d['csvcol']['time']], row[self._d['csvcol']['mgdl']]))
            except IndexError:
                data = {}
        self._data = data

    def _read_unknown(self):
        data = defaultdict(list)
        return data

    def extract(self):
        xaxis = list()
        yaxis = defaultdict(list)

        for date, value in self._sortdate(self._data):
            for time, mgdl in value:
                if time and mgdl:
                    xaxis.append('{0}-{1}'.format(date, time))
                    yaxis['mg/dl'].append(int(mgdl))

        return xaxis, yaxis['mg/dl']

if __name__ == '__main__':
    wave_sense = {'csvcol': {'date': 1, 'mgdl': 3, 'time': 2},
                  'datefmt': '%m/%d/%y', 'lines_to_skip': 15}
    xaxis, yaxis = ReadCSV(wave_sense,'WaveSenseLog.csv').extract()
    print 'xaxis={0} yaxis={1}'.format(xaxis, yaxis)

    my_sgr = {'csvcol': {'date': 0, 'mgdl': 3, 'time': 1},
              'datefmt': '%b %d, %Y', 'lines_to_skip': 1}
    xaxis, yaxis =  ReadCSV(my_sgr,'mysugr_data_2015-06-03_2130.csv').extract()
    print 'xaxis={0} yaxis={1}'.format(xaxis, yaxis)
