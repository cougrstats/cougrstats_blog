---
title: An Introduction to data.table using sythetic lat/lon data
author: Nicholas A. Potter
date: '2020-04-15'
categories:
  - Package Introductions
tags:
  - data.table
slug: an-introduction-to-data-table-using-sythetic-lat-lon-data
---

_By Nicholas A. Potter_

This is a short introduction to using data.table based on my work with climate data.

## Initial setup

Let's begin by generating some data to work with. We'll use the following packages:

```r
# If you don't have the packages below, install with:
#install.packages(c("data.table", "readr", "dplyr", "microbenchmark"))

library(data.table)
library(dplyr) # tidyverse data manipulation
library(readr) # tidyverse reading in data
library(microbenchmark) # for timing code to see which is faster
```

We will work with a grid of latitude and longitude points, and we'll generate some fake temperature and precip data:

```r
# grid resolution
res <- 0.0416666666666667

# Grid extents
lats <- seq(  24.358333333333333,  52.909999999999997, by = res)
lons <- seq(-124.933333300000000, -66.016666633333330, by = res)

# Define a data.table
dt <- data.table(expand.grid(lat = lats, lon = lons))

# default printing of data.tables is screen friendly:
dt

##              lat        lon
##      1: 24.35833 -124.93333
##      2: 24.40000 -124.93333
##      3: 24.44167 -124.93333
##      4: 24.48333 -124.93333
##      5: 24.52500 -124.93333
##     ---
## 970686: 52.73333  -66.01667
## 970687: 52.77500  -66.01667
## 970688: 52.81667  -66.01667
## 970689: 52.85833  -66.01667
## 970690: 52.90000  -66.01667

# Assume:
# GDD is a function of latitude (Areas closer to the poles are less warm)
# Precip is random

# Equivalent to dplyr::mutate(gdd = ..., prec = ...)
dt[, `:=`(
  gdd = 3000 - 70*(lat-24) + rnorm(n = nrow(dt), sd = 100),
  prec = pmax(0,rnorm(n = nrow(dt), mean = 12, sd = 3)))]
dt

##              lat        lon       gdd
##      1: 24.35833 -124.93333 3056.2775
##      2: 24.40000 -124.93333 3234.5665
##      3: 24.44167 -124.93333 2920.4358
##      4: 24.48333 -124.93333 2850.3544
##      5: 24.52500 -124.93333 2980.4107
##     ---
## 970686: 52.73333  -66.01667 1069.3607
## 970687: 52.77500  -66.01667  812.7283
## 970688: 52.81667  -66.01667  920.2619
## 970689: 52.85833  -66.01667 1137.4059
## 970690: 52.90000  -66.01667  946.3984
##             prec
##      1: 10.66249
##      2: 12.14676
##      3: 10.33538
##      4: 10.30929
##      5: 14.82836
##     ---
## 970686: 12.03940
## 970687: 13.76590
## 970688: 11.02060
## 970689: 11.92815
## 970690: 17.25918

# For comparison, a data.frame
df <- as.data.frame(dt)
```

**A good reference comparing data.table and dplyr:**

<https://atrebas.github.io/post/2019-03-03-datatable-dplyr/>

**If you're wedded to dplyr grammar and don't want to learn data.table, try `dtplyr`:**

<https://dtplyr.tidyverse.org/>

### Why data.table?

When is data.table perhaps better than the tidyverse? I like and use both, so I don't hold with the idea that there is one that is better. Instead, there are specific reasons to use each. I use data.table when:

#### 1. I need complex transformations on large data sets

As the number of rows increases, data.table becomes increasingly faster that a data.frame or tibble. This can turn a several day process into a day or less, which is huge when you inevitably end up rerunning things. By converting a script to use `data.table`, `sp`, and refactoring functions, I decreased the processing time for one year of climate data from **four days** to **five hours**. I had 90 years of data to process for a minimum of six different models...

For example, let's time a summary of gdd at a more coarse lat/lon grid:

```r
microbenchmark(
  dt[, .(gdd = mean(gdd)), by = .(lat = round(lat, 2), lon = round(lon,2))],
  times = 10, unit = "ms")

## Unit: milliseconds
##                                                                             expr
##  dt[, .(gdd = mean(gdd)), by = .(lat = round(lat, 2), lon = round(lon,      2))]
##       min       lq     mean   median
##  263.4171 265.3146 302.2987 268.0365
##        uq      max neval
##  355.6186 364.7961    10

microbenchmark(
  df %>%
    #mutate(lat = round(lat, 2), lon = round(lon, 2)) %>%
    group_by(lat = round(lat, 2), lon = round(lon, 2)) %>%
    summarize(gdd = mean(gdd)),
  times = 10, unit = "ms")

## Unit: milliseconds
##                                                                                           expr
##  df %>% group_by(lat = round(lat, 2), lon = round(lon, 2)) %>%      summarize(gdd = mean(gdd))
##       min       lq     mean   median
##  2156.705 2544.885 2627.235 2661.827
##        uq      max neval
##  2745.505 2816.072    10
```

