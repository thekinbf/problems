import check50


@check50.check()
def exists():
    """variations.R exists"""
    check50.exists("variations.R")


@check50.check(exists)
def variations():
    """variations.R prints random sequences of 20 characters"""
    out = check50.run("Rscript variations.R").stdout(timeout=6).strip()
    length = len(out)
    if length != 20:
        raise check50.Failure(f"variations.R printed a sequence of {length} characters")
