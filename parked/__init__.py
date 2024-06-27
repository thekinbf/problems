import check50


@check50.check()
def exists():
    """parked.R exists"""
    check50.exists("parked.R")


@check50.check(exists)
def lyrics():
    """parked.R creates lyrics.png"""
    check50.run("Rscript parked.R").exit(0)
    check50.exists("lyrics.png")
