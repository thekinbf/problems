expected_columns <- c(
  "title",
  "year",
  "system",
  "directors",
  "producers",
  "designers",
  "programmers",
  "writers",
  "composers",
  "artists"
)

# Attempt to load the file and handle any errors
load_successful <- tryCatch({
  load("zelda.RData")
  TRUE
}, error = function(e) {
  FALSE
}, warning = function(w) {
  FALSE
}, message = function(m) {
  FALSE
})

# Check if load was successful
if (!load_successful) {
  cat("Failed to load zelda.RData")
  quit(status = 1)
}

# Check if the zelda tibble exists
if (!exists("zelda")) {
  cat("`zelda` tibble does not exist in zelda.RData")
  quit(status = 1)
}

# Check if zelda is a tibble by inspecting its class
if (!("tbl_df" %in% class(zelda))) {
  cat("`zelda` in zelda.RData is not a tibble")
  quit(status = 1)
}

# Check if the zelda tibble contains only the specified columns
extra_columns <- setdiff(colnames(zelda), expected_columns)
if (length(extra_columns) > 0) {
  cat("tibble in zelda.RData contains column(s) not specified:", paste(extra_columns, collapse = ", "))
  quit(status = 1)
}

# Check if the zelda tibble contains all the specified columns
missing_columns <- setdiff(expected_columns, colnames(zelda))
if (length(missing_columns) > 0) {
  cat("tibble in zelda.RData does not contain all specified columns. Missing columns:", paste(missing_columns, collapse = ", "))
  quit(status = 1)
}

# Check if the zelda tibble contains unique combinations of title, year, and system
if (any(duplicated(zelda[, c("title", "year", "system")]))) {
  cat("tibble in zelda.RData contains duplicate combinations of title, year, and system")
  quit(status = 1)
}
