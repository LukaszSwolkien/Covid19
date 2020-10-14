from datetime import date
from functools import wraps
from opentelemetry import trace
import locale


def to_date(d):
    year = to_num(d["year"])
    month = to_num(d["month"])
    day = to_num(d["day"])
    return date(day=day, month=month, year=year)


def week_number(d):
    return d.isocalendar()[1]


def trace_function(name, module_name=__name__):
    tracer = trace.get_tracer(module_name)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwds):
            with tracer.start_as_current_span(name) as root:
                try:
                    return func(*args, **kwds)
                except Exception as e:
                    print(root.get_context()) # SpanContext can help to link traces with 
                    raise e

        return wrapper

    return decorator


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
