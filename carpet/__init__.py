import check50
import re


@check50.check()
def exists():
    """carpet.R exists"""
    check50.exists("carpet.R")
    check50.include("visitors.csv")


@check50.check(exists)
def readline():
    """carpet.R uses readline"""
    with open("carpet.R", "r") as f:
        contents = f.readlines()

    new_contents = replace_readline(contents)
    if new_contents == contents:
        raise check50.Failure(f"Could not find readline in carpet.R")

    with open("carpet.R", "w") as f:
        f.writelines(new_contents)


@check50.check(readline)
def twenty_four():
    """carpet.R correctly predicts 2024 visitors"""
    check_prediction("2024", "10.24 million visitors")


@check50.check(readline)
def thirty_four():
    """carpet.R correctly predicts 2034 visitors"""
    check_prediction("2034", "12.14 million visitors")


@check50.check(readline)
def fourteen():
    """carpet.R correctly predicts 2014 visitors"""
    check_prediction("2014", "8.34 million visitors")


def check_prediction(year: str, output: str) -> None:
    status = check50.run(f"Rscript carpet.R {year}").exit()
    out = check50.run(f"Rscript carpet.R {year}").stdout()

    if status != 0:
        if match := re.search(r"cannot open file '(?P<filename>[^']+)'", out):
            raise check50.Failure(
                f'carpet.R could not open "{match.group("filename")}"',
                help='Be sure to provide a relative path, such as "visitors.csv"',
            )
        raise check50.Failure(out)

    if output not in out:
        raise check50.Failure(f'Could not find "{output}" in carpet.R\'s output')


def replace_readline(contents: list[str]) -> list[str]:
    """Prepares an interactive R script to be run with command line arguments"""
    modified_contents = []
    readline_count = 0

    for line in contents:
        if match := re.search("readline", line):
            readline_count += 1

            start = match.start()
            open_paren = 0
            close_paren = 0
            for i in range(start, len(line)):
                if line[i] == "(":
                    open_paren += 1
                elif line[i] == ")":
                    close_paren += 1
                
                if open_paren > 0 and open_paren == close_paren:
                    end = i
                    break
            
            line = line[:start] + f"commandArgs(trailingOnly = TRUE)[{readline_count}]" + line[end + 1:]

        modified_contents.append(line)

    return modified_contents
