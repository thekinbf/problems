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
if (!load_successful("5.RData")) {
  cat("Failed to load 5.RData")
  quit(status = 1)
}

# Load is successful
if (!load_successful("check_5.RData")) {
  cat("Failed to load check_5.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Object exists
if (!exists("air")) {
  cat("`air` tibble does not exist in 5.RData")
  quit(status = 1)
}

# Object exists
if (!exists("check_air")) {
  cat("`check_air` tibble does not exist in check_5.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Object is a tibble
if (!("tbl_df" %in% class(air))) {
  cat("`air` is not a tibble")
  quit(status = 1)
}

# Object is a tibble
if (!("tbl_df" %in% class(air))) {
  cat("`check_air` is not a tibble. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Tibble contains only specified columns
extra_columns <- setdiff(colnames(air), colnames(check_air))
if (length(extra_columns) > 0) {
  cat("tibble in 5.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains all specified columns
missing_columns <- setdiff(colnames(check_air), colnames(air))
if (length(missing_columns) > 0) {
  cat("tibble in 5.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains 1 row per county
if (any(table(air$county) > 1)) {
  cat("air tibble contains more than one row per county")
  quit(status = 1)
}

# Tibble contains highest emissions for each county
if (!isTRUE(all.equal(sort(air$emissions), sort(check_air$emissions)))) {
  cat("air tibble does not contain highest emissions for each county")
  quit(status = 1)
}
