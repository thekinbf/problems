import check50
import re


@check50.check()
def exists():
    """pitstop.R exists"""
    check50.exists("pitstop.R")
    check50.include(
        "bahrain.csv",
        "imola.csv",
        "jeddah.csv",
        "melbourne.csv",
        "miami.csv",
        "shanghai.csv",
        "suzuka.csv",
    )


@check50.check(exists)
def uses_readline():
    """pitstop.R uses readline"""
    with open("pitstop.R", "r") as f:
        contents = f.readlines()

    new_contents = replace_readline(contents)
    if new_contents == contents:
        raise check50.Failure(f"Could not find readline in pitstop.R")

    with open("pitstop.R", "w") as f:
        f.writelines(new_contents)


@check50.check(uses_readline)
def bahrain():
    """Correctly prints Bahrain data"""
    check_statistics(
        "bahrain.csv", pitstops="43", fastest="2.23", slowest="52.44", total="202.01"
    )


@check50.check(uses_readline)
def imola():
    """Correctly prints Imola data"""
    check_statistics("imola.csv", pitstops="27", fastest="2.09", slowest="10.94", total="83.18")


@check50.check(uses_readline)
def jeddah():
    """Correctly prints Jeddah data"""
    check_statistics(
        "jeddah.csv", pitstops="19", fastest="2.44", slowest="41.61", total="131.53"
    )


@check50.check(uses_readline)
def melbourne():
    """Correctly prints Melbourne data"""
    check_statistics(
        "melbourne.csv", pitstops="36", fastest="2.1", slowest="31.18", total="159.11"
    )


@check50.check(uses_readline)
def miami():
    """Correctly prints Miami data"""
    check_statistics("miami.csv", pitstops="28", fastest="1.94", slowest="11.05", total="98.53")


@check50.check(uses_readline)
def shanghai():
    """Correctly prints Shanghai data"""
    check_statistics(
        "shanghai.csv", pitstops="39", fastest="1.9", slowest="19.35", total="135.82"
    )


@check50.check(uses_readline)
def suzuka():
    """Correctly prints Suzuka data"""
    check_statistics(
        "suzuka.csv", pitstops="36", fastest="2.08", slowest="5.43", total="105.32"
    )


def check_statistics(
    filename: str, pitstops: str, fastest: str, slowest: str, total: str
):
    out = check50.run(f"Rscript pitstop.R {filename}").stdout()

    if not re.search(rf"\b{re.escape(pitstops)}\b", out):
        raise check50.Failure(f"Could not find {pitstops} pit stops in output.")

    if not re.search(rf"\b{re.escape(fastest)}\b", out):
        raise check50.Failure(f"Could not find fastest time of {fastest}s in output.")

    if not re.search(rf"\b{re.escape(slowest)}\b", out):
        raise check50.Failure(f"Could not find slowest time of {slowest}s in output.")

    if not re.search(rf"\b{re.escape(total)}\b", out):
        raise check50.Failure(f"Could not find total time of {total}s in output.")


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
