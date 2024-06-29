expected_columns <- c(
  "state",
  "county",
  "pollutant",
  "emissions",
  "level_1",
  "level_2",
  "level_3",
  "level_4"
)

expected_rows <- 32015

load_successful <- function(filename) {
  tryCatch({
    load(filename, envir = .GlobalEnv)
    TRUE
  }, error = function(e) {
    FALSE
  }, warning = function(w) {
    FALSE
  }, message = function(m) {
    FALSE
  })
}

# Load is successful
if (!load_successful("air.RData")) {
  cat("Failed to load air.RData")
  quit(status = 1)
}

# Object exists
if (!exists("air")) {
  cat("`air` tibble does not exist in air.RData")
  quit(status = 1)
}

# Object is a tibble
if (!("tbl_df" %in% class(air))) {
  cat("`air` in air.RData is not a tibble")
  quit(status = 1)
}

# Tibble contains only specified columns
extra_columns <- setdiff(colnames(air), expected_columns)
if (length(extra_columns) > 0) {
  cat("tibble in air.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains all specified columns
missing_columns <- setdiff(expected_columns, colnames(air))
if (length(missing_columns) > 0) {
  cat("tibble in air.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains expected rows
if (nrow(air) != expected_rows) {
  cat("tibble in air.RData does not contain all specified rows")
  quit(status = 1)
}
