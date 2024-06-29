# Attempt to load the file and handle any errors
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
if (!load_successful("6.RData")) {
  cat("Failed to load 6.RData")
  quit(status = 1)
}

# Check if load was successful
if (!load_successful("check_6.RData")) {
  cat("Failed to load check_6.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Check if air exists in 6.RData
if (!exists("air")) {
  cat("`air` tibble does not exist in 6.RData")
  quit(status = 1)
}

# Check if air is a tibble by inspecting its class
if (!("tbl_df" %in% class(air))) {
  cat("`air` is not a tibble")
  quit(status = 1)
}

# Check if check_air exists in check_6.RData
if (!exists("check_air")) {
  cat("`check_air` tibble does not exist in check_6.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Check if the air tibble contains only the specified columns
extra_columns <- setdiff(colnames(air), colnames(check_air))
if (length(extra_columns) > 0) {
  cat("tibble in air.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Check if the air tibble contains all the specified columns
missing_columns <- setdiff(colnames(check_air), colnames(air))
if (length(missing_columns) > 0) {
  cat("tibble in air.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Check if air contains the same data, in the same order, as check_air
if (!all.equal(air, check_air)) {
  cat("tibble in 6.RData contains rows that are out of order or different from what's expected")
  quit(status = 1)
}
