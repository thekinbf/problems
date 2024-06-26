load("4.RData")

if (!all(diff(air$emissions) <= 0)) {
  cat("air tibble does not sort emissions column in descending order")
  quit(status = 1)
} else if (length(unique(air$county)) != 1) {
  cat("air tibble does not contain data from only one county")
  quit(status = 2)
}
