"""
Mock objects used in the test program
"""
class MockIO(object):
    def __init__(self):
        self.captured_out = []

    def write(self, string):
        self.captured_out.append(string)

    def clear(self):
        self.captured_out = []

class MockArgs(object):
    def __init__(self, units=False, api_key="1234"):
        self.units = units
        self.api_key = api_key

    def __iter__(self):
        yield "api_key"
        yield "units"

