#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function

import argparse
import sys
import json
import codecs
import os
from .types import *
from .settings import Settings, WEATHER_CONF_FILE


class ResultPrinter(object):
    """
    Responsible for printing weather underground API results
    in a formatted manner.
    """
    def __init__(self, out=None, settings=None):
        self.out = out
        self.settings = settings

        if self.out is None:
            if sys.version_info >= (3, 0):
                self.out = sys.stdout
            else:
                # Wrap sys.stdout in a utf8 stream writer in case output
                # is piped
                self.out = codecs.getwriter('utf8')(sys.stdout)

        if not self.settings:
            self.settings = Settings()

    def _print(self, msg):
        # convert bytes (python 3) or unicode (python 2) to str
        print(msg, file=self.out)

    def print_alerts(self, data):
        """
        Prints any weather alerts in red
        """
        if not len(data['alerts']):
            self._print("No alerts for {0}".format(data['current_observation']['display_location']['full']))

        for alert in data['alerts']:
            self._print("\033[91m" + alert['message'].rstrip("\n") + "\nExpires: " + alert['expires'] + "\033[0m")

    def print_conditions(self, data):
        """
        Prints the current weather conditions
        """
        self._print("Weather for {0}".format(data['display_location']['full']))

        temp_c = format_degree({"metric": data['temp_c']}, Units.METRIC)
        temp_f = format_degree({"english": data['temp_f']}, Units.ENGLISH)
        if self.settings.units == Units.METRIC:
            self._print(u"Currently: {0} ({1}) {2}".format(temp_c, temp_f, data["weather"]))
        else:
            self._print(u"Currently: {0} ({1}) {2}".format(temp_f, temp_c, data["weather"]))

        self._print("Wind: {0}".format(data['wind_string']))
        self._print("Humidity: {0}".format(data['relative_humidity']))

    def print_hourly(self, data):
        """
        Prints the hourly weather data in a table
        """
        # Need to generate an array to send the print_table, first row must be the keys
        val = []
        val.append(["Date", "Hour", "Temperature", "Chance of Rain", "Weather"])

        for item in data:
            time = format_hour(item["FCTTIME"], self.settings.time)
            date = format_date(item["FCTTIME"], self.settings.date)
            temp = format_degree(item["temp"], self.settings.units)
            val.append([date, time, temp, item["pop"] + "%", item['condition']])

        self._print("36 Hour Hourly Forecast:")
        self._print_table(val)

    def print_forecast(self, data):
        """
        Prints the forcast data in a table
        """
        unit = self.settings.units
        val = []
        # Need to generate an array to send the print_table, first row must be the keys
        val.append(["Date", "Condition", "Chance of Rain", "Temp (Hi/Lo)", "Wind", "Humidity"])

        for item in data:
            date = item['date']
            date_str = format_date(date, self.settings.date)
            temp = u"{0} / {1}".format(format_degree(item['high'], unit),
                                       format_degree(item['low'], unit))
            wind = format_windspeed(item['avewind'], unit)

            hum = str(item["avehumidity"]) + "%"
            val.append([date_str, item['conditions'], str(item["pop"]) + "%", temp, wind, hum])

        print("Weather Forecast:")
        self._print_table(val)

    def _print_table(self, table):
        """
        Aligns and prints an array into a formatted table

        Requires that the first row in the array contain the column names
        and that each row contains the same number of elements
        """
        max_col_widths = []
        for col in range(len(table[0])):
            max_col_widths.append(self._get_max_col_width(table, col))

        self.out.write((table[0][0].ljust(max_col_widths[0] + 1)))
        for i in range(1, len(table[0])):
            col = table[0][i].rjust(max_col_widths[i] + 2)
            self.out.write(col)

        self._print("")
        self._print("-" * (sum(max_col_widths) + 3 * len(max_col_widths)))

        table.pop(0)
        for row in table:
            self.out.write(row[0].ljust(max_col_widths[0] + 1))
            for i in range(1, len(row)):
                col = row[i].rjust(max_col_widths[i] + 2)
                self.out.write(col)

            self._print("")

    def _get_max_col_width(self, table, column_index):
        """
        Returns the length of the longest string in any column
        """
        return max([len(row[column_index]) for row in table])


FORMAT_STRINGS = {
    'windspeed': "~{0:2}{1} {2:3}",
    'date': "{0} {1:3}",
    'temp': u"{0:3}\u00B0{1:1}",
    'military': u"{0}:{1}",
}


