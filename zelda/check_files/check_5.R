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
if (!exists("zelda")) {
  cat("`zelda` tibble does not exist in 5.RData")
  quit(status = 1)
}

# Object exists
if (!exists("check_zelda")) {
  cat("`check_zelda` tibble does not exist in check_5.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
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
  cat("tibble in 5.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Tibble contains all specified columns
missing_columns <- setdiff(colnames(check_zelda), colnames(zelda))
if (length(missing_columns) > 0) {
  cat("tibble in 5.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Objects are equal
for (colname in c("title", "year", "system")) {
  if (length(zelda[[colname]]) < length(check_zelda[[colname]])) {
      cat(paste0("tibble in 5.RData has fewer rows than expected"))
      quit(status = 1)
  }

  if (length(zelda[[colname]]) > length(check_zelda[[colname]])) {
      cat(paste0("tibble in 5.RData has more rows than expected"))
      quit(status = 1)
  }

  if (!all(zelda[[colname]] == check_zelda[[colname]], na.rm = TRUE)) {
      cat(paste0("In ", colname, " column, tibble in 5.RData contains data that is out of order or different from what's expected"))
      quit(status = 1)
  }
}
