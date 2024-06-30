import check50
import glob
import re


@check50.check()
def exists():
    """All required files and folders exist"""
    check50.exists("DESCRIPTION")
    check50.exists("NAMESPACE")
    check50.exists("R")
    check50.exists("man")
    check50.exists("tests")


@check50.check(exists)
def check_description():
    """DESCRIPTION file is of sufficient length and contains video URL"""
    with open("DESCRIPTION", "r") as f:
        contents = f.read().lower()

    if len(contents) < 100:
        raise check50.Failure(f"DESCRIPTION is not long enough.")

    urls = re.findall("https?:\/\/[\w/\-?=%.]+\.[\w/\-?=%.]+", contents)
    if not urls:
        raise check50.Failure(f"Video URL is missing.")


@check50.check(check_description)
def check_r_files():
    """At least 3 .R files present in R folder"""
    r_files = glob.glob("R/*.R")
    if (num_files := len(r_files)) < 3:
        raise check50.Failure(f"Expected to find 3 .R files in R folder. Found {num_files}.")

    for file in r_files:
        test_contents(pattern="function", filename=file, quantity=1)


@check50.check(check_r_files)
def check_man_files():
    """At least 3 .Rd files present in man folder"""
    rd_files = glob.glob("man/*.Rd")
    if (num_files := len(rd_files)) < 3:
        raise check50.Failure(f"Expected to find 3 .Rd files in man folder. Found {num_files}.")
    
    for file in rd_files:
        test_contents(pattern=r"name", filename=file, quantity=1)
        test_contents(pattern=r"description", filename=file, quantity=1)
        test_contents(pattern=r"usage", filename=file, quantity=1)
        test_contents(pattern=r"arguments", filename=file, quantity=1)
        test_contents(pattern=r"value", filename=file, quantity=1)
        test_contents(pattern=r"examples", filename=file, quantity=1)


@check50.check(check_man_files)
def check_test_files():
    """At least 3 .R files present in tests folder"""
    test_files = glob.glob("tests/**/*.R")
    if (num_files := len(test_files)) < 3:
        raise check50.Failure(f"Expected to find 3 .R files in tests folder. Found {num_files}.")


def test_contents(pattern: str, filename: str, quantity: int = 1) -> None:
    """
    Tests if the given pattern is in the filename quantity number of times

    positional arguments:
        pattern (str)       regex pattern to check for
        filename (str)      the file in which to look for the pattern
        quantity (int)      the number of times the pattern should appear

    raises:
        check50.Failure if the pattern is not found quantity number of times
    """
    with open(filename, "r") as f:
        contents = f.read()

    if not len(re.findall(pattern, contents, re.IGNORECASE)) >= quantity:
        if quantity == 1:
            message = f"Expected to find at least {quantity} {pattern} statement in {filename}"
        else:
            message = f"Expected to find at least {quantity} {pattern} statements in {filename}"
        raise check50.Failure(message)