def format_degree(temp_dict, unit):
    """
    Takes a dictionary from the Weather underground api
    and returns a formatted temperature string ex: "62 °F", "25 °C"
    """
    symbol = "C" if unit == Units.METRIC else "F"

    temp = temp_dict.get('fahrenheit') or temp_dict.get('english')
    if unit == Units.METRIC:
        temp = temp_dict.get('celsius') or temp_dict.get('metric')

    # For whatever reason, weather underground returns temps
    # as both strings and ints
    return FORMAT_STRINGS['temp'].format(str(temp), symbol)


def format_windspeed(windspeed_dict, unit):
    """
    Returns a formatted windspeed, for example,
    >>>format_windspeed({
            'kph': 04,
            'mph': 02,
            'dir': NW,
       }, Units.ENGLISH)
    >>>'~02mph NW
    """
    direction = Direction.shorthand(windspeed_dict['dir'])
    idx = 'kph' if unit == Units.METRIC else 'mph'
    return FORMAT_STRINGS['windspeed'].format(str(windspeed_dict[idx]), idx,
                                              direction)


def format_hour(time_dict, time_format):
    if time_format == TimeFormats.MILITARY:
        return FORMAT_STRINGS['military'].format(time_dict['hour_padded'],
                                                 time_dict['min'])
    else:
        return time_dict['civil']


def format_date(date, date_format):
    """
    Returns a date string, 'April 2' for example
    """
    if date_format == DateFormats.DATE or 'weekday_short' not in date:
        if 'monthname' in date:
            return FORMAT_STRINGS['date'].format(str(date['monthname']), str(date['day']))
        else:
            return FORMAT_STRINGS['date'].format(str(date['mon_abbrev']), str(date['mday']))
    else:
        return date['weekday_short']


def print_weather_data(data, args, settings):
    """
    Prints the supplied weather data as specified by the options and program arguments.
    """
    data = json.loads(data.decode('utf-8'))

    if 'error' in data['response']:
        print(data['response']['error']['description'])
        return

    if 'results' in data['response']:
        print("More than 1 city matched your query, try being more specific")
        for result in data['response']['results']:
            print("{0}, {1} {2}".format(result['name'], result['state'],
                                        result['country_name']))
        return

    result_printer = ResultPrinter(settings=settings)
    if args.alerts:
        result_printer.print_alerts(data)
        print("")
    if args.now:
        result_printer.print_conditions(data['current_observation'])
        print("")
    if args.hourly:
        result_printer.print_hourly(data['hourly_forecast'])
        print("")
    if args.forecast or args.extended:
        result_printer.print_forecast(data['forecast']['simpleforecast']['forecastday'])
        print("")


def make_query_path(args):
    """
    Returns a path to use against the weather underground API
    by parsing program arguments.
    """
    query = ""

    paths = {
        "now": "conditions/alerts/",
        "forecast": "forecast/",
        "extended": "forecast10day/",
        "hourly": "hourly/",
    }

    # In the case no options are set, use the default
    if not (args.now or args.hourly or args.alerts or args.forecast or
            args.extended):
        args.now = True

    if args.now or args.alerts:
        query += paths['now']
    if args.hourly:
        query += paths['hourly']
    if args.forecast:
        query += paths['forecast']
    if args.extended:
        query += paths['extended']
    return query


def make_api_url(args, settings):
    """
    Returns a url to the weather underground API endpoint by parsing
    program arguments.
    """
    base_url="http://api.wunderground.com/api/%s/" % settings.api_key

    # Create a location string, or use autoip
    query="q/%s.json"
    if args.location:
        query = query % "_".join(args.location);
    else:
        query = query % "autoip"

    return base_url + make_query_path(args) + query


def parse_args():
    parser = argparse.ArgumentParser(description="Display the current weather, or forecast")
    parser.add_argument('location', nargs='*', help='Optional location, by default uses geoip')

    parser.add_argument('-n', '--now', help='Get the current conditions (Default)',
                        action='store_true')
    parser.add_argument('-f', '--forecast', help='Get the current forecast',
                        action='store_true')
    parser.add_argument('-e', '--extended', help='Get the 10 day forecast',
                        action='store_true')
    parser.add_argument('-o', '--hourly', help='Get the hourly forecast',
                        action='store_true')
    parser.add_argument('-a', '--alerts', help='View any current weather alerts',
                        action='store_true')
    parser.add_argument('-t', '--time', choices=TimeFormats.to_array(),
                        help='Set time format to use (default is \'civilian\')')
    parser.add_argument('-d', '--date', choices=DateFormats.to_array(),
                        help='Set date format to use (default is \'date\')')
    parser.add_argument('-u', '--units', choices=Units.to_array(),
                        help='Set units to use (default is \'english\')')
    return parser.parse_args()


def main():
    import requests
    args = parse_args()
    settings = Settings(args)
    api_url = make_api_url(args, settings)
    r = requests.get(api_url)
    print_weather_data(r.content, args, settings)


if __name__ == "__main__":
    main()

