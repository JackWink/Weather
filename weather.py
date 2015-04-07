#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests
import argparse
import sys
import json
import codecs
import os

WEATHER_CONF_FILE = "~/.weatherrc"

class Units(object):
    METRIC = "metric"
    ENGLISH = "english"

    @staticmethod
    def to_array():
        return [Units.METRIC, Units.ENGLISH]

class TimeFormats(object):
    MILITARY = "military"
    CIVILIAN = "civilian"

    @staticmethod
    def to_array():
        return [TimeFormats.MILITARY, TimeFormats.CIVILIAN]

class Direction(object):
    @staticmethod
    def shorthand(direction):
        normalized = direction.lower()
        if normalized == "east":
            return "E"
        if normalized == "west":
            return "W"
        if normalized == "south":
            return "S"
        if normalized == "north":
            return "N"
        return direction


class Settings(object):
    """
    Contains the settings held in the WEATHER_CONF_FILE.
    """
    # Cache of the class level settings
    settings  = None
    file_path = None

    def __init__(self, args=None):
        if not args:
            args = {}

        if not Settings.settings:
            Settings.file_path = os.path.expanduser(WEATHER_CONF_FILE)
            if not os.path.exists(Settings.file_path):
                Settings.generate_default_weatherrc()

            with open(Settings.file_path) as weatherrc:
                Settings.settings = json.load(weatherrc)

        if "units" in args and args.units:
            Settings.settings["units"] = args.units

        if "time" in args and args.time:
            Settings.settings["time"] = args.time

        if "units" not in Settings.settings or Settings.settings["units"] is None:
            Settings.settings["units"] = Units.ENGLISH

        if "time" not in Settings.settings or Settings.settings["time"] is None:
            Settings.settings["time"] = TimeFormats.CIVILIAN

    @staticmethod
    def generate_default_weatherrc():
        """
        Writes a default weather conf file
        """
        with open(Settings.file_path, "w") as weatherrc:
            weatherrc.write("\n".join(["{", '"api_key": "your-api-key",',
                                            '"units": "english",',
                                            '"time": "civilian"', "}"]))

    def __getattr__(self, attr):
        """
        Proxy attribute requests to the settings cache
        """
        return Settings.settings[attr]

class ResultPrinter(object):
    """
    Responsible for printing weather underground API results
    in a formatted manner.
    """
    def __init__(self, out=None, settings=None):
        self.out = out
        self.settings = settings

        if self.out is None:
            # Wrap sys.stdout in a utf8 stream writer in case output is piped
            self.out = codecs.getwriter('utf8')(sys.stdout)

        if not self.settings:
            self.settings = Settings()


    def print_alerts(self, data):
        """
        Prints any weather alerts in red
        """
        if not len(data['alerts']):
            print >> self.out, "No alerts for {0}".format(data['current_observation']['display_location']['full'])

        for alert in data['alerts']:
            print >> self.out, "\033[91m" + alert['message'].rstrip("\n") + "\nExpires: " + alert['expires'] + "\033[0m"

    def print_conditions(self, data):
        """
        Prints the current weather conditions
        """
        print >> self.out, "Weather for {0}".format(data['display_location']['full'])

        temp_c = format_degree({"metric": data['temp_c']}, Units.METRIC)
        temp_f = format_degree({"english": data['temp_f']}, Units.ENGLISH)
        if self.settings.units == Units.METRIC:
            print >> self.out, u"Currently: {0} ({1}) {2}".format(temp_c, temp_f, data["weather"])
        else:
            print >> self.out, u"Currently: {0} ({1}) {2}".format(temp_f, temp_c, data["weather"])

        print >> self.out, "Wind: {0}".format(data['wind_string'])
        print >> self.out, "Humidity: {0}".format(data['relative_humidity'])

    def print_hourly(self, data):
        """
        Prints the hourly weather data in a table
        """
        # Need to generate an array to send the print_table, first row must be the keys
        val = []
        val.append(["Date", "Hour", "Temperature", "Chance of Rain", "Weather"])

        for item in data:
            time = format_hour(item["FCTTIME"], self.settings.time)
            date = format_date(item["FCTTIME"]["mon_abbrev"], item["FCTTIME"]["mday"])
            temp = format_degree(item["temp"], self.settings.units)
            val.append([date, time, temp, item["pop"] + "%", item['condition']])

        print >> self.out, "36 Hour Hourly Forecast:"
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
            date_str = format_date(date['monthname'], date['day'])
            temp = u"{0} / {1}".format(format_degree(item['high'], unit),
                                      format_degree(item['low'], unit))
            wind = format_windspeed(item['avewind'], unit)

            hum = str(item["avehumidity"]) + "%"
            val.append([date_str, item['conditions'], str(item["pop"]) + "%", temp, wind, hum])

        print >> self.out, "Weather Forecast:"
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

        print >> self.out, table[0][0].ljust(max_col_widths[0] + 1),
        for i in range(1, len(table[0])):
            col = table[0][i].rjust(max_col_widths[i] + 2)
            self.out.write(col)

        print >> self.out, ""
        print >> self.out, "-" * (sum(max_col_widths) + 3 * len(max_col_widths))

        table.pop(0)
        for row in table:
            print >> self.out, row[0].ljust(max_col_widths[0] + 1),
            for i in range(1, len(row)):
                col = row[i].rjust(max_col_widths[i] + 2)
                self.out.write(col)

            print >> self.out, ""

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

def format_date(month, day):
    """
    Returns a date string, 'April 2' for example
    """
    return FORMAT_STRINGS['date'].format(str(month), str(day))

def print_weather_data(data, args, settings):
    """
    Prints the supplied weather data as specified by the options and program arguments.
    """
    data = json.loads(data)

    if 'error' in data['response']:
        print data['response']['error']['description']
        return

    if 'results' in data['response']:
        print "More than 1 city matched your query, try being more specific"
        for result in data['response']['results']:
            print "{0}, {1} {2}".format(result['name'], result['state'], result['country_name'])
        return

    result_printer = ResultPrinter(settings=settings)
    if args.alerts:
        result_printer.print_alerts(data)
        print ""
    if args.now:
        result_printer.print_conditions(data['current_observation'])
        print ""
    if args.hourly:
        result_printer.print_hourly(data['hourly_forecast'])
        print ""
    if args.forecast or args.extended:
        result_printer.print_forecast(data['forecast']['simpleforecast']['forecastday'])
        print ""

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
    settings = Settings()
    base_url="http://api.wunderground.com/api/%s/" % settings.api_key

    # Create a location string, or use autoip
    query="q/%s.json"
    if args.location:
        query = query % "_".join(args.location);
    else:
        query = query % "autoip"

    return base_url + make_query_path(args) + query

def main(args):
    settings = Settings(args)
    api_url = make_api_url(args, settings)
    r = requests.get(api_url)
    print_weather_data(r.content, args, settings)

if __name__ == "__main__":
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
    parser.add_argument('-u', '--units', choices=Units.to_array(),
                        help='Set units to use (default is \'english\')')
    main(parser.parse_args())

