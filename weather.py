#!/usr/bin/env python
import requests, argparse, sys, json 

settings = {
    "api_key": "your-api-key",   
    "metric": False 
}

## get_max_width
#
#  Returns the max width of any row in an array
def get_max_width(table, i):
    return max([len(row[i]) for row in table])

## print_table
#
#  Aligns and prints an array into a table, given that the first 
#  row in the array contains the column names
def print_table(out, table):
    col_paddings = []
    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))
   
    print >> out, table[0][0].ljust(col_paddings[0] + 1),
    for i in range(1, len(table[0])):
        col = table[0][i].rjust(col_paddings[i] + 2)
        print >> out, col,
    

    print >> out, "" 
    print >> out, "-" * (sum(col_paddings) + 3 * len(col_paddings))

    table.pop(0)
    for row in table:
        print >> out, row[0].ljust(col_paddings[0] + 1),
        for i in range(1, len(row)):
            col = row[i].rjust(col_paddings[i] + 2)
            print >> out, col,
        
        print >> out


## Make_str
#
#  Takes the options and arguments and assembles the query string
def make_str(args, options):
    url = ""

    # In the case no options are set, use the default
    if not (args.now or args.hourly or args.alerts or args.forecast):
        args.now = True
        args.alerts = True

    if (args.now):
        url += options['now']
    if (args.hourly):
        url += options['hourly']
    if (args.forecast):
        url += options['forecast']
    if (args.alerts):
        url += options['alerts']
    
    return url


## parse_alerts
#
#  Takes the returned data and parses the alert messages
def parse_alerts(data):
    for alert in data['alerts']:
        print "\033[91m" + alert['message'].rstrip("\n") + "\nExpires: " + alert['expires'] + "\033[0m"


## parse_conditions
#
#  Parses the current conditions from the API
def parse_conditions(data):
    print "Weather for " + data['display_location']['full']
    print "Currently: "  + data['temperature_string'] + " " + data['weather'] 
    print "Wind: "       + data['wind_string']  
    print "Humidity: "   + data['relative_humidity']


## parse_hourly
#
#  Parses the hourly condition data from the API
def parse_hourly(data, metric):
    # Need to generate an array to send the print_table, first row must be the keys
    val = []
    val.append(["Date", "Hour", "Temperature", "Weather"])
    
    for item in data:
        # Format the date and temp strings before appending to the array
        time = item["FCTTIME"]
        date = time["mon_abbrev"] + " " + time["mday_padded"] + ", " + time["year"]
        
        if settings['metric'] or metric:
            temp = item["temp"]["metric"] + u" \u00B0C"
        else:
            temp = item["temp"]["english"] + u" \u00B0F"
        val.append([date, time['civil'], temp, item['condition']])
    
    print "\n36 Hour Hourly Forecast:"
    print_table(sys.stdout, val)


## parse_forecast
#
#  Parses the forecast data from the API
def parse_forecast(data, metric):
    # Need to generate an array to send the print_table, first row must be the keys
    val = []
    val.append(["Date", "Condition", "Temp (Hi/Lo)", "Wind", "Humidity"])
    
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
        val.append([date_str, item['conditions'], temp, wind, hum])
    
    print "\nWeather Forecast:"
    print_table(sys.stdout, val)


## parse_weather_data
#
#  Parses the returned API data along with the options for proper formatting
def parse_weather_data(data, args):
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
        parse_alerts(data)
    if args.now:
        parse_conditions(data['current_observation'])
    if args.hourly:
        parse_hourly(data['hourly_forecast'], args.metric)
    if args.forecast:
        parse_forecast(data['forecast']['simpleforecast']['forecastday'], args.metric)


def main(args):
    # API methods 
    values = {
        "now": "conditions/",
        "forecast": "forecast/",
        "hourly": "hourly/",
        "alerts": "alerts/",
        "ip": "autoip"
    }
    
    # Create a location string, or use geoip
    query="q/%s.json"
    if args.location:
        query = query % "_".join(args.location);
    else:
        query = query % values['ip']
    
    base_url="http://api.wunderground.com/api/%s/" % settings['api_key']
    url = base_url + make_str(args, values) + query
    
    # Make the API request, parse the data
    r = requests.get(url)
    parse_weather_data(r.content, args)


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

