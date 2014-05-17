import unittest
import weather
import os
import shutil
import json
from weather_mock import MockArgs

class TestSettingsFunctions(unittest.TestCase):
    def setUp(self):
        self.conf_path = os.path.expanduser(weather.WEATHER_CONF_FILE)
        if os.path.exists(self.conf_path):
            self._backup_settings(self.conf_path)

        #XXX - Need to reset internal settings so it'll reparse the conf file
        if weather.Settings.settings:
            weather.Settings.settings = None


    def tearDown(self):
        backupPath= os.path.expanduser("~/.weatherrc_backup")
        if os.path.exists(backupPath):
            self._restore_settings(self.conf_path)


    def _backup_settings(self, path):
        backup = os.path.expanduser("~/.weatherrc_backup")
        shutil.copy(path, backup)
        os.remove(path)

    def _restore_settings(self, path):
        backup = os.path.expanduser("~/.weatherrc_backup")
        shutil.copy(backup, path)
        os.remove(backup)

    def _write_conf(self, api_key, metric_str):
        with open(self.conf_path, 'w') as f:
            f.write('{ "api_key": "%s", "metric": %s }' % (api_key, metric_str))


    def test_default_file_creation(self):
        """
        Test that the default conf file is a valid JSON file that contains both
        the metric and API key value pair.
        """
        self.assertFalse(os.path.exists(self.conf_path))
        s = weather.Settings()
        self.assertTrue(os.path.exists(self.conf_path))
        data = {}
        with open(self.conf_path) as f:
            data = json.load(f)

        self.assertFalse(data["metric"])
        self.assertEqual(data["api_key"], "your-api-key")

    def test_file_loading(self):
        """
        Test that the loading Settings overrides the default conf file
        """
        self._write_conf("12341234", "true")
        s = weather.Settings()
        self.assertTrue(s.metric)
        self.assertEqual(s.api_key, "12341234")

        self._write_conf("1234", "false")
        #XXX reset conf file
        weather.Settings.settings = None
        s = weather.Settings()
        self.assertFalse(s.metric)
        self.assertEqual(s.api_key, "1234")

    def test_argument_override(self):
        """
        Test to ensure that arguments can override metric, but not API key setting
        """
        self._write_conf("12341234", "true")
        s = weather.Settings()
        self.assertTrue(s.metric)
        s = weather.Settings(MockArgs())
        self.assertFalse(s.metric)
        self.assertEqual(s.api_key, "12341234")



if __name__ == "__main__":
    unittest.main()
