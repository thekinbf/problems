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
if (!load_successful("4.RData")) {
  cat("Failed to load 4.RData")
  quit(status = 1)
}

# Object exists
if (!exists("air")) {
  cat("`air` tibble does not exist in 4.RData")
  quit(status = 1)
}

# Object is a tibble
if (!("tbl_df" %in% class(air))) {
  cat("`air` in 4.RData is not a tibble")
  quit(status = 1)
}

# Tibble contains only specified columns
extra_columns <- setdiff(colnames(air), expected_columns)
if (length(extra_columns) > 0) {
  cat("tibble in 4.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains all specified columns
missing_columns <- setdiff(expected_columns, colnames(air))
if (length(missing_columns) > 0) {
  cat("tibble in 4.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble's emissions column is sorted in descending order
if (!all(diff(air$emissions) <= 0)) {
  cat("air tibble does not sort emissions column in descending order")
  quit(status = 1)
}

# Tibble contains data for only 1 county
if (length(unique(air$county)) != 1) {
  cat("air tibble does not contain data from only one county")
  quit(status = 1)
}
