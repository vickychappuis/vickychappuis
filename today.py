"""Recalculates the Uptime line in both profile SVGs. Runs daily via GitHub Actions."""
import datetime
import re

from dateutil import relativedelta

BIRTHDAY = datetime.datetime(2003, 12, 10)
LINE_WIDTH = 56  # visible chars per ficha line: ". Uptime: <dots> <value>"


def plural(n):
    return "" if n == 1 else "s"


def uptime():
    d = relativedelta.relativedelta(datetime.datetime.today(), BIRTHDAY)
    cake = " 🎂" if (d.months == 0 and d.days == 0) else ""
    return (
        f"{d.years} year{plural(d.years)}, "
        f"{d.months} month{plural(d.months)}, "
        f"{d.days} day{plural(d.days)}{cake}"
    )


def update(path, value):
    svg = open(path, encoding="utf-8").read()
    dots = "." * (LINE_WIDTH - 5 - len("Uptime") - len(value))
    svg = re.sub(r'(<tspan id="uptime_dots"[^>]*>)[^<]*(</tspan>)', rf"\g<1>{dots}\g<2>", svg)
    svg = re.sub(r'(<tspan id="uptime_data"[^>]*>)[^<]*(</tspan>)', rf"\g<1>{value}\g<2>", svg)
    open(path, "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    value = uptime()
    for f in ("dark_mode.svg", "light_mode.svg"):
        update(f, value)
    print(f"Uptime: {value}")
