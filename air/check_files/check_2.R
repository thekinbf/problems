load("2.RData")

if (!all(diff(air$emissions) <= 0)) {
  cat("air tibble does not sort emissions column in descending order")
  quit(status = 1)
}