#### 2. tidyverse grammar gets too long / complex

People will also say this is a negative, because other people can't read your code as easily. I'm not sure I agree. In my experience as a researcher, we don't collaboratively write code often. Your most common reader is going to be yourself in 3-6 months when you have to revisit something. So documenting and writing clear code is important, but data.table is clear, it's just a different language than the tidyverse. It is wonderfully succinct at times. For example, in dplyr you might write:

```r
# dplyr approach
df %>%
  mutate(lat = round(lat), lon = round(lon)) %>%
  group_by(lat, lon) %>%
  summarize(gdd = mean(gdd))

# data.table
dt[, .(gdd = mean(gdd)), by = .(lat = round(lat), lon = round(lon))]
```

That doesn't seem like much for one transformation, but if the number of transformations is high either because you have multiple data files or multiple variables that all need a different transformation, the difference in code length is substantial. It's much easier to look at 20 lines of data.table transformations than it is to look at 50 lines of dplyr transformations to accomplish the same thing.

### Using data.table

The grammar of data.table is `DT[i,j, other]`, where `i` is a logical selector on rows, `j` is operations on columns, and `other` is additional arguments for grouping, which columns to perform operations on, etc...

#### I Operations (select rows)

    # Select using the "i" argument
    dt[lat % dplyr::filter(lat < 25)

    ##             lat        lon      gdd
    ##     1: 24.35833 -124.93333 3056.277
    ##     2: 24.40000 -124.93333 3234.566
    ##     3: 24.44167 -124.93333 2920.436
    ##     4: 24.48333 -124.93333 2850.354
    ##     5: 24.52500 -124.93333 2980.411
    ##    ---
    ## 22636: 24.81667  -66.01667 2902.917
    ## 22637: 24.85833  -66.01667 2901.789
    ## 22638: 24.90000  -66.01667 2822.173
    ## 22639: 24.94167  -66.01667 2830.030
    ## 22640: 24.98333  -66.01667 3019.428
    ##             prec
    ##     1: 10.662486
    ##     2: 12.146765
    ##     3: 10.335384
    ##     4: 10.309294
    ##     5: 14.828355
    ##    ---
    ## 22636: 11.866986
    ## 22637:  9.461943
    ## 22638: 12.930729
    ## 22639: 14.225363
    ## 22640: 12.048109

    dt[lat  -67]

    ##           lat       lon      gdd      prec
    ##   1: 24.35833 -66.97500 2847.152 10.236523
    ##   2: 24.40000 -66.97500 2997.729 10.588268
    ##   3: 24.44167 -66.97500 2912.901 15.688600
    ##   4: 24.48333 -66.97500 2782.295 13.240460
    ##   5: 24.52500 -66.97500 3024.306 13.872522
    ##  ---
    ## 380: 24.81667 -66.01667 2902.917 11.866986
    ## 381: 24.85833 -66.01667 2901.789  9.461943
    ## 382: 24.90000 -66.01667 2822.173 12.930729
    ## 383: 24.94167 -66.01667 2830.030 14.225363
    ## 384: 24.98333 -66.01667 3019.428 12.048109

#### J Operations (operate on columns)

```r
# Perform an operation on specific columns
dt[, .(
  lat = mean(lat),
  lon = mean(lon),
  gdd = mean(gdd))]

##         lat     lon     gdd
## 1: 38.62917 -95.475 1975.92

# Alternatively, for all columns or just specific ones:
dt[, lapply(.SD, mean, na.rm = TRUE)] # equivalent to dplyr::transmute_all()

##         lat     lon     gdd     prec
## 1: 38.62917 -95.475 1975.92 11.99819

dt[, lapply(.SD, mean, na.rm = TRUE), .SDcols = c("gdd", "prec")]

##        gdd     prec
## 1: 1975.92 11.99819

# A more complicated function
# center GDD by removing the mean
dt[, .(lat, lon, d_gdd = gdd - mean(gdd))]

##              lat        lon      d_gdd
##      1: 24.35833 -124.93333  1080.3575
##      2: 24.40000 -124.93333  1258.6465
##      3: 24.44167 -124.93333   944.5158
##      4: 24.48333 -124.93333   874.4344
##      5: 24.52500 -124.93333  1004.4908
##     ---
## 970686: 52.73333  -66.01667  -906.5593
## 970687: 52.77500  -66.01667 -1163.1916
## 970688: 52.81667  -66.01667 -1055.6581
## 970689: 52.85833  -66.01667  -838.5141
## 970690: 52.90000  -66.01667 -1029.5216

# Perform operations on the same data set
dt[, gd_gdd := gdd - mean(gdd)] # equivalent to dplyr::mutate()

# For multiple variables at once:
dt[, `:=`(gd_gdd = gdd - mean(gdd),
          gd_prec = prec - mean(prec))]
dt

##              lat        lon       gdd
##      1: 24.35833 -124.93333 3056.2775
##      2: 24.40000 -124.93333 3234.5665
##      3: 24.44167 -124.93333 2920.4358
##      4: 24.48333 -124.93333 2850.3544
##      5: 24.52500 -124.93333 2980.4107
##     ---
## 970686: 52.73333  -66.01667 1069.3607
## 970687: 52.77500  -66.01667  812.7283
## 970688: 52.81667  -66.01667  920.2619
## 970689: 52.85833  -66.01667 1137.4059
## 970690: 52.90000  -66.01667  946.3984
##             prec     gd_gdd     gd_prec
##      1: 10.66249  1080.3575 -1.33570660
##      2: 12.14676  1258.6465  0.14857212
##      3: 10.33538   944.5158 -1.66280901
##      4: 10.30929   874.4344 -1.68889873
##      5: 14.82836  1004.4908  2.83016281
##     ---
## 970686: 12.03940  -906.5593  0.04120797
## 970687: 13.76590 -1163.1916  1.76771001
## 970688: 11.02060 -1055.6581 -0.97759204
## 970689: 11.92815  -838.5141 -0.07004544
## 970690: 17.25918 -1029.5216  5.26098430

# Or equivalently
dt[, c("gd_gdd", "gd_prec") := .(gdd - mean(gdd), prec - mean(prec))]

# Group transformations
dt[, `:=`(lat0 = round(lat), lon0 = round(lon))]
dt[, `:=`(gd_gdd = gdd - mean(gdd),
          gd_prec = prec - mean(prec)),
   by = .(lat0, lon0)]
dt

##              lat        lon       gdd
##      1: 24.35833 -124.93333 3056.2775
##      2: 24.40000 -124.93333 3234.5665
##      3: 24.44167 -124.93333 2920.4358
##      4: 24.48333 -124.93333 2850.3544
##      5: 24.52500 -124.93333 2980.4107
##     ---
## 970686: 52.73333  -66.01667 1069.3607
## 970687: 52.77500  -66.01667  812.7283
## 970688: 52.81667  -66.01667  920.2619
## 970689: 52.85833  -66.01667 1137.4059
## 970690: 52.90000  -66.01667  946.3984
##             prec     gd_gdd    gd_prec lat0
##      1: 10.66249   95.14628 -1.2601424   24
##      2: 12.14676  273.43529  0.2241363   24
##      3: 10.33538  -40.69542 -1.5872448   24
##      4: 10.30929 -110.77682 -1.6133345   24
##      5: 14.82836   45.97717  3.0862385   25
##     ---
## 970686: 12.03940   62.21880  0.2354413   53
## 970687: 13.76590 -194.41356  1.9619434   53
## 970688: 11.02060  -86.87996 -0.7833587   53
## 970689: 11.92815  130.26402  0.1241879   53
## 970690: 17.25918  -60.74347  5.4552177   53
##         lon0
##      1: -125
##      2: -125
##      3: -125
##      4: -125
##      5: -125
##     ---
## 970686:  -66
## 970687:  -66
## 970688:  -66
## 970689:  -66
## 970690:  -66

# Removing variables
dt[, `:=`(gd_gdd = NULL, gd_prec = NULL)] # dplyr::select(-gd_gdd, -gd_prec)
```

#### Other Operations (keys, indices, merges, and renaming)

```r
# Create some 2-digit lat/lon groups
dt[, `:=`(lat2 = round(lat,2), lon2 = round(lon,2))]

# No keys is okay, but operations are slower
key(dt) # No key set

## NULL

microbenchmark(
  dt[, .(gdd = mean(gdd)), by = .(lat2, lon2)],
  times = 10, unit = "ms")

## Unit: milliseconds
##                                          expr
##  dt[, .(gdd = mean(gdd)), by = .(lat2, lon2)]
##       min       lq     mean   median
##  155.8982 289.4522 323.1314 303.3228
##       uq     max neval
##  310.706 530.188    10

# Set keys that you are grouping by is faster
setkey(dt, lat2, lon2)
setkeyv(dt, c("lat2", "lon2")) #Equivalent - useful for quoted vars in functions
key(dt) # Now with lat2, lon2

## [1] "lat2" "lon2"

microbenchmark(
  dt[, .(gdd = mean(gdd)), by = .(lat2, lon2)],
  times = 10, unit = "ms")

## Unit: milliseconds
##                                          expr
##  dt[, .(gdd = mean(gdd)), by = .(lat2, lon2)]
##      min      lq     mean  median      uq
##  44.2884 46.3645 66.44499 69.0569 79.6183
##     max neval
##  96.594    10
```

#### In Functions (or for loops)

```r
#' Center variables of a data.table.
#' @param d a data.table.
#' @param vars a list of quoted column names to center.
#' @param byvar a list of quoted column names by which to center.
#' @param na.rm exclude NA?
#' @return a data.table with centered variables.
center_dt <- function(d, vars, byvars, na.rm = TRUE) {
  setkeyv(d, byvars)
  d[, lapply(.SD, function(x) { x - mean(x, na.rm = na.rm) }),
    by = byvars, .SDcols = vars]
}
dt[, `:=`(lat0 = round(lat), lon0 = round(lon))]
center_dt(dt, vars = c("gdd", "prec"), byvars = c("lat0", "lon0"))

##         lat0 lon0         gdd       prec
##      1:   24 -125   95.146283 -1.2601424
##      2:   24 -125  -45.366808  0.7401815
##      3:   24 -125  -59.763709 -1.5278002
##      4:   24 -125    4.492488 -6.7632807
##      5:   24 -125   36.774394  1.3920487
##     ---
## 970686:   53  -66  -72.051125  2.6577200
## 970687:   53  -66   75.705411  5.4217230
## 970688:   53  -66  -57.443669  1.3007194
## 970689:   53  -66 -145.215167  1.6826111
## 970690:   53  -66  -60.743466  5.4552177

# Alternatively, specify just the transformation as a function
center <- function(x) { x - mean(x) }
dt[, lapply(.SD, function(x){ center(x) }),
   by = c("lat0", "lon0"), .SDcols = c("gdd", "prec")]

##         lat0 lon0         gdd       prec
##      1:   24 -125   95.146283 -1.2601424
##      2:   24 -125  -45.366808  0.7401815
##      3:   24 -125  -59.763709 -1.5278002
##      4:   24 -125    4.492488 -6.7632807
##      5:   24 -125   36.774394  1.3920487
##     ---
## 970686:   53  -66  -72.051125  2.6577200
## 970687:   53  -66   75.705411  5.4217230
## 970688:   53  -66  -57.443669  1.3007194
## 970689:   53  -66 -145.215167  1.6826111
## 970690:   53  -66  -60.743466  5.4552177
```

#### Reading and writing data

`data.table` provides `fread` and `fwrite` to quickly read and write data.

`fread()` also takes a URL if you want to directly read data from http.

```r
microbenchmark(fwrite(dt, file = "dt.csv"), times = 1, unit = "ms")

## Unit: milliseconds
##                         expr      min
##  fwrite(dt, file = "dt.csv") 682.1413
##        lq     mean   median       uq
##  682.1413 682.1413 682.1413 682.1413
##       max neval
##  682.1413     1

microbenchmark(write_csv(dt, path = "dt.csv"), times = 1, unit = "ms")

## Unit: milliseconds
##                            expr      min
##  write_csv(dt, path = "dt.csv") 3856.494
##        lq     mean   median       uq
##  3856.494 3856.494 3856.494 3856.494
##       max neval
##  3856.494     1

microbenchmark(saveRDS(dt, file = "dt.rds"), times = 1, unit = "ms")

## Unit: milliseconds
##                          expr      min
##  saveRDS(dt, file = "dt.rds") 4002.413
##        lq     mean   median       uq
##  4002.413 4002.413 4002.413 4002.413
##       max neval
##  4002.413     1

microbenchmark(fread("dt.csv"), times = 1, unit = "ms")

## Unit: milliseconds
##             expr      min       lq     mean
##  fread("dt.csv") 298.4178 298.4178 298.4178
##    median       uq      max neval
##  298.4178 298.4178 298.4178     1

microbenchmark(read_csv("dt.csv"), times = 1, unit = "ms")

## Unit: milliseconds
##                expr      min       lq
##  read_csv("dt.csv") 2899.474 2899.474
##      mean   median       uq      max neval
##  2899.474 2899.474 2899.474 2899.474     1

microbenchmark(readRDS("dt.rds"), times = 1, unit = "ms")

## Unit: milliseconds
##               expr      min       lq
##  readRDS("dt.rds") 529.9389 529.9389
##      mean   median       uq      max neval
##  529.9389 529.9389 529.9389 529.9389     1
```
