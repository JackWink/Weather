#Weather 

[![Build Status](https://travis-ci.org/JackWink/Weather.svg?branch=master)](https://travis-ci.org/JackWink/Weather)

Weather is a small command line python script to grab the current weather and/or weather forcast from weather underground and display it nicely in the terminal.

##Usage

Commands can be run by themselves, or stacked.

Sample Usage:

	jackwink: weather (master) $ chmod +x ./weather.py
	jackwink: weather (master) $ vim ~/.weatherrc
	jackwink: weather (master) $ ./weather.py
	Weather for Ann Arbor, MI
	Currently: 61.3°F (16.3°C) Clear
	Wind: Calm
	Humidity: 59%

	jackwink: weather (master) $ ./weather.py -anf
	No alerts for Ann Arbor, MI

	Weather for Ann Arbor, MI
	Currently: 61.3°F (16.3°C) Clear
	Wind: Calm
	Humidity: 59%

	Weather Forecast:
	Date                          Condition  Chance of Rain   Temp (Hi/Lo)        Wind  Humidity
	---------------------------------------------------------------------------------------------------
	May 9                     Partly Cloudy             20%  79 °F / 53 °F  ~0mph            82%
	May 10                    Partly Cloudy              0%  70 °F / 47 °F  ~14mph W         57%
	May 11         Chance of a Thunderstorm             40%  76 °F / 60 °F  ~11mph SSE       83%
	May 12         Chance of a Thunderstorm             60%  81 °F / 64 °F  ~16mph SSW       85%
	
	jackwink: weather (master) $ 

##Usage Options

- `-n`, `--now`  Gives the current weather conditions 
- `-o`, `--hourly`  Gives an overview of the hourly forcast for the next 36 hours 
- `-f`, `--forecast`  Gives an overview of the daily forecast 
- `-e`, `--extended`  Gives an overview of the extended forecast 
- `-t`, `--time`  {civil, military}  Set time format
- `-m`, `--metric` Uses metric units instead of English 
- `-a`, `--alert` View any current weather alerts
- `-h`, `--help`  Prints out a help message
- `location`  The only argument without a flag, you can look up via zipcode or XX/CITY where XX is the state initial.  By default, it uses geoip to get your location

##Dependencies

- Requests
- Weather Underground API key 

If you don't have requests installed, install it! `pip install -r requirements.txt` or `pip install requests` 

You'll need to sign up for an API key from weather underground `http://www.wunderground.com/weather/api/`.  You'll want the Cumulus feature plan and as long as you select the developer usage plan, it's free.  

##Configuring

Run weather.py to generate a `.weatherrc` file, which by default installs into your home directory.  You may change it's install location by editing `WEATHER_CONF_FILE` in `weather.py`

Edit your `~/.weatherrc` file to include your API key.  If you like metric units by default, set `metric` to true. A sample `.weatherrc` file is provided below.

	{
		"api_key": "your-api-key",
		"metric": false
	}
	

##Installing

Run `chmod +x weather.py` to ensure it's set to execute.  Move `weather.py` to into a directory in your `$PATH` variable (`/usr/bin` or `/usr/local/bin` typically). Optionally rename it to `weather`.   

##Testing

Install the requirements.txt file, you'll need coverage and nose. If you're using windows or linux, edit the Makefile and uncomment the line relative to your OS.  

Run `make test` to run the unit tests, and `make` if you want to run the unit tests and generate a coverage report.

