from dateutil import tz
from dateutil.parser import parse


def parse_date(date):
    tzinfos = {
        "GMT": tz.gettz("GMT"),
        "PDT": tz.gettz("America/Los_Angeles"),
        "PST": tz.gettz("America/Los_Angeles"),
        "EDT": tz.gettz("America/New_York"),
        "EST": tz.gettz("America/New_York"),
    }
    date = parse(date, tzinfos=tzinfos)
    date = date.astimezone(tz.UTC).isoformat()
    if date.endswith('+00:00'):
        date = date.replace('+00:00', 'Z')
    return date
