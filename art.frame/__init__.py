import check50


@check50.check()
def exists():
    """art.R exists"""
    check50.exists("art.R")
    check50.include("check_art.R")


@check50.check(exists)
def error():
    """art.R runs without error"""
    check50.run("Rscript art.R").exit(0)


@check50.check(error)
def name():
    """art.R defines a data frame named art"""
    if check50.run("Rscript check_art.R").exit() == 1:
        raise check50.Failure('art.R does not define a data frame named "art"')


@check50.check(error)
def nonempty():
    """art data frame is non-empty"""
    if check50.run("Rscript check_art.R").exit() == 2:
        raise check50.Failure("art data frame seems to be empty")


@check50.check(error)
def size():
    """art data frame contains at least 3 rows and 3 columns"""
    if check50.run("Rscript check_art.R").exit() == 3:
        raise check50.Failure(
            "art data frame seems contain fewer than 3 rows or 3 columns"
        )
