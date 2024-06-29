import check50


@check50.check()
def exists():
    """eda.R exists"""
    check50.exists("eda.R")


@check50.check(exists)
def eda():
    """eda.R creates visualization.png"""
    status = check50.run("Rscript eda.R").exit()
    out = check50.run("Rscript eda.R").stdout()
    
    if status != 0:
        raise check50.Failure(out)

    check50.exists("visualization.png")
