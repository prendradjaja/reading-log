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
    end = date.today()
    start = end - timedelta(28)
    n = 7  # read at least this often (in days) to keep a streak going
    input_path = 'data.tsv'

    #######################################################
    # table[book][day]
    table = defaultdict(lambda: defaultdict(lambda: NOTHING))

    # read input and populate table with READs
    reader = csv.reader(open(input_path, 'r'), delimiter='\t')
    for row in islice(reader, 1, None):
        s_date, shortcode = row
        d = parse(s_date)
        table[shortcode][to_string(d)] = READ

    shortcodes = sorted(table.keys())
    for s in shortcodes:
        streak_start = None
        for d in date_range(start - timedelta(n), end):
            datestring = to_string(d)
            if table[s][datestring] == READ:
                if streak_start and d - streak_start < timedelta(n + 1):
                    fill_streak(table[s], streak_start, d)
                streak_start = d


    print_tabular(table, start, end)

def fill_streak(table_s, start, end):
    for d in date_range(start, end, include_start=False, include_end=False):
        datestring = to_string(d)
        table_s[datestring] = STREAK

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

def date_range(start_date, end_date, include_start=True, include_end=True):
    """
    Inclusive by default.
    """
    if not include_start:
        start_date += timedelta(1)
    if not include_end:
        end_date -= timedelta(1)
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
