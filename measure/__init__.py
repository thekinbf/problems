import check50
import re


@check50.check()
def exists():
    """test-str_length.R exists"""
    check50.exists("test-str_length.R")


@check50.check(exists)
def num_tests():
    """test-str_length.R has at least 4 `test_that` and 4 `expect` functions"""
    with open("test-str_length.R", "r") as f:
        content = f.read()

    test_that_calls = len(re.findall(r"\btest_that\b", content))
    expect_calls = len(re.findall(r"\bexpect\w+\b", content))

    if test_that_calls < 4:
        raise check50.Failure("Less than 4 calls to `test_that` found in test-str_length.R")

    if expect_calls < 4:
        raise check50.Failure("Less than 4 calls to functions starting with `expect` found in test-str_length.R")
