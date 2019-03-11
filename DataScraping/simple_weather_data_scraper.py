# IMSE785
# KANSAS STATE UNIVERSITY

import argparse
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
from datetime import datetime as dt, timedelta
import csv
from os import path


def get_weather_data(zipcode, date):
    url = 'https://www.almanac.com/weather/history/zipcode/%s/%s' % (zipcode, date)
    print(url + '\n-------')
    weather_data = {}
    try:
        page = urlopen(url)
    except HTTPError as e:
        print('* Fail to load page, possiblly for invalid zip code.')
    else:
        soup = BS(page, 'html.parser')
        location = soup.find(id='page-title').string.strip() + ', %s:' % date
        print(location)
        data_blocks = soup.find_all(attrs={'class':'weatherhistory_results_datavalue'})
        if len(data_blocks):
            for block in data_blocks:
                # print(block.contents[1].p.contents[0].string)
                print(block.h3.string, block.contents[1].p.get_text())
                weather_data['Date'] = date
                weather_data[block.h3.string] = block.contents[1].p.contents[0].string
        else:
            print('* Failed to load data.')
    print('\n')
    return weather_data

def collect_weather_data(zipcode, date, days):
    start = dt.strptime(date, '%Y-%m-%d')
    end = start + timedelta(days=days)
    if start > end:
        start, end = end, start
        days = abs(days - 1)
    print('Collecting weather data for zip code: %s, between dates: %s and %s...'
        % (zipcode, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))

    dates = [dt.strftime(start + timedelta(days=x), "%Y-%m-%d") for x in range(0, days)]
    weather_data_list = []
    for date in dates:
        weather_data_list.append(get_weather_data(zipcode, date))
    return weather_data_list


def write_to_csv(path, contents_list):
    with open(path, 'w', newline='') as fp:
        csv_writer = csv.DictWriter(fp, fieldnames=contents_list[0].keys())
        csv_writer.writeheader()
        for row in contents_list:
            csv_writer.writerow(row)
        return len(contents_list)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('zipcode', help='Specify 5-digit zip code, e.g. 66506')
    parser.add_argument('date', help='Specify date in format YYYY-MM-DD, e.g. 2015-01-01')
    parser.add_argument('-d', '--days', metavar='days', type=int, help='Specify number of days to check, e.g. 30')
    # TODO: optional argument for specifying path of csv output
    parser.add_argument('-p', '--path', metavar='path', help='Specify file path to save output csv file, e.g. results.csv')
    args = parser.parse_args()
    if args.zipcode and args.date:
        try:
            dt.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print('Invalid date: ', args.date)
        else:
            if args.days:
                weather_data_list = collect_weather_data(args.zipcode, args.date, args.days)
                if args.path:
                    try:
                        if path.isfile(args.path):
                            if input('File exists! Overwrite? (Y/N) ') not in ('Y', 'y'):
                                print('Cancelled.\n')
                                return 0
                        print("%d rows written to %s \n" % (write_to_csv(args.path, weather_data_list), args.path))
                    except IOError as e:
                        raise
            else:
                get_weather_data(args.zipcode, args.date)
    else:
        print(parse.print_help())

if __name__ == '__main__':
    main()
