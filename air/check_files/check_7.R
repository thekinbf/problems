load("7.RData")
load("check_7.RData")

if (!all(colnames(air) %in% colnames(check_air))) {
  cat("air tibble contains columns not in specification")
  quit(status = 1)
} else if (!all(colnames(check_air) %in% colnames(air))) {
  cat("air tibble does not contain all columns specified")
  quit(status = 1)
} else if (!all(check_air$source == air$source)) {
  cat("air tibble does not correctly sort sources")
} else if (!all(check_air$pollutant == air$pollutant)) {
  cat("air tibble does not correctly sort pollutants")
} else if (!all(check_air$emissions == air$emissions)) {
  cat("air tibble does not correctly sum emissions for each pollutant")
  quit(status = 1)
}
