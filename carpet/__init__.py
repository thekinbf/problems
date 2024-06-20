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
    check50.run("Rscript carpet.R 2024").stdout("10.24 million visitors")


@check50.check(readline)
def thirty_four():
    """carpet.R correctly predicts 2034 visitors"""
    check50.run("Rscript carpet.R 2034").stdout("12.14 million visitors")


@check50.check(readline)
def fourteen():
    """carpet.R correctly predicts 2014 visitors"""
    check50.run("Rscript carpet.R 2014").stdout("8.34 million visitors")


def replace_readline(contents: list[str]) -> list[str]:
    """Prepares an interactive R script to be run with command line arguments"""
    modified_contents = []
    readline_count = 0

    for line in contents:
        if "readline" in line:
            readline_count += 1
            line = re.sub(
                r"readline\([^\)]*\)",
                f"commandArgs(trailingOnly = TRUE)[{readline_count}]",
                line,
            )
        modified_contents.append(line)

    return modified_contents