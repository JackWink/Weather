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
