#!/usr/bin/env python
import requests, argparse, sys, json 

settings = {
    "api_key": "your-api-key"    
}


def get_max_width(table, i):
    return max([len(row[i]) for row in table])

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



def make_str(args, options):
    url = ""
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



def parse_alerts(data):
    for alert in range(len(data['alerts'])):
        print "\033[91m" + data['alerts'][alert] + "\033[0m"



def parse_conditions(data):
    print "Weather for " + data['display_location']['full']
    print "Currently: "  + data['temperature_string'] + " " + data['weather'] 
    print "Wind: "       + data['wind_string']  
    print "Humidity: "   + data['relative_humidity']



def parse_hourly(data):
    val = []
    val.append(["Date", "Hour", "Temp (F / C)", "Weather"])
    for item in data:
        time = item["FCTTIME"]
        date = time["mon_abbrev"] + " " + time["mday_padded"] + ", " + time["year"]
        temp = item["temp"]["english"] + " / " + item["temp"]["metric"]
        val.append([date, time['civil'], temp, item['condition']])
    print "\n36 Hour Hourly Forecast:"
    print_table(sys.stdout, val)

def parse_forecast(data):
    val = []
    val.append(["Date", "Condition", "Temp (Hi/Lo)", "Wind", "Humidity"])
    for item in data:
        date = item['date']
        date_str = date['monthname'] + " " + str(date['day']) + ", " + str(date['year'])
        temp = item['high']['fahrenheit'] + "F (" + item['high']['celsius'] + "C) / " + item['low']['fahrenheit'] + "F (" + item['low']['celsius'] + "C)"
        wind = "~" + str(item['avewind']['mph']) + "mph (" + str(item['avewind']['kph']) + "kph) " + item['avewind']['dir'] 
        hum = str(item["avehumidity"]) + "%"
        val.append([date_str, item['conditions'], temp, wind, hum])
    print "\nWeather Forecast:"
    print_table(sys.stdout, val)


def parse_weather_data(data, args):
    data = json.loads(data)
    
    if 'error' in data['response']:
        print data['response']['error']['description']
        return
    
    if 'results' in data['response']:
        print "More than 1 city matched your query."
        for result in data['response']['results']:
            print result['name'] + ", " + result['state'] + " " + result['country_name']
        return

    if args.alerts:
        parse_alerts(data)
    if args.now:
        parse_conditions(data['current_observation'])
    if args.hourly:
        parse_hourly(data['hourly_forecast'])
    if args.forecast:
        parse_forecast(data['forecast']['simpleforecast']['forecastday'])


def main(args):
    # api/KEY/FEATURE/[FEATURE].../q/QUERY.FORMAT
    base_url="http://api.wunderground.com/api/%s/" % settings['api_key']
    query="q/%s.json"

    options = {
        "now": "conditions/",
        "forecast": "forecast/",
        "hourly": "hourly/",
        "alerts": "alerts/",
        "ip": "autoip"
    }
     
    if args.location:
        query = query % "_".join(args.location);
    else:
        query = query % options['ip']
    
    url = base_url + make_str(args, options) + query
    r = requests.get(url)

    parse_weather_data(r.content, args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display the current weather, or forecast")
    parser.add_argument('location', nargs='*', help='Optional location, by default uses geoip')
    parser.add_argument('-n', '--now', help='Get the current conditions (Default)', action='store_true')
    parser.add_argument('-f', '--forecast', help='Get the current forecast', action='store_true')
    parser.add_argument('-o', '--hourly', help='Get the hourly forecast', action='store_true')
    parser.add_argument('-a', '--alerts', help='View any current weather alerts (Default)', action='store_true')
    
    main(parser.parse_args())

