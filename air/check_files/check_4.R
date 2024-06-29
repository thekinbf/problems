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

# Check if load was successful
if (!load_successful("4.RData")) {
  cat("Failed to load 4.RData")
  quit(status = 1)
}

# Check if an air object exists
if (!exists("air")) {
  cat("`air` tibble does not exist in 4.RData")
  quit(status = 1)
}

# Check if air is a tibble
if (!("tbl_df" %in% class(air))) {
  cat("`air` in 4.RData is not a tibble")
  quit(status = 1)
}

# Check if the air tibble contains emissions column sorted in descending order
if (!all(diff(air$emissions) <= 0)) {
  cat("air tibble does not sort emissions column in descending order")
  quit(status = 1)
}

# Check if the county vector has only a single unique county
if (length(unique(air$county)) != 1) {
  cat("air tibble does not contain data from only one county")
  quit(status = 1)
}
