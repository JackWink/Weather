import weather
import unittest
import sys

from weather_mock import MockArgs, MockIO

class TestPrinterFunctions(unittest.TestCase):
    def setUp(self):
        self.spy = MockIO()

    def tearDown(self):
        self.spy.clear()

    def test_initialization(self):
        printer = weather.ResultPrinter()

        # Ensure we've wrapped std.out
        # XXX need to look into better way of testing
        self.assertNotEqual(printer.out, sys.stdout)

        printer = weather.ResultPrinter(sys.stdout)
        self.assertEqual(printer.out, sys.stdout)

        default_settings = weather.Settings()
        self.assertEqual(default_settings.units, printer.settings.units)
        self.assertEqual(default_settings.api_key, printer.settings.api_key)

    def test_print_no_alerts(self):
        """
        Test to ensure we print a message when there are no alerts
        """
        printer = weather.ResultPrinter(self.spy)

        printer.print_alerts({'alerts': [], 'current_observation': {'display_location': { 'full': 'test'} } })

        self.assertEqual(len(self.spy.captured_out), 2)
        self.assertEqual(self.spy.captured_out[0], 'No alerts for test')
        self.assertEqual(self.spy.captured_out[1], '\n')

    def test_print_alerts(self):
        """
        Test to ensure we print the message, followed by a new line, then the expiration time
        """
        printer = weather.ResultPrinter(self.spy)
        printer.print_alerts({'alerts': [{'message': '1234', 'expires': 'never!' }]})

        self.assertEqual(len(self.spy.captured_out), 2)
        self.assertEqual(self.spy.captured_out[0], '\x1b[91m1234\nExpires: never!\x1b[0m')
        self.assertEqual(self.spy.captured_out[1], '\n')

    def test_print_conditions(self):
        printer = weather.ResultPrinter(self.spy)
        printer.print_conditions(self._gen_conditions_dict(metric_larger=False))
        self.assertEqual(len(self.spy.captured_out), 8)
        print self.spy.captured_out
        self.assertEqual(self.spy.captured_out[0], 'Weather for Ann Arbor')
        self.assertEqual(self.spy.captured_out[1], '\n')
        self.assertEqual(self.spy.captured_out[2], u'Currently: 45 \xb0F (44 \xb0C) Light showers')
        self.assertEqual(self.spy.captured_out[3], '\n')
        self.assertEqual(self.spy.captured_out[4], 'Wind: Calm')
        self.assertEqual(self.spy.captured_out[5], '\n')
        self.assertEqual(self.spy.captured_out[6], 'Humidity: 37')
        self.assertEqual(self.spy.captured_out[7], '\n')

        self.spy.clear()
        printer = weather.ResultPrinter(settings=weather.Settings(MockArgs(units="metric")), out=self.spy)
        printer.print_conditions(self._gen_conditions_dict(metric_larger=False))
        self.assertEqual(printer.settings.units, "metric")
        self.assertEqual(len(self.spy.captured_out), 8)
        self.assertEqual(self.spy.captured_out[0], 'Weather for Ann Arbor')
        self.assertEqual(self.spy.captured_out[1], '\n')
        self.assertEqual(self.spy.captured_out[2], u'Currently: 44 \xb0C (45 \xb0F) Light showers')
        self.assertEqual(self.spy.captured_out[3], '\n')
        self.assertEqual(self.spy.captured_out[4], 'Wind: Calm')
        self.assertEqual(self.spy.captured_out[5], '\n')
        self.assertEqual(self.spy.captured_out[6], 'Humidity: 37')
        self.assertEqual(self.spy.captured_out[7], '\n')


    def _gen_conditions_dict(self, city="Ann Arbor", weather="Light showers", temp=45,
                                   metric_larger=False, wind="Calm", humidity=37):
        """
        Generate a dictionary with the data for print_conditions

        C will be one less than F if metric_larger is True.
        """
        temp_key = "temp_f"
        other_temp_key = "temp_c"
        if metric_larger:
            temp_key = "temp_c"
            other_temp_key = "temp_f"

        return { 'display_location': {'full': city }, temp_key: temp, other_temp_key: temp-1,
                 'weather': weather, 'wind_string': wind, 'relative_humidity': humidity }

    def test_print_forecast(self):
        pass

    def test_print_hourly(self):
        pass

    def test_print_weather_data(self):
        pass





