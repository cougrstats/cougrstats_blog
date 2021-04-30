---
title: Date and Time data in R
author: cougrstats
date: '2018-02-21'
categories:
  - Package Introductions
tags:
  - Date
  - date/time
  - lubridate
  - POSIXct
  - POSIXlt
  - zoo
slug: date-and-time-data-in-r
---

_Author: Stephanie Labou_

## Getting started

First, let's read in the date/time data created for this lesson. We'll read in the data with strings as character data, not factors.

```r
dat_orig <- read.csv("date_time_examples.csv", stringsAsFactors = FALSE)
```

What does this data look like? What structure is it?

```r
dat_orig

##   dates_only         date_times
## 1  12/5/2017  5-12-2017 5:23:10
## 2 12/13/2017 13-12-2017 3:10:45
## 3   1/9/2018  9-1-2018 14:15:10
## 4  2/15/2018 15-2-2018 19:25:05
## 5  2/21/2018  21-2-2018 8:55:35

str(dat_orig)

## 'data.frame':    5 obs. of  2 variables:
##  $ dates_only: chr  "12/5/2017" "12/13/2017" "1/9/2018" "2/15/2018" ...
##  $ date_times: chr  "5-12-2017 5:23:10" "13-12-2017 3:10:45" "9-1-2018 14:15:10" "15-2-2018 19:25:05" ...
```

We'll make a new dataframe so we can compare changes we make to what we read in originally.

```r
dat <- dat_orig
```

We want to convert these character date formats into something R wil recognize as dates.

## The "Date" format

