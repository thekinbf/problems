import check50

@check50.check()
def exists():
    """.RData files exist"""
    for filename in ["air.RData", "2.RData", "3.RData", "4.RData", "5.RData", "6.RData", "7.RData"]:
        check50.exists(filename)
    
    check50.include("check_files/check_air.RData")
    check50.include("check_files/check_5.RData")
    check50.include("check_files/check_6.RData")
    check50.include("check_files/check_7.RData")


@check50.check(exists)
def check_1():
    """air.RData contains correctly cleaned data"""
    run_check("check_1.R")


@check50.check(check_1)
def check_2():
    """2.RData contains air tibble sorted by emissions column"""
    run_check("check_2.R")


@check50.check(check_2)
def check_3():
    """3.RData contains air tibble with only one county's data"""
    run_check("check_3.R")


@check50.check(check_3)
def check_4():
    """4.RData contains air tibble with only one county's data, sorted by emissions column"""
    run_check("check_4.R")


@check50.check(check_4)
def check_5():
    """5.RData contains air tibble with largest pollutant source for each county"""
    run_check("check_5.R")


@check50.check(check_5)
def check_6():
    """6.RData contains air tibble with total emissions for each pollutant"""
    run_check("check_6.R")


@check50.check(check_6)
def check_7():
    """7.RData contains air tibble with total emissions of each pollutant for each level 1 source"""
    run_check("check_7.R")


def run_check(filename: str) -> None:
    check50.include(f"check_files/{filename}")
    status = check50.run(f"Rscript {filename}").exit()
    if status != 0:
        out = check50.run(f"Rscript {filename}").stdout()
        raise check50.Failure(out)
