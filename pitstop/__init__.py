import check50


@check50.check()
def exists():
    """pitstop.R exists"""
    check50.exists("pitstop.R")


@check50.check(exists)
def runs_interactively():
    """Opens and closes R interactive console"""
    check50.run("R").stdin("q()").stdin("n").exit(0)
