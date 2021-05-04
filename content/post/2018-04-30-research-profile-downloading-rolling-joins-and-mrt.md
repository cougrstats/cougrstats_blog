---
title: 'Research Profile: Downloading, Rolling Joins, and MRT'
author: cougrstats
date: '2018-04-30'
categories:
  - Research Profiles
tags:
  - date/time
  - downloader
  - MRT
  - multivariate
  - species
  - vegan
slug: research-profile-downloading-rolling-joins-and-mrt
---


```r
library(tidyverse)
library(dplyr)
library(data.table)
library(mvpart)
library(vegan)

#setwd("C:/Users/Stefanie/Documents/WSU/rGroup") #set working directory
```

### _Author: Stefanie Watson_

## Getting Data

_You can download the species subset for this research profile [here](https://s3.wp.wsu.edu/uploads/sites/95/2018/04/speciesSub.csv). Other data is downloaded from Canada using the downloader package. _

The environmental data that we are using is all freely available through the national data buoy center. First, you have to download the zipped file to the correct location (use mode 'wb' to download correctly). The URL should be one that you can copy/paste into your address bar and will immediately start a download. In this case, this was not the same as the URL displayed in the address bar. I had to hover my mouse over the download to get the correct URl for Windows 10. You will know you have the correct URL when you put it into the address bar and it immediately starts a download instead of taking you to a webpage. Then, you have to unzip the file into a folder and read the csv into R. I have used locations on my computer, but you can create a temp file if you are unsure where to save.

I have also included a 50 observation subset of species data to work with later.

```r
#download the buoy data directly from Canada using downloader package
download("http://www.meds-sdmm.dfo-mpo.gc.ca/alphapro/wave/waveshare/csvData/C46132_CSV.ZIP", dest="dataset.zip", mode="wb")

#unzip the file to be able to read in the csv
unzip("dataset.zip")

buoy <- read_csv("C46132.csv")

## Parsed with column specification:
## cols(
##   .default = col_double(),
##   STN_ID = col_character(),
##   DATE = col_character(),
##   Q_FLAG = col_integer(),
##   X24 = col_character()
## )

## See spec(...) for full column specifications.

head(buoy)

## # A tibble: 6 x 24
##   STN_ID DATE     Q_FLAG LATITUDE LONGITUDE DEPTH  VCAR  VTPK `VWH$`  VCMX
##   <chr>  <chr>     <int>    <dbl>     <dbl> <dbl> <dbl> <dbl>  <dbl> <dbl>
## 1 C46132 05/05/1~      7     49.7      128.  2040  0    12.2     1.5   2.4
## 2 C46132 05/06/1~      7     49.7      128.  2040  0    28.4     1.8   3.6
## 3 C46132 05/07/1~      7     49.7      128.  2040  0.12 11.1     2.6   0
## 4 C46132 05/07/1~      7     49.7      128.  2040  0    12.2     2.6   4.7
## 5 C46132 05/08/1~      7     49.7      128.  2040  0    12.2     1.7   3
## 6 C46132 06/01/1~      7     49.7      128.  2040  0     4.27    3.8   5.9
## # ... with 14 more variables: `VTP$` <dbl>, WDIR <dbl>, WSPD <dbl>,
## #   `WSS$` <dbl>, GSPD <dbl>, WDIR_1 <dbl>, WSPD_1 <dbl>, `WSS$_1` <dbl>,
## #   GSPD_1 <dbl>, ATMS <dbl>, ATMS_1 <dbl>, DRYT <dbl>, SSTP <dbl>,
## #   X24 <chr>

species <- read_csv("speciesSub.csv")

## Parsed with column specification:
## cols(
##   Time = col_datetime(format = ""),
##   species1 = col_integer(),
##   species2 = col_integer(),
##   species3 = col_integer(),
##   species4 = col_integer(),
##   species5 = col_integer()
## )

head(species)

## # A tibble: 6 x 6
##   Time                species1 species2 species3 species4 species5
##   <dttm>                 <int>    <int>    <int>    <int>    <int>
## 1 2014-07-04 06:30:00        1        0        2       11        0
## 2 2015-02-23 04:30:00        0        1        1        0        2
## 3 2014-06-13 00:30:00        0        0        2        8        1
## 4 2015-02-15 08:30:00        1        0        0        1        0
## 5 2014-08-04 07:30:00        1        0        0       24        0
## 6 2014-07-16 09:30:00        0        0        1       24        0
```

## Date/Times and Rolling Joins

The environmental data is a mess right now. We only need the dates that span our study and only want to use a few of the variables. We need to clean up the date/time formatting and then we can focus on subsetting this data to our needs.

Note: You may need to change the species timestamp to POSIXct if you opened it in excel.

```r
#convert to standard date/time format: this is important for if they are in the wrong format
buoy$DATE <- strptime(buoy$DATE, '%m/%d/%Y %H:%M')
head(buoy$DATE)

## [1] "1994-05-05 19:41:00 PDT" "1994-05-06 10:41:00 PDT"
## [3] "1994-05-07 09:41:00 PDT" "1994-05-07 16:41:00 PDT"
## [5] "1994-05-08 19:41:00 PDT" "1994-06-01 08:42:00 PDT"

#convert to Posixct
buoy$DATE <- as.POSIXct(buoy$DATE)

#subset the buoy data
#Below is my attempt to fix a variable name ending in $
#It didnt work and messed up the dataset more than it helped, any ideas are welcome
#buoy$VWHB <- buoy[,9]

buoy <- buoy %>%
  filter(DATE >= as.POSIXct('2014-06-04 00:00:00 PDT') &
                    DATE <= as.POSIXct('2015-04-08 00:00:00 PDT')) %>%
  select(DATE, WSPD, GSPD, ATMS, SSTP)
```

We can now use rolling joins to match the species information with the correct times in the bouy data. You will want to use a join when matching data. The functions rbind and cbind require that your data is already ordered and will append regardless of whether the observations match. Usually this is fine, but for disjoint datasets you should use joins. A join will match two datasets by a common key. You have to specify the key as a unique identifier for each observation (typically an ID, but here I use timestamps). You will probably mostly use left/right joins to fill a dataset. However, in these joins the keys must match exactly. Here, I have timestamps taken at different minutes that I want to match. I use a rolling join which matches to the nearest time. I have also specified that it has to match to past measurements and that the measurement must be within an hour of the image.

```r
#We need each dataset to have a key
buoy <- data.table(buoy, key = "DATE")
species <- data.table(species, key = "Time")

#match to nearest
#create a condition to 1 hour
hour <- 60*60*1 # 1 hour = 60sec * 60min * 1 hour
mergeData <-buoy[species, roll = -hour]
mergeData <- na.omit(mergeData)
```

## Multivariate Regression Trees

This is a summary of how to use the 'mvpart' package in R as first described by De/'Ath (2002). This is only available directly from GitHub so make sure that you have it downloaded correctly. There are tutorials online on how to do so.

The first thing that I need to do is make sure that I have my data in order from above. My two data sets need to be bound and any transformations need to be done beforehand.

```r
#transform species data: sqrt for poisson and wisconsin for natural species variation
mergeData[,6:10] <- mergeData[,6:10] %>%
  sqrt() %>%
  wisconsin()

head(mergeData)

##                   DATE WSPD GSPD   ATMS SSTP species1  species2  species3
## 1: 2014-06-05 04:30:00 10.6 12.6 1023.9 10.7        0 0.0000000 0.3865505
## 2: 2014-06-05 08:30:00 11.5 13.4 1023.2 10.4        0 0.0000000 0.6475296
## 3: 2014-06-07 05:30:00  5.4  6.6 1022.7 11.9        0 0.3095295 0.4377408
## 4: 2014-06-08 06:30:00  3.4  3.9 1024.0 12.3        0 0.4046282 0.4046282
## 5: 2014-06-10 13:30:00  6.9  8.3 1020.6 12.5        0 0.0000000 0.6216661
## 6: 2014-06-13 00:30:00  8.9 10.8 1010.5 13.4        0 0.0000000 0.3610369
##     species4  species5
## 1: 0.6134495 0.0000000
## 2: 0.3524704 0.0000000
## 3: 0.2527298 0.0000000
## 4: 0.1907436 0.0000000
## 5: 0.3783339 0.0000000
## 6: 0.2779263 0.3610369
```

Now we can make our first MRT. The first one that we are making is based on Euclidean distance and is prodiced by R. By default, R chooses the smallest tree within one standard error of the tree with the minimum cross-validated relative error. Using the summary function gives us more information about each of the nodes and leaves.

```r
#tree pruned by R
comp <- mvpart(data.matrix(mergeData[,6:10])~WSPD+GSPD+ATMS+SSTP, mergeData)
```

![plot of chunk createMRT](http://cougrstats.files.wordpress.com/2018/04/createmrt-1.png)

```r
summary(comp)

## Call:
## mvpart(form = data.matrix(mergeData[, 6:10]) ~ WSPD + GSPD +
##     ATMS + SSTP, data = mergeData)
##   n= 41
##
##          CP nsplit rel error   xerror      xstd
## 1 0.1308952      0 1.0000000 1.040219 0.1040792
## 2 0.1036941      1 0.8691048 1.141133 0.1384589
##
## Node number 1: 41 observations,    complexity param=0.1308952
##   Means=0.2009,0.1068,0.2581,0.3345,0.02654, Summed MSE=0.1969636
##   left son=2 (11 obs) right son=3 (30 obs)
##   Primary splits:
##       SSTP < 10.95   to the left,  improve=0.13089520, (0 missing)
##       WSPD < 5.45    to the right, improve=0.07554495, (0 missing)
##       GSPD < 6.25    to the left,  improve=0.06469340, (0 missing)
##       ATMS < 1002.65 to the right, improve=0.06151302, (0 missing)
##
## Node number 2: 11 observations
##   Means=0.1091,0.09661,0.4648,0.1973,0.04119, Summed MSE=0.2353352
##
## Node number 3: 30 observations
##   Means=0.2346,0.1106,0.1822,0.3848,0.02117, Summed MSE=0.1476592
```

This MRT has 2 leaves and 3 nodes. Node 1 is a split and nodes 2-3 are leaves. The bar charts by each leaf show the average species count during that condition and gives the number of observations in that condition (n=##). The relative error is reported at the bottom. The equation to find the amount of variance the tree can explain is 1 - relative error. In this case it is 1 - 0.869 = 13.1% of the variance. The complexity param of the summary gives the amount of variance explained by each split in the tree. In this case there is only one split, so all of the variance is explained by that split.

If we want to then we can prune the tree ourselves. R will give us an interactive relative error chart from which to select a tree size. The chart is static in this RMarkdown, but you can select a blue node to view the different tree sizes when the plot is live. RMarkDown has seen fit to select all of the trees for us and plot them overlapping below. This will not happen live.

```r
mvpart(data.matrix(mergeData[,6:10])~WSPD+GSPD+ATMS+SSTP, mergeData, xv="p")
```

![plot of chunk selfPrune](http://cougrstats.files.wordpress.com/2018/04/selfprune-1.png)![plot of chunk selfPrune](http://cougrstats.files.wordpress.com/2018/04/selfprune-2.png)

Finally, we can produce a summary of each of the leaves and conditions within our tree.

```r
#To obtain the path to the leaf nodes

#searches frame for info on leaves and identifies leaves by bool
leafnodeRows <- grepl("leaf",comp$frame$var)

#determine the leaf position
nodevals <- as.numeric(rownames(comp$frame)[leafnodeRows])

#creates a list of rules taken from each node identified as a leaf
rules <- path.rpart(comp,nodevals)

##
##  node number: 2
##    root
##    SSTP< 10.95
##
##  node number: 3
##    root
##    SSTP>=10.95

#creates a nice dataframe of the rules by formatting and casting
rulesdf <- do.call("rbind",lapply(rules,function(x)paste(x,collapse = " -AND- ")))
rulesdf <- data.frame(nodeNumber=rownames(rulesdf),rule=rulesdf[,1],stringsAsFactors=FALSE)
rulesdf

##   nodeNumber                   rule
## 2          2 root -AND- SSTP< 10.95
## 3          3 root -AND- SSTP>=10.95
```
