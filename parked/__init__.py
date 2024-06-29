import check50


@check50.check()
def exists():
    """parked.R exists"""
    check50.exists("parked.R")


@check50.check(exists)
def lyrics():
    """parked.R creates lyrics.png"""
    status = check50.run("Rscript parked.R").exit()
    out = check50.run("Rscript parked.R").stdout()
    
    if status != 0:
        raise check50.Failure(out)
    
    check50.exists("lyrics.png")
