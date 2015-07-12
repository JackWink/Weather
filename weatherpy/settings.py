import os
import json
from copy import deepcopy
from .types import Units, TimeFormats, DateFormats

WEATHER_CONF_FILE = "~/.weatherrc"


class Settings(object):
    """
    Contains the settings held in the WEATHER_CONF_FILE.
    """
    _DUMMY_API_KEY = 'your-api-key'

    # Cache of the class level settings
    _settings = {
        'api_key': _DUMMY_API_KEY,
        'units': Units.ENGLISH,
        'time': TimeFormats.CIVILIAN,
        'date': DateFormats.DATE
    }

    def __init__(self, args=None):
        self.file_path = os.path.expanduser(WEATHER_CONF_FILE)
        self.settings = deepcopy(self._settings)

        # Load (and create if needed) the weatherrc file
        if not os.path.exists(self.file_path):
            self.generate_default_weatherrc()
        else:
            with open(self.file_path) as weatherrc:
                saved_settings = json.load(weatherrc)
                for key in saved_settings:
                    self._override(key, saved_settings)

        if args is not None:
            self._override("units", args)
            self._override("time", args)
            self._override("date", args)

    def _override(self, key, args):
        """
        Updates the cached settings with the provided argument. Defaults to
        the previous value if the key isn't found in the arguments object

        :param key: Settings key to override, ex: 'time', 'units'
        :param args: argument object provided to settings init function
        """
        try:
            if key in args and args[key] is not None:
                self.settings[key] = args[key]
        except TypeError:
            if getattr(args, key, self.settings[key]) is not None:
                self.settings[key] = getattr(args, key, self.settings[key])


    def generate_default_weatherrc(self):
        """
        Writes a default weather conf file
        """
        with open(self.file_path, "w") as weatherrc:
            weatherrc.write(json.dumps(self.settings, sort_keys=True,
                                       indent=4, separators=(',', ': ')))

    def __getattr__(self, attr):
        """
        Proxy attribute requests to the settings cache
        """
        return self.settings[attr]
