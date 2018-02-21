"""
input file has headers
"""

import csv
from itertools import islice
from datetime import datetime, date, timedelta
from collections import defaultdict
import json


NOTHING, READ, STREAK = ' #|'

def main():
    # INPUTS
    start = parse('2/7/2018')
    end = parse('2/22/2018')
    n = 3  # how long is the streak 'tail' (including the first day)
    input_path = 'example-input'

    #######################################################
    # table[book][day]
    table = defaultdict(lambda: defaultdict(lambda: NOTHING))

    # read input and populate table with READs
    reader = csv.reader(open(input_path, 'r'), delimiter='\t')
    for row in islice(reader, 1, None):
        s_date, shortcode = row
        d = parse(s_date)
        table[shortcode][to_string(d)] = READ

    streak_starters = {}
    shortcodes = sorted(table.keys())
    for d in date_range(start - timedelta(n), end):
        datestring = to_string(d)
        for s in shortcodes:
            if table[s][datestring] == READ:
                streak_starters[s] = d
            else:
                starter = streak_starters.get(s)
                if starter and d - starter < timedelta(n):
                    table[s][datestring] = STREAK


    print_tabular(table, start, end)

def print_json(table):
    print(json.dumps(table, indent=3, sort_keys=True))

def print_tabular(table, start_date, end_date):
    shortcodes = sorted(table.keys())
    print_row('----------', *shortcodes)
    for d in date_range(start_date, end_date):
        datestring = to_string(d)
        items = [table[s][datestring] for s in shortcodes]
        print_row(datestring, *items)

def print_row(*args):
    for each in args:
        print(each, end='\t')
    print()

def date_range(start_date, end_date):
    d = start_date
    while d <= end_date:
        yield d
        d += timedelta(1)

def to_string(d):
    return d.isoformat()

def parse(datestring):
    return datetime.strptime(datestring, '%m/%d/%Y').date()

if __name__ == '__main__':
    main()
