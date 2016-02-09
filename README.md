#Weatherpy

[![Build Status](https://travis-ci.org/JackWink/Weather.svg?branch=master)](https://travis-ci.org/JackWink/Weather)

Weatherpy is a small command line python script to grab the current weather and/or weather forcast from weather underground and display it nicely in the terminal.

##Usage

Commands can be run by themselves, or stacked.

Sample Usage:

    jackwink: weather (master) $ sudo python setup.py install 
    jackwink: weather (master) $ vim ~/.weatherrc
    jackwink: weather (master) $ weatherpy
    Weather for Ann Arbor, MI
    Currently: 61.3°F (16.3°C) Clear
    Wind: Calm
    Humidity: 59%

    jackwink: weather (master) $ weatherpy -anf
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
- `-a`, `--alert` View any current weather alerts
- `-t`, `--time`  {civilian, military} Set time format (defaults to civilian)
- `-d`, `--date`  {date, weekday} Set date format (defaults to date)
- `-u`, `--units` {english, metric} Set the units to use (defaults to english)
- `-h`, `--help`  Prints out a help message
- `location`  The only argument without a flag, you can look up via zipcode or XX/CITY where XX is the state initial

By default, weatherpy uses geoip to get your location, so you don't need to provide one

##Dependencies

- Weather Underground API key 

You'll need to sign up for an API key from weather underground `http://www.wunderground.com/weather/api/`.  
You'll want the Cumulus feature plan and as long as you select the developer usage plan, it's free.  

##Configuring

Run weatherpy to generate a `.weatherrc` file, which by default installs into your home directory. 
You may change the install location by editing `WEATHER_CONF_FILE` in `weatherpy/__init__.py`

Edit your `~/.weatherrc` file to include your API key.  If you want metric units by default, 
set `units` to 'metric'. A sample `.weatherrc` file is provided below.

    {
        "api_key": "your-api-key",
        "units": "english",
        "time": "military",
        "date": "weekday"
    }
	

##Installing

Run `sudo python setup.py install`   

##Testing

If you're using windows or linux, edit the Makefile and uncomment the line relative to your OS. 
You'll need nose and coverage installed.

Run `make test` to run the unit tests, and `make coverage` if you want to run the unit tests 
and generate a coverage report.

