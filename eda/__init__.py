import check50


@check50.check()
def exists():
    """eda.R exists"""
    check50.exists("eda.R")


@check50.check(exists)
def lyrics():
    """eda.R creates visualization.png"""
    check50.run("Rscript eda.R").exit(0)
    check50.exists("visualization.png")
