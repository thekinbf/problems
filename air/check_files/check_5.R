load("5.RData")
load("check_5.RData")

if (any(table(air$county) > 1)) {
  cat("air tibble contains more than one row per county")
  quit(status = 1)
}

if (!all(sort(air$emissions) == sort(check_air$emissions))) {
  cat("air tibble does not contain highest emissions for each county")
  quit(status = 1)
}
