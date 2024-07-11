import check50
import glob
import re


@check50.check()
def exists():
    """teahouse.R exists"""
    check50.exists("teahouse.R")


@check50.check(exists)
def readline():
    """teahouse.R uses readline"""
    with open("teahouse.R", "r") as f:
        contents = f.readlines()

    new_contents = replace_readline(contents)
    if new_contents == contents:
        raise check50.Failure(f"Could not find readline in teahouse.R")

    with open("teahouse.R", "w") as f:
        f.writelines(new_contents)

    out = check50.run(f"Rscript teahouse.R Light Yes").stdout()
    status = check50.run(f"Rscript teahouse.R Light Yes").exit()
    if status != 0 and "unexpected" in out:
        raise check50.Failure("Could not find your use of readline. Ensure it's on a single line without stray spaces.")


@check50.check(readline)
def green_tea():
    """teahouse.R correctly recommends green tea"""
    check_recommendation("Light", "Yes", "green tea")


@check50.check(green_tea)
def black_tea():
    """teahouse.R correctly recommends black tea"""
    check_recommendation("Bold", "Yes", "black tea")


@check50.check(black_tea)
def chamomile():
    """teahouse.R correctly recommends chamomile tea"""
    check_recommendation("Light", "No", "chamomile")


@check50.check(chamomile)
def rooibos():
    """teahouse.R correctly recommends rooibos tea"""
    check_recommendation("Bold", "No", "rooibos")


@check50.check(rooibos)
def part2():
    """personal .R program exists"""
    r_filenames = glob.glob("*.R")
    if not len(r_filenames) >= 2:
        raise check50.Failure("Could not find additional .R files")


def check_recommendation(flavor: str, caffeine: str, tea: str) -> None:
    status = check50.run(f"Rscript teahouse.R {flavor} {caffeine}").exit()
    out = check50.run(f"Rscript teahouse.R {flavor} {caffeine}").stdout()

    if status != 0:
        raise check50.Failure(out)

    if tea.lower() not in out.lower():
        raise check50.Failure(
            f'Expected to find "{tea}" in output when entering "{flavor}" followed by "{caffeine}"'
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