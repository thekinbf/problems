import check50


@check50.check()
def exists():
    """.RData files exist"""
    for filename in ["zelda.RData", "2.RData", "3.RData", "4.RData", "5.RData"]:
        check50.exists(filename)


@check50.check(exists)
def check_1():
    """zelda.RData contains tidy zelda tibble"""
    run_check("check_1.R")


@check50.check(check_1)
def check_2():
    """2.RData contains tibble with correct data"""
    check50.include("check_files/check_2.RData")
    run_check("check_2.R")


@check50.check(check_2)
def check_3():
    """3.RData contains tibble with correct data"""
    check50.include("check_files/check_3.RData")
    run_check("check_3.R")


@check50.check(check_3)
def check_4():
    """4.RData contains tibble with correct data"""
    check50.include("check_files/check_4.RData")
    run_check("check_4.R")


@check50.check(check_4)
def check_5():
    """5.RData contains tibble with correct data"""
    check50.include("check_files/check_5.RData")
    run_check("check_5.R")


def run_check(filename: str) -> None:
    check50.include(f"check_files/{filename}")
    status = check50.run(f"Rscript {filename}").exit()
    if status != 0:
        out = check50.run(f"Rscript {filename}").stdout()
        raise check50.Failure(out)
