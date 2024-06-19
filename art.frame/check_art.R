source("art.R")

if (!exists("art")) {
    quit(status = 1)
}

if (all(art == " " | art == "")) {
    quit(status = 2)
}

if (ncol(art) < 3 || nrow(art) < 3) {
    quit(status = 3)
}
