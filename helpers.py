from datetime import date
import locale


def to_date(d):
    year = d['year']
    month = d['month']
    day = d['day']
    return date(day=day, month=month, year=year)


def week_number(d):
    return d.isocalendar()[1]


def is_int(s):
    try:
        if isinstance(s, str):
            num = to_num(s)
            if isinstance(num, float):
                return num.is_integer()
            return isinstance(num, int)
        elif isinstance(s, int):
            int(s)
            return True
        else:
            return False
    except ValueError:
        return False


def is_num(s):
    try:
        locale.atoi(str(s))
    except ValueError:
        try:
            locale.atof(str(s))
        except ValueError:
            return False
    return True


def to_num(s):
    try:
        return locale.atoi(str(s))
    except ValueError:
        return locale.atof(str(s))


def to_str(value):
    try:
        strval = u"".join(value)
    except TypeError:
        strval = str(value, errors="ignore")
    return strval
