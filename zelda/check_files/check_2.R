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
if (!load_successful("2.RData")) {
  cat("Failed to load 2.RData")
  quit(status = 1)
}

# Load is successful
if (!load_successful("check_2.RData")) {
  cat("Failed to load check_2.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Object exists
if (!exists("zelda")) {
  cat("`zelda` tibble does not exist in 2.RData")
  quit(status = 1)
}

# Object exists
if (!exists("check_zelda")) {
  cat("`check_zelda` tibble does not exist in check_2.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Object is a tibble
if (!("tbl_df" %in% class(zelda))) {
  cat("`zelda` is not a tibble")
  quit(status = 1)
}

# Object is a tibble
if (!("tbl_df" %in% class(check_zelda))) {
  cat("`check_zelda` is not a tibble. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Tibble contains only specified columns
extra_columns <- setdiff(colnames(zelda), colnames(check_zelda))
if (length(extra_columns) > 0) {
  cat("tibble in 2.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains all specified columns
missing_columns <- setdiff(colnames(check_zelda), colnames(zelda))
if (length(missing_columns) > 0) {
  cat("tibble in 2.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Objects are equal
if (!isTRUE(all.equal(zelda, check_zelda))) {
  differences <- which(!apply(zelda == check_zelda, 1, all))
  cat("tibble in 2.RData contains rows that are out of order or different from what's expected")
  quit(status = 1)
}