R has built-in functions that can convert character data to a date format. The most popular of these is [as.Date](https://stat.ethz.ch/R-manual/R-devel/library/base/html/as.Date.html).

For example, if I want to turn the "dates_only" column into a recognizable date format, I would run:

```r
dat$dates_only <- as.Date(dat$dates_only, format = "%m/%d/%Y")
```

Now when we look at our data, we see that it is a "Date" class and the dates are all in a new standard format.

```r
str(dat)

## 'data.frame':    5 obs. of  2 variables:
##  $ dates_only: Date, format: "2017-12-05" "2017-12-13" ...
##  $ date_times: chr  "5-12-2017 5:23:10" "13-12-2017 3:10:45" "9-1-2018 14:15:10" "15-2-2018 19:25:05" ...
```

We also see that our date data has been restructured to be year-month-day.

```r
dat

##   dates_only         date_times
## 1 2017-12-05  5-12-2017 5:23:10
## 2 2017-12-13 13-12-2017 3:10:45
## 3 2018-01-09  9-1-2018 14:15:10
## 4 2018-02-15 15-2-2018 19:25:05
## 5 2018-02-21  21-2-2018 8:55:35
```

The "format" argument in as.Date() specifies what format the data are in _originally_. In this case, we have a "month/day/year" format. Since date data comes in all kinds of formats, built-in codes include:

<table style="margin-left:auto;margin-right:auto;" class="table" >

<tr >
Code
Value
</tr>

<tbody >
<tr >

<td style="text-align:left;" >%d
</td>

<td style="text-align:left;" >Day of the month (decimal number)
</td>
</tr>
<tr >

<td style="text-align:left;" >%m
</td>

<td style="text-align:left;" >Month (decimal number)
</td>
</tr>
<tr >

<td style="text-align:left;" >%b
</td>

<td style="text-align:left;" >Month (abbreviated)
</td>
</tr>
<tr >

<td style="text-align:left;" >%B
</td>

<td style="text-align:left;" >Month (full name)
</td>
</tr>
<tr >

<td style="text-align:left;" >%y
</td>

<td style="text-align:left;" >Year (2 digit)
</td>
</tr>
<tr >

<td style="text-align:left;" >%Y
</td>

<td style="text-align:left;" >Year (4 digit)
</td>
</tr>
</tbody>
</table>

It is very important to specify the date format of the character data you are trying to convert to a "Date" format! If you don't specify a format, things can go very wrong with your data:

```r
# Make new data frame
dat2 <- dat_orig

# Use as.Date() without specifying format
dat2$dates_only <- as.Date(dat2$dates_only)

# Check out the result
dat2

##   dates_only         date_times
## 1 0012-05-20  5-12-2017 5:23:10
## 2       <NA> 13-12-2017 3:10:45
## 3 0001-09-20  9-1-2018 14:15:10
## 4       <NA> 15-2-2018 19:25:05
## 5       <NA>  21-2-2018 8:55:35
```

Something went awry here with _no error_. Not good!

In some cases, you may encounter actual errors instead of behind-the-scenes shenanigans. For example:

```r
as.Date("2.4.2017")

## Error in charToDate(x): character string is not in a standard unambiguous format
```

## POSIXct format

POSIXct stands for "Portable Operating System Interface calendar time." The name is a mouthful, but POSIXct is useful when you time data along with date data, which we have in the second column of our data.

```r
##   dates_only         date_times
## 1  12/5/2017  5-12-2017 5:23:10
## 2 12/13/2017 13-12-2017 3:10:45
## 3   1/9/2018  9-1-2018 14:15:10
## 4  2/15/2018 15-2-2018 19:25:05
## 5  2/21/2018  21-2-2018 8:55:35
```

For instance, what happens when we try to use as.Date() with date time data?

```r
## [1] "2017-12-05" "2017-12-13" "2018-01-09" "2018-02-15" "2018-02-21"
```

Even if we try to specify a day/month/year hour:minute:second format, we lose the time information.

The equivalent function [as.POSIXct](https://stat.ethz.ch/R-manual/R-devel/library/base/html/as.POSIXlt.html) can handle time data as well as date data.

```r
as.POSIXct(dat3$date_times, format = "%d-%m-%Y %H:%M:%S")

## [1] "2017-12-05 05:23:10 PST" "2017-12-13 03:10:45 PST"
## [3] "2018-01-09 14:15:10 PST" "2018-02-15 19:25:05 PST"
## [5] "2018-02-21 08:55:35 PST"
```

Note that this defaulted to Pacific Standard Time. We can change this by specifying which timezone we want.

```r
as.POSIXct(dat3$date_times, format = "%d-%m-%Y %H:%M:%S", tz = "GMT")

## [1] "2017-12-05 05:23:10 GMT" "2017-12-13 03:10:45 GMT"
## [3] "2018-01-09 14:15:10 GMT" "2018-02-15 19:25:05 GMT"
## [5] "2018-02-21 08:55:35 GMT"
```

If we assign the date_times column to be a date using POSIXct, we can see this reflected in the data structure.

```r
# Change date_times column to be POSIXct date
dat3$date_times <- as.POSIXct(dat3$date_times, format = "%d-%m-%Y %H:%M:%S", tz = "GMT")

str(dat3)

## 'data.frame':    5 obs. of  2 variables:
##  $ dates_only: chr  "12/5/2017" "12/13/2017" "1/9/2018" "2/15/2018" ...
##  $ date_times: POSIXct, format: "2017-12-05 05:23:10" "2017-12-13 03:10:45" ...
```

So far, this seems pretty similar to as.Date() output, except we can include hours/minutes/seconds. On the surface, this is true, but differences appear when we look closer.

Let's check out what's going on behind-the-scenes with Date objects.

```r
unclass(dat$dates_only)

## [1] 17505 17513 17540 17577 17583
```

Unexpected! Looking closer at the [Dates](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Dates.html) documentation, we see that "dates are represented as the number of days since 1970-01-01, with negative values for earlier dates."

What about as.POSIXct?

```r
unclass(dat3$date_times)

## [1] 1512451390 1513134645 1515507310 1518722705 1519203335
## attr(,"tzone")
## [1] "GMT"
```

Behind the scenes, POSIXct stores data as seconds since the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time).

## POSIXlt format

POSIXlt stands for "Portable Operating System Interface local time." The syntax ([as.POSIXlt](https://stat.ethz.ch/R-manual/R-devel/library/base/html/as.POSIXlt.html)) and output look extremely similar to POSIXct.

```r
# New dataframe
dat4 <- dat_orig

# Use POSIXlt for dates
as.POSIXlt(dat4$date_times, format = "%d-%m-%Y %H:%M:%S")

## [1] "2017-12-05 05:23:10 PST" "2017-12-13 03:10:45 PST"
## [3] "2018-01-09 14:15:10 PST" "2018-02-15 19:25:05 PST"
## [5] "2018-02-21 08:55:35 PST"
```

As with Date and POSIXct, the difference is behind the scenes: POSIXlt stores data as a list
of day, month, year, hour, minute, second, and attributes.

```r
# Format dates using POSIXlt
dat4$date_times <- as.POSIXlt(dat4$date_times, format = "%d-%m-%Y %H:%M:%S")

# Check data structure
str(dat4)

## 'data.frame':    5 obs. of  2 variables:
##  $ dates_only: chr  "12/5/2017" "12/13/2017" "1/9/2018" "2/15/2018" ...
##  $ date_times: POSIXlt, format: "2017-12-05 05:23:10" "2017-12-13 03:10:45" ...

# Unclass to see behind the scenes
unclass(dat4$date_times)

## $sec
## [1] 10 45 10  5 35
##
## $min
## [1] 23 10 15 25 55
##
## $hour
## [1]  5  3 14 19  8
##
## $mday
## [1]  5 13  9 15 21
##
## $mon
## [1] 11 11  0  1  1
##
## $year
## [1] 117 117 118 118 118
##
## $wday
## [1] 2 3 2 4 3
##
## $yday
## [1] 338 346   8  45  51
##
## $isdst
## [1] 0 0 0 0 0
##
## $zone
## [1] "PST" "PST" "PST" "PST" "PST"
##
## $gmtoff
## [1] NA NA NA NA NA
```

## Packages for date/time data

Everything we've done so far as been using built-in R functions. So let's say we get our data in the right format for the type of data.

```r
# Make useable dataframe
dat_use <- dat_orig

# Format dates_only to be Date objects
dat_use$dates_only <- as.Date(dat_use$dates_only, format = "%m/%d/%Y")

# Format date_times to be POSIXct objects
dat_use$date_times <- as.POSIXct(dat_use$date_times, format = "%d-%m-%Y %H:%M:%S")

# Check out structure
str(dat_use)

## 'data.frame':    5 obs. of  2 variables:
##  $ dates_only: Date, format: "2017-12-05" "2017-12-13" ...
##  $ date_times: POSIXct, format: "2017-12-05 05:23:10" "2017-12-13 03:10:45" ...

# Check out data
dat_use

##   dates_only          date_times
## 1 2017-12-05 2017-12-05 05:23:10
## 2 2017-12-13 2017-12-13 03:10:45
## 3 2018-01-09 2018-01-09 14:15:10
## 4 2018-02-15 2018-02-15 19:25:05
## 5 2018-02-21 2018-02-21 08:55:35
```

The package [lubridate](https://cran.r-project.org/web/packages/lubridate/lubridate.pdf) is a wrapper for POSIXct objects and also works for Date objects.

Once lubridate is installed, use library() to make the lubridate functions accessible.

```r
library(lubridate)
```

Note that this masks "date" from the base package, which may not be what you want for certain analyses.

Lubridate is useful for wrangling date data, or extracting data subsets.

For instance, extract months:

```r
# Use month to get months date
month(dat_use$dates_only)

## [1] 12 12  1  2  2
```

or years

```r
# Use year to get years from date
year(dat_use$date_times)

## [1] 2017 2017 2018 2018 2018
```

Another frequently used package is [zoo](https://cran.r-project.org/web/packages/zoo/zoo.pdf), especially in cases of time series data.

```r
library(zoo)
```

Again, we see masking - now as.Date is masked from base!

Zoo is especially useful for working with monthly data.

```r
# Use as.yearmon to get year and month data
as.yearmon(dat_use$dates_only)

## [1] "Dec 2017" "Dec 2017" "Jan 2018" "Feb 2018" "Feb 2018"
```

Other date/time packages include: [chron](https://cran.r-project.org/web/packages/chron/chron.pdf), [timeDate](https://cran.r-project.org/web/packages/timeDate/timeDate.pdf), and [xts](https://cran.r-project.org/web/packages/xts/xts.pdf). What package you'll need depends on what kinds of analysis you're doing and how complex your data are. In most cases, base and lubridate/zoo are sufficient for data wrangling, while other packages are primarily aimed at facilitating time series modeling.

## Additional resrouces

Overview of dates and times in R from [Berkeley stats](https://www.stat.berkeley.edu/%7Es133/dates.html) department

Walk-through of Date, POSIXct, and POSIXlt from [R-bloggers](https://www.r-bloggers.com/using-dates-and-times-in-r/)

[CRAN vignette](https://cran.r-project.org/web/packages/lubridate/vignettes/lubridate.html) about lubridate

RStudio lubridate [cheat sheet](https://www.rstudio.com/resources/cheatsheets/) (scroll to "Dates and Times Cheat Sheet")

Stack Overflow [post](https://stackoverflow.com/questions/10699511/difference-between-as-posixct-as-posixlt-and-strptime-for-converting-character-v) about POSIXct vs POSIXlt

DataCamp xts [cheat sheet](https://www.datacamp.com/community/blog/r-xts-cheat-sheet)

[Post ](http://blog.revolutionanalytics.com/2009/06/converting-time-zones.html)on time zone conversions

[Dealing ](https://stackoverflow.com/questions/8004050/import-date-time-at-a-specified-timezone-disregard-daylights-savings-time?rq=1)with daylight savings [issues](https://stackoverflow.com/questions/37053620/dealing-with-eastern-standard-time-est-and-eastern-daylight-savings-edt-in-r?rq=1)
