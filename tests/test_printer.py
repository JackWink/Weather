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
        self.assertEqual(default_settings.metric, printer.settings.metric)
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
        pass

    def test_print_forecast(self):
        pass

    def test_print_hourly(self):
        pass

    def test_print_weather_data(self):
        pass





