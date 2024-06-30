import check50
import re


@check50.check()
def exists():
    """happy.R exists"""
    check50.exists("happy.R")
    for year in [2020, 2021, 2022, 2023, 2024]:
        check50.include(f"{year}.csv")


@check50.check(exists)
def readline():
    """happy.R uses readline"""
    with open("happy.R", "r") as f:
        contents = f.readlines()

    new_contents = replace_readline(contents)
    if new_contents == contents:
        raise check50.Failure(f"Could not find readline in happy.R")

    with open("happy.R", "w") as f:
        f.writelines(new_contents)


@check50.check(readline)
def united_states():
    """happy.R outputs correct data for United States"""
    check_country(
        country="United States",
        expected_scores={
            "2020": "6.94",
            "2021": "6.95",
            "2022": "6.98",
            "2023": "6.89",
            "2024": "6.72",
        },
    )


@check50.check(readline)
def nepal():
    """happy.R outputs correct data for Nepal"""
    check_country(
        country="Nepal",
        expected_scores={
            "2020": "5.14",
            "2021": "5.27",
            "2022": "5.38",
            "2023": "5.36",
            "2024": "5.16",
        },
    )


@check50.check(readline)
def finland():
    """happy.R outputs correct data for Finland"""
    check_country(
        country="Finland",
        expected_scores={
            "2020": "7.81",
            "2021": "7.84",
            "2022": "7.82",
            "2023": "7.8",
            "2024": "7.74",
        },
    )


@check50.check(readline)
def south_africa():
    """happy.R outputs correct data for South Africa"""
    check_country(
        country="South Africa",
        expected_scores={
            "2020": "4.81",
            "2021": "4.96",
            "2022": "5.19",
            "2023": "5.28",
            "2024": "5.42",
        },
    )


@check50.check(readline)
def new_zealand():
    """happy.R outputs correct data for New Zealand"""
    check_country(
        country="New Zealand",
        expected_scores={
            "2020": "7.3",
            "2021": "7.28",
            "2022": "7.2",
            "2023": "7.12",
            "2024": "7.03",
        },
    )


@check50.check(readline)
def bhutan():
    """happy.R outputs correct data for Bhutan"""
    check_country(
        country="Bhutan",
        expected_scores={
            "2020": "unavailable",
            "2021": "unavailable",
            "2022": "unavailable",
            "2023": "unavailable",
            "2024": "unavailable",
        },
    )


def check_country(country: str, expected_scores: dict[str]) -> None:
    status = check50.run(f"Rscript happy.R '{country}'").exit()
    out = check50.run(f"Rscript happy.R '{country}'").stdout().lower()

    if status != 0:
        if match := re.search(r"cannot open file '(?P<filename>[^']+)'", out):
            raise check50.Failure(
                f'happy.R could not open "{match.group("filename")}"',
                help='Be sure to provide a relative path, such as "2020.csv"',
            )
        raise check50.Failure(out)

    for year, score in expected_scores.items():
        if not (year in out and score in out):
            raise check50.Failure(
                f"Expected to find score of {score} in {year} for {country}"
            )


def replace_readline(contents: list[str]) -> list[str]:
    """Prepares an interactive R script to be run with command line arguments"""
    modified_contents = []
    readline_count = 0

    for line in contents:
        if "readline" in line:
            readline_count += 1
            line = re.sub(
                r"readline\([^\v]*\)",
                f"commandArgs(trailingOnly = TRUE)[{readline_count}]",
                line,
            )
        modified_contents.append(line)

    return modified_contents
