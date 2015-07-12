
class Units(object):
    METRIC = "metric"
    ENGLISH = "english"

    @staticmethod
    def to_array():
        return [Units.METRIC, Units.ENGLISH]


class TimeFormats(object):
    MILITARY = "military"
    CIVILIAN = "civilian"

    @staticmethod
    def to_array():
        return [TimeFormats.MILITARY, TimeFormats.CIVILIAN]


class Direction(object):
    @staticmethod
    def shorthand(direction):
        normalized = direction.lower()
        if normalized == "east":
            return "E"
        if normalized == "west":
            return "W"
        if normalized == "south":
            return "S"
        if normalized == "north":
            return "N"
        return direction

class DateFormats(object):
    DATE  = "date"
    DAY   = "weekday"

    @staticmethod
    def to_array():
        return [DateFormats.DATE, DateFormats.DAY]
