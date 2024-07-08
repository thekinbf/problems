import check50
import re


@check50.check()
def exists():
    """ontime.R exists"""
    check50.exists("ontime.R")
    check50.include("bus.csv")
    check50.include("rail.csv")


@check50.check(exists)
def readline():
    "ontime.R uses readline"
    with open("ontime.R", "r") as f:
        contents = f.readlines()

    new_contents = replace_readline(contents)
    if new_contents == contents:
        raise check50.Failure(f"Could not find readline in ontime.R")

    with open("ontime.R", "w") as f:
        f.writelines(new_contents)

    out = check50.run(f"Rscript ontime.R Red").stdout()
    status = check50.run(f"Rscript ontime.R Red").exit()
    if status != 0 and "unexpected" in out:
        raise check50.Failure("Could not find your use of readline. Ensure it's on a single line without stray spaces.")


@check50.check(readline)
def red_line():
    """ontime.R outputs correct predictions for the Red Line"""
    check_route("Red", peak_percent="89%", offpeak_percent="89%")


@check50.check(readline)
def green_line():
    """ontime.R outputs correct predictions for the Green Line (D)"""
    check_route("Green-D", peak_percent="75%", offpeak_percent="76%")


@check50.check(readline)
def bus_1():
    """ontime.R outputs correct predictions for the 1 Bus"""
    check_route("1", peak_percent="73%", offpeak_percent="74%")


@check50.check(readline)
def bus_86():
    """ontime.R outputs correct predictions for the 86 Bus"""
    check_route("86", peak_percent="72%", offpeak_percent="65%")


def check_route(route: str, peak_percent: str, offpeak_percent: str) -> None:
    status = check50.run(f"Rscript ontime.R {route}").exit()
    out = check50.run(f"Rscript ontime.R {route}").stdout()

    if status != 0:
        if match := re.search(r"cannot open file '(?P<filename>[^']+)'", out):
            raise check50.Failure(
                f'ontime.R could not open "{match.group("filename")}"',
                help='Be sure to provide a relative path, such as "rail.csv" or "bus.csv"',
            )
        raise check50.Failure(out)

    if not (peak_percent in out and offpeak_percent in out):
        raise check50.Mismatch(
            expected=f"On time {peak_percent} of the time during peak hours.\nOn time {offpeak_percent} of the time during off-peak hours.",
            actual=out,
        )


def replace_readline(contents: list[str]) -> list[str]:
    """Prepares an interactive R script to be run with command line arguments"""
    modified_contents = []
    readline_count = 0

    for line in contents:
        if "readline" in line:
            readline_count += 1

            if not re.search(r"readline\([\S\s]*(?:(?<!\))\))", line):
                raise check50.Failure(
                    "Could not find your use of readline. Ensure it's on a single line without stray spaces."
                )

            line = re.sub(
                r"readline\([\S\s]*(?:(?<!\))\))",
                f"commandArgs(trailingOnly = TRUE)[{readline_count}]",
                line,
            )

        modified_contents.append(line)

    return modified_contents
