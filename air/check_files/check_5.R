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
if (!load_successful("5.RData")) {
  cat("Failed to load 5.RData")
  quit(status = 1)
}

# Check if load was successful
if (!load_successful("check_5.RData")) {
  cat("Failed to load check_5.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

# Check if air exists in 5.RData
if (!exists("air")) {
  cat("`air` tibble does not exist in 5.RData")
  quit(status = 1)
}

# Check if zelda is a tibble by inspecting its class
if (!("tbl_df" %in% class(air))) {
  cat("`air` is not a tibble")
  quit(status = 1)
}

# Check if check_zelda exists in check_2.RData
if (!exists("check_air")) {
  cat("`check_air` tibble does not exist in check_5.RData. Not your fault! Contact <sysadmins@cs50.harvard.edu>")
  quit(status = 1)
}

if (any(table(air$county) > 1)) {
  cat("air tibble contains more than one row per county")
  quit(status = 1)
}

if (!all(sort(air$emissions) == sort(check_air$emissions))) {
  cat("air tibble does not contain highest emissions for each county")
  quit(status = 1)
}
