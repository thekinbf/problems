import check50


@check50.check()
def exists():
    """pitstop.R exists"""
    check50.exists("pitstop.R")


@check50.check(exists)
def runs_interactively():
    """Tests retrieving stdout"""
    out = check50.run("R").stdin("source('pitstop.R')").stdin("pitstop.csv").stdin("q()").stdin("n").stdout()
    check50.log(str(out))
