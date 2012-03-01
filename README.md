#Weather

Weather is a small command line python script to grab the current weather and/or weather forcast and display it.

##Usage Options

- `-n`, `--now`  Gives the current weather conditions 
- `-o`, `--hourly`  Gives an overview of the hourly forcast for the next 36 hours 
- `-f`, `--forecast`  Gives an overview of the daily forecast 
- `-h`, `--help`  Prints out a help message
- `location`  The only argument without a flag, you can look up via zipcode or XX/CITY where XX is the state initial.  By default, it uses geoip to get your location

##Dependencies

- Requests
- Weather Underground API key 

##Installation

If you don't have requests installed, install it! `pip install requests`

You need to sign up for an API key from weather underground `http://www.wunderground.com/weather/api/`.  You'll want the Cumulus feature plan, as long as you select the developer usage plan, it's free.  Edit weather.py to include your API key in the settings dictionary.

Move `weather.py` to `/usr/local/bin/` or `/usr/bin/` and rename it weather.  Make sure you set `chmod +x weather` for it to execute.
