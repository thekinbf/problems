import check50
import re


@check50.check()
def exists():
    """believe.R and test-believe.R exist"""
    check50.exists("believe.R")
    check50.exists("test-believe.R")


@check50.check(exists)
def believe_error():
    """believe.R runs without error"""
    status = check50.run("Rscript believe.R").exit()
    out = check50.run("Rscript believe.R").stdout()
    if status != 0:
        raise check50.Failure(out)


@check50.check(exists)
def test_believe_error():
    """test-believe.R runs without error"""
    status = check50.run("Rscript test-believe.R").exit()
    out = check50.run("Rscript test-believe.R").stdout()
    if status != 0:
        if "could not find function" in out:
            raise check50.Failure("Oops! Did you forget to include `source(\"believe.R\")` in `test-believe.R`?")
        raise check50.Failure(out)


@check50.check(test_believe_error)
def test_believe_contents():
    """test-believe.R has at least 4 test_that and 4 expect functions"""
    with open("test-believe.R", "r") as f:
        content = f.read()

    test_that_calls = len(re.findall(r"\btest_that\b", content))
    expect_calls = len(re.findall(r"\bexpect\w+\b", content))

    if test_that_calls < 4:
        raise check50.Failure("Less than 4 calls to test_that found in test-str_length.R")

    if expect_calls < 4:
        raise check50.Failure("Less than 4 calls to functions starting with expect found in test-str_length.R")
