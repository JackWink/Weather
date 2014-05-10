import unittest
import weather
import os
import shutil
import json

class TestSettingsFunctions(unittest.TestCase):
    def setUp(self):
        self.conf_path = os.path.expanduser(weather.WEATHER_CONF_FILE)
        if os.path.exists(self.conf_path):
            self._backup_settings(self.conf_path)

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

    def test_default_file_creation(self):
        self.assertFalse(os.path.exists(self.conf_path))
        s = weather.Settings()
        self.assertTrue(os.path.exists(self.conf_path))
        data = {}
        with open(self.conf_path) as f:
            data = json.load(f)

        self.assertFalse(data["metric"])
        self.assertEqual(data["api_key"], "your-api-key")


if __name__ == "__main__":
    unittest.main()
