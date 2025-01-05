import datetime


def parse_date(date_string: str) -> str:
    date = datetime.datetime.strptime(date_string, "%m/%d")
    date = date.replace(year=datetime.datetime.now().year)
    return f"{date.year}-{date.month:02}-{date.day:02}"
