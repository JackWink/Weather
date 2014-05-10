#Weather

Weather is a small command line python script to grab the current weather and/or weather forcast from weather underground and display it nicely in the terminal.

##Usage Options

- `-n`, `--now`  Gives the current weather conditions 
- `-o`, `--hourly`  Gives an overview of the hourly forcast for the next 36 hours 
- `-f`, `--forecast`  Gives an overview of the daily forecast 
- `-m`, `--metric` Uses metric units instead of English 
- `-h`, `--help`  Prints out a help message
- `location`  The only argument without a flag, you can look up via zipcode or XX/CITY where XX is the state initial.  By default, it uses geoip to get your location

##Dependencies

- Requests
- Weather Underground API key 

##Requirements
If you don't have requests installed, install it! `pip install -r requirements.txt` or `pip install requests` 

You need to sign up for an API key from weather underground `http://www.wunderground.com/weather/api/`.  You'll want the Cumulus feature plan, as long as you select the developer usage plan, it's free.  

##Configuring

Run weather.py to generate a `.weatherrc` file, which by default installs into your home directory.  You may change it's install location by editing `WEATHER_CONF_FILE` in `weather.py`

Edit your `~/.weatherrc` file to include your API key.  If you like metric units by default, set `metric` to true. A sample `.weatherrc` file is provided below.

	{
		"api_key": "your-api-key",
		"metric": false
	}
	

##Installing

Run `chmod +x weather.py` to ensure it's set to execute.  Move `weather.py` to into a directory in your `$PATH` variable (`/usr/bin` or `/usr/local/bin` typically). Optionally rename it to `weather`.   

##Output

Sample output:

	jackwink: weather (master) $ weather -o
	36 Hour Hourly Forecast:
	Date               Hour  Temperature  Chance of Rain         Weather
	--------------------------------------------------------------------------
	May 02, 2014   11:00 PM        48 °F             60%  Chance of Rain
	May 03, 2014   12:00 AM        48 °F             60%  Chance of Rain
	May 03, 2014    1:00 AM        48 °F             60%  Chance of Rain
	May 03, 2014    2:00 AM        48 °F             60%  Chance of Rain
	May 03, 2014    3:00 AM        47 °F             60%  Chance of Rain
	May 03, 2014    4:00 AM        47 °F             60%  Chance of Rain
	May 03, 2014    5:00 AM        46 °F             60%    Rain Showers
	May 03, 2014    6:00 AM        47 °F             60%    Rain Showers
	May 03, 2014    7:00 AM        49 °F             60%    Rain Showers
	May 03, 2014    8:00 AM        50 °F             60%  Chance of Rain
	May 03, 2014    9:00 AM        52 °F             60%  Chance of Rain
	May 03, 2014   10:00 AM        53 °F             60%  Chance of Rain
	...
	jackwink: weather (master) $ weather -f
	Weather Forecast:
	Date               Condition  Chance of Rain   Temp (Hi/Lo)         Wind  Humidity
	-----------------------------------------------------------------------------------------
	May 2, 2014     Rain Showers             30%  61 °F / 45 °F   ~13mph WSW       76%
	May 3, 2014     Rain Showers             50%  63 °F / 41 °F   ~15mph WSW       66%
	May 4, 2014    Partly Cloudy             10%  57 °F / 36 °F    ~15mph NW       61%
	May 5, 2014   Chance of Rain             20%  59 °F / 36 °F  ~6mph South       63%
	jackwink: weather (master) $ weather
	Weather for Ann Arbor, MI
	Currently: 49.2 F (9.6 C) Rain
	Wind: From the SSW at 8.0 MPH Gusting to 11.0 MPH
	Humidity: 88%
