load("air.RData")
load("check_air.RData")

if (any(!(colnames(air) %in% colnames(check_air)))) {
    cat("air tibble contains columns not specified")
    quit(status = 1)
} else if (any(!(colnames(check_air) %in% colnames(air)))) {
    cat("air tibble does not contains all columns specified")
    quit(status = 2)
} else if (nrow(air) != nrow(check_air)) {
    cat("air tibble does not contain all rows from air.csv")
    quit(status = 3)
}
