import check50
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

    
@check50.check(readline)
def green_tea():
    """teahouse.R correctly recommends green tea"""
    out = check50.run("Rscript teahouse.R Light Yes").stdout()
    if "green tea" not in out.lower():
        raise check50.Failure("Expected to find \"green tea\" in output when entering \"Light\" followed by \"Yes\"")


@check50.check(readline)
def black_tea():
    """teahouse.R correctly recommends black tea"""
    out = check50.run("Rscript teahouse.R Bold Yes").stdout()
    if "black tea" not in out.lower():
        raise check50.Failure("Expected to find \"black tea\" in output when entering \"Bold\" followed by \"Yes\"")


@check50.check(readline)
def chamomile():
    """teahouse.R correctly recommends chamomile tea"""
    out = check50.run("Rscript teahouse.R Light No").stdout()
    if "chamomile" not in out.lower():
        raise check50.Failure("Expected to find \"chamomile\" in output when entering \"Light\" followed by \"No\"")


@check50.check(readline)
def rooibos():
    """teahouse.R correctly recommends rooibos tea"""
    out = check50.run("Rscript teahouse.R Bold No").stdout()
    if "rooibos" not in out.lower():
        raise check50.Failure("Expected to find \"rooibos\" in output when entering \"Bold\" followed by \"No\"")


def replace_readline(contents: list[str]) -> list[str]:
    """Prepares an interactive R script to be run with command line arguments"""
    modified_contents = []
    readline_count = 0

    for line in contents:
        if "readline" in line:
            readline_count += 1
            line = re.sub(
                r"readline\(.*\)",
                f"commandArgs(trailingOnly = TRUE)[{readline_count}]",
                line,
            )
        modified_contents.append(line)

    return modified_contents

