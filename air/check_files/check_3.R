load("3.RData")

# Check if the county vector has only a single unique county
if (length(unique(air$county)) != 1) {
  cat("air tibble does not contain data from only one county")
  quit(status = 1)
}
