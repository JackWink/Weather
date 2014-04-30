#!/usr/bin/env python
import requests
import argparse
import sys
import json
import codecs

settings = {
    "api_key": "your-api-key",
    "metric": False
}

def get_max_col_width(table, column_index):
    """
    Returns the length of the longest string in any column
    """
    return max([len(row[column_index]) for row in table])

def print_table(out, table):
    """
    Aligns and prints an array into a formatted table

    Requires that the first row in the array contain the column names
    and that each row contains the same number of elements
    """
    max_col_widths = []
    for col in range(len(table[0])):
        max_col_widths.append(get_max_col_width(table, col))

    print >> out, table[0][0].ljust(max_col_widths[0] + 1),
    for i in range(1, len(table[0])):
        col = table[0][i].rjust(max_col_widths[i] + 2)
        out.write(col)


    print >> out, ""
    print >> out, "-" * (sum(max_col_widths) + 3 * len(max_col_widths))

    table.pop(0)
    for row in table:
        print >> out, row[0].ljust(max_col_widths[0] + 1),
        for i in range(1, len(row)):
            col = row[i].rjust(max_col_widths[i] + 2)
            out.write(col)

        print >> out


def print_alerts(data):
    """
    Prints any weather alerts in red
    """
    for alert in data['alerts']:
        print "\033[91m" + alert['message'].rstrip("\n") + "\nExpires: " + alert['expires'] + "\033[0m"


def print_conditions(data):
    """
    Prints the current weather conditions
    """
    print "Weather for " + data['display_location']['full']
    print "Currently: "  + data['temperature_string'] + " " + data['weather']
    print "Wind: "       + data['wind_string']
    print "Humidity: "   + data['relative_humidity']


def print_hourly(data, metric):
    """
    Prints the hourly weather data in a table
    """
    # Need to generate an array to send the print_table, first row must be the keys
    val = []
    val.append(["Date", "Hour", "Temperature", "Chance of Rain", "Weather"])

    for item in data:
        # Format the date and temp strings before appending to the array
        time = item["FCTTIME"]
        date = time["mon_abbrev"] + " " + time["mday_padded"] + ", " + time["year"]

        if settings['metric'] or metric:
            temp = item["temp"]["metric"] + u" \u00B0C"
        else:
            temp = item["temp"]["english"] + u" \u00B0F"
        val.append([date, time['civil'], temp,  item["pop"] + "%", item['condition']])

    print "\n36 Hour Hourly Forecast:"
    print_table(sys.stdout, val)


def print_forecast(data, metric):
    """
    Prints the 3 day forcast data in a table
    """
    # Need to generate an array to send the print_table, first row must be the keys
    val = []
    val.append(["Date", "Condition", "Chance of Rain", "Temp (Hi/Lo)", "Wind", "Humidity"])

    for item in data:
        date = item['date']
        date_str = date['monthname'] + " " + str(date['day']) + ", " + str(date['year'])

        if settings['metric'] or metric:
            temp = item['high']['celsius'] + u" \u00B0C / " + item['low']['celsius'] + u" \u00B0C"
            wind = "~" + str(item['avewind']['kph']) + "kph " + item['avewind']['dir']
        else:
            temp = item['high']['fahrenheit'] + u" \u00B0F / " + item['low']['fahrenheit'] + u" \u00B0F"
            wind = "~" + str(item['avewind']['mph']) + "mph " + item['avewind']['dir']

        hum = str(item["avehumidity"]) + "%"
        val.append([date_str, item['conditions'], str(item["pop"]) + "%", temp, wind, hum])

    print "\nWeather Forecast:"
    print_table(sys.stdout, val)


def print_weather_data(data, args):
    """
    Prints the supplied weather data as specified by the options and arguments.
    """
    data = json.loads(data)

    if 'error' in data['response']:
        print data['response']['error']['description']
        return

    if 'results' in data['response']:
        print "More than 1 city matched your query, try being more specific"
        for result in data['response']['results']:
            print result['name'] + ", " + result['state'] + " " + result['country_name']
        return

    if args.alerts:
        print_alerts(data)
    if args.now:
        print_conditions(data['current_observation'])
    if args.hourly:
        print_hourly(data['hourly_forecast'], args.metric)
    if args.forecast:
        print_forecast(data['forecast']['simpleforecast']['forecastday'], args.metric)



def make_query_path(args):
    """
    Returns a path to use against the weather underground API
    by parsing program arguments.
    """
    query = ""

    paths = {
        "now": "conditions/",
        "forecast": "forecast/",
        "hourly": "hourly/",
        "alerts": "alerts/",
    }

    # In the case no options are set, use the default
    if not (args.now or args.hourly or args.alerts or args.forecast):
        args.now = True
        args.alerts = True

    if (args.now):
        query += paths['now']
    if (args.hourly):
        query += paths['hourly']
    if (args.forecast):
        query += paths['forecast']
    if (args.alerts):
        query += paths['alerts']

    return query

def make_api_url(args):
    """
    Returns a url to the weather underground API endpoint by parsing
    program arguments.
    """
    base_url="http://api.wunderground.com/api/%s/" % settings['api_key']

    # Create a location string, or use autoip
    query="q/%s.json"
    if args.location:
        query = query % "_".join(args.location);
    else:
        query = query % "autoip"

    return base_url + make_query_path(args) + query


def main(args):
    api_url = make_api_url(args)
    r = requests.get(api_url)

    # Wrap sys.stdout in a utf8 stream writer in case output is piped
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    print_weather_data(r.content, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display the current weather, or forecast")
    parser.add_argument('location', nargs='*', help='Optional location, by default uses geoip')
    parser.add_argument('-n', '--now', help='Get the current conditions (Default)', action='store_true')
    parser.add_argument('-f', '--forecast', help='Get the current forecast', action='store_true')
    parser.add_argument('-o', '--hourly', help='Get the hourly forecast', action='store_true')
    parser.add_argument('-a', '--alerts', help='View any current weather alerts (Default)', action='store_true')

    if settings['metric']:
        parser.add_argument('-m', '--metric', help='Use metric units instead of English units (Default)', action='store_true')
    else:
        parser.add_argument('-m', '--metric', help='Use metric units instead of English units', action='store_true')

    main(parser.parse_args())

