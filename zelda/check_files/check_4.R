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
if (!load_successful("4.RData")) {
  cat("Failed to load 4.RData")
  quit(status = 1)
}

# Check if load was successful
if (!load_successful("check_4.RData")) {
  cat("Failed to load check_4.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Check if zelda exists in 4.RData
if (!exists("zelda")) {
  cat("`zelda` tibble does not exist in 4.RData")
  quit(status = 1)
}

# Check if zelda is a tibble by inspecting its class
if (!("tbl_df" %in% class(zelda))) {
  cat("`zelda` is not a tibble")
  quit(status = 1)
}

# Check if check_zelda exists in check_4.RData
if (!exists("check_zelda")) {
  cat("`check_zelda` tibble does not exist in check_4.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Check if zelda only contains columns in check_zelda
extra_columns <- setdiff(colnames(zelda), colnames(check_zelda))
if (length(extra_columns) > 0) {
  cat("tibble in 4.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Check if zelda contains all columns in check_zelda
missing_columns <- setdiff(colnames(check_zelda), colnames(zelda))
if (length(missing_columns) > 0) {
  cat("tibble in 4.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Check if zelda contains the same data, in the same order, as check_zelda
if (!all.equal(zelda, check_zelda)) {
  differences <- which(!apply(zelda == check_zelda, 1, all))
  cat("tibble in 4.RData contains rows that are out of order or different from what's expected")
  quit(status = 1)
}
