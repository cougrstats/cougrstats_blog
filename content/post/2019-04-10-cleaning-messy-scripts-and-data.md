---
title: Cleaning messy scripts and data
author: cougrstats
date: '2019-04-10'
categories:
  - Introduction to R
tags:
  - data formatting
  - janitor
slug: cleaning-messy-scripts-and-data
---

_By Matt Brousil_

The goal of this walkthrough is to look over some methods for cleaning and maintaining data and scripts. This will not be comprehensive for either topic, but contains some tips I've collected.

### Data

Cleaned data is a wonderful thing. There are resources like Data Carpentry to provide crash courses in how to get started in doing data manipulation and management in R. Below are a few additional tips and tricks for cleaning up data that you may not have previously encountered.

**1. Dealing with bad column names.**

The csv below [(download here)](https://drive.google.com/file/d/1uJnprAMsXnD3UjSKF1xtCzuFfQ_1Ohi_/view?usp=sharing) has the following column names in its raw form:

_test date, which group?, value, group*value, "Notes"_

How does R interpret those when read in?

```r
og_csv <- read.csv(file = "bad-header.csv")

og_csv

##    test.date which.group. value group.value                 X.Notes.
## 1      42370            A     1          A1 experimental, greenhouse
## 2      42371            A     5          A5 experimental, greenhouse
## 3      42371            B    75         B75        experimental, lab
## 4         NA            B     4          B4 experimental, greenhouse
## 5         NA            A     2          A2        experimental, lab
## 6      42370            A     1          A1 experimental, greenhouse
## 7      42373            A     1          A1        experimental, lab
## 8      42374            A   544        A544 experimental, greenhouse
## 9      42375            B    45         B45        experimental, lab
## 10     42370            A     1          A1 experimental, greenhouse
##           lat        long
## 1  -27.18648° -109.43542°
## 2  -27.18648° -109.43542°
## 3  -27.18648° -109.43542°
## 4  -27.18648° -109.43542°
## 5  -27.18648° -109.43542°
## 6  -27.18648° -109.43542°
## 7  -27.18351° -109.44268°
## 8  -27.18351° -109.44268°
## 9  -27.18351° -109.44268°
## 10 -27.18351° -109.44268°
```

There is a function working under-the-hood in R to make the crazy names of our csv "valid." This is the function `make.names()`, which is referenced by
`read.csv()` by default. This is what happens if we turn it off:

```r
raw_csv <- read.csv(file = "bad-header.csv", check.names = F)

raw_csv

##    test date which group? value group*value                  "Notes"
## 1      42370            A     1          A1 experimental, greenhouse
## 2      42371            A     5          A5 experimental, greenhouse
## 3      42371            B    75         B75        experimental, lab
## 4         NA            B     4          B4 experimental, greenhouse
## 5         NA            A     2          A2        experimental, lab
## 6      42370            A     1          A1 experimental, greenhouse
## 7      42373            A     1          A1        experimental, lab
## 8      42374            A   544        A544 experimental, greenhouse
## 9      42375            B    45         B45        experimental, lab
## 10     42370            A     1          A1 experimental, greenhouse
##           lat        long
## 1  -27.18648° -109.43542°
## 2  -27.18648° -109.43542°
## 3  -27.18648° -109.43542°
## 4  -27.18648° -109.43542°
## 5  -27.18648° -109.43542°
## 6  -27.18648° -109.43542°
## 7  -27.18351° -109.44268°
## 8  -27.18351° -109.44268°
## 9  -27.18351° -109.44268°
## 10 -27.18351° -109.44268°

str(raw_csv)

## 'data.frame':    10 obs. of  7 variables:
##  $ test date   : int  42370 42371 42371 NA NA 42370 42373 42374 42375 42370
##  $ which group?: Factor w/ 2 levels "A","B": 1 1 2 2 1 1 1 1 2 1
##  $ value       : int  1 5 75 4 2 1 1 544 45 1
##  $ group*value : Factor w/ 7 levels "A1","A2","A5",..: 1 3 7 5 2 1 1 4 6 1
##  $ "Notes"     : Factor w/ 2 levels "experimental, greenhouse",..: 1 1 2 1 2 1 2 1 2 1
##  $ lat         : Factor w/ 2 levels "-27.18351°","-27.18648°": 2 2 2 2 2 2 1 1 1 1
##  $ long        : Factor w/ 2 levels "-109.43542°",..: 1 1 1 1 1 1 2 2 2 2
```

If we want to start referencing those column names in our code it gets trickier, as we need to start quoting:

    raw_csv
    <em>By Matt Brousil</em>

    The goal of this walkthrough is to look over some methods for cleaning and maintaining data and scripts. This will not be comprehensive for either topic, but contains some tips I've collected.

    <h3>Data</h3>

    Cleaned data is a wonderful thing. There are resources like Data Carpentry to provide crash courses in how to get started in doing data manipulation and management in R. Below are a few additional tips and tricks for cleaning up data that you may not have previously encountered.

    <strong>1. Dealing with bad column names.</strong>

    The csv below <a href="https://drive.google.com/file/d/1uJnprAMsXnD3UjSKF1xtCzuFfQ_1Ohi_/view?usp=sharing">(download here)</a> has the following column names in its raw form:

    <em>test date, which group?, value, group*value, "Notes"</em>

    How does R interpret those when read in?

    og_csv <- read.csv(file = "bad-header.csv")

    og_csv

    ##    test.date which.group. value group.value                 X.Notes.
    ## 1      42370            A     1          A1 experimental, greenhouse
    ## 2      42371            A     5          A5 experimental, greenhouse
    ## 3      42371            B    75         B75        experimental, lab
    ## 4         NA            B     4          B4 experimental, greenhouse
    ## 5         NA            A     2          A2        experimental, lab
    ## 6      42370            A     1          A1 experimental, greenhouse
    ## 7      42373            A     1          A1        experimental, lab
    ## 8      42374            A   544        A544 experimental, greenhouse
    ## 9      42375            B    45         B45        experimental, lab
    ## 10     42370            A     1          A1 experimental, greenhouse
    ##           lat        long
    ## 1  -27.18648° -109.43542°
    ## 2  -27.18648° -109.43542°
    ## 3  -27.18648° -109.43542°
    ## 4  -27.18648° -109.43542°
    ## 5  -27.18648° -109.43542°
    ## 6  -27.18648° -109.43542°
    ## 7  -27.18351° -109.44268°
    ## 8  -27.18351° -109.44268°
    ## 9  -27.18351° -109.44268°
    ## 10 -27.18351° -109.44268°

There is a function working under-the-hood in R to make the crazy names of our csv "valid." This is the function `make.names()`, which is referenced by
`read.csv()` by default. This is what happens if we turn it off:

```r
raw_csv <- read.csv(file = "bad-header.csv", check.names = F)

raw_csv

##    test date which group? value group*value                  "Notes"
## 1      42370            A     1          A1 experimental, greenhouse
## 2      42371            A     5          A5 experimental, greenhouse
## 3      42371            B    75         B75        experimental, lab
## 4         NA            B     4          B4 experimental, greenhouse
## 5         NA            A     2          A2        experimental, lab
## 6      42370            A     1          A1 experimental, greenhouse
## 7      42373            A     1          A1        experimental, lab
## 8      42374            A   544        A544 experimental, greenhouse
## 9      42375            B    45         B45        experimental, lab
## 10     42370            A     1          A1 experimental, greenhouse
##           lat        long
## 1  -27.18648° -109.43542°
## 2  -27.18648° -109.43542°
## 3  -27.18648° -109.43542°
## 4  -27.18648° -109.43542°
## 5  -27.18648° -109.43542°
## 6  -27.18648° -109.43542°
## 7  -27.18351° -109.44268°
## 8  -27.18351° -109.44268°
## 9  -27.18351° -109.44268°
## 10 -27.18351° -109.44268°

str(raw_csv)

## 'data.frame':    10 obs. of  7 variables:
##  $ test date   : int  42370 42371 42371 NA NA 42370 42373 42374 42375 42370
##  $ which group?: Factor w/ 2 levels "A","B": 1 1 2 2 1 1 1 1 2 1
##  $ value       : int  1 5 75 4 2 1 1 544 45 1
##  $ group*value : Factor w/ 7 levels "A1","A2","A5",..: 1 3 7 5 2 1 1 4 6 1
##  $ "Notes"     : Factor w/ 2 levels "experimental, greenhouse",..: 1 1 2 1 2 1 2 1 2 1
##  $ lat         : Factor w/ 2 levels "-27.18351°","-27.18648°": 2 2 2 2 2 2 1 1 1 1
##  $ long        : Factor w/ 2 levels "-109.43542°",..: 1 1 1 1 1 1 2 2 2 2
```

If we want to start referencing those column names in our code it gets trickier, as we need to start quoting:

which group?`
`

```r
##  [1] A A B B A A A A B A
## Levels: A B
```

There are a couple of ways to go about cleaning up the names of a messy file. We can use `make.names()` as described above, which requires a **vector** of names as input. Alternatively, we can use `clean_names()` from the `janitor` package.
`clean_names()` will take a **data frame** directly and return a new data frame with tidy-looking names.

```r
make.names(names(raw_csv))

## [1] "test.date"    "which.group." "value"        "group.value"
## [5] "X.Notes."     "lat"          "long"

clean_names(raw_csv) %>% names()

## [1] "test_date"   "which_group" "value"       "group_value" "notes"
## [6] "lat"         "long"
```

It also has a lot of options for changing case.

```r
clean_names(raw_csv, case = "upper_camel") %>% names()

## [1] "TestDate"   "WhichGroup" "Value"      "GroupValue" "Notes"
## [6] "Lat"        "Long"
```

We'll keep the tidier format:

```r
raw_csv <- clean_names(raw_csv)
```

**2. One person's Excel dates are another person's usable data**

Working with dates can be difficult at times, especially when importing them from Excel. In some cases you will read in date data from Excel and find that your dates have been converted to serial numbers such as this:

```r
raw_csv$test_date

##  [1] 42370 42371 42371    NA    NA 42370 42373 42374 42375 42370
```

Here the `janitor` package is useful once again: We can use
`excel_numeric_to_date()` to convert these to dates we can use. Note that they must be `numeric`.

```r
excel_numeric_to_date(as.numeric(raw_csv$test_date))

##  [1] "2016-01-01" "2016-01-02" "2016-01-02" NA           NA
##  [6] "2016-01-01" "2016-01-04" "2016-01-05" "2016-01-06" "2016-01-01"

raw_csv$test_date <- excel_numeric_to_date(as.numeric(raw_csv$test_date))
```

**3. Fill in NA values in a sequence of data**

If you've ever entered data collected by hand, it isn't difficult to imagine a situation where someone skips filling in rows that have identical data. For example, we might know that the NA values in the date column below aren't truly unknown. Perhaps our lab technician just didn't want to write the same date over and over again.

```r
raw_csv

##     test_date which_group value group_value                    notes
## 1  2016-01-01           A     1          A1 experimental, greenhouse
## 2  2016-01-02           A     5          A5 experimental, greenhouse
## 3  2016-01-02           B    75         B75        experimental, lab
## 4                   B     4          B4 experimental, greenhouse
## 5                   A     2          A2        experimental, lab
## 6  2016-01-01           A     1          A1 experimental, greenhouse
## 7  2016-01-04           A     1          A1        experimental, lab
## 8  2016-01-05           A   544        A544 experimental, greenhouse
## 9  2016-01-06           B    45         B45        experimental, lab
## 10 2016-01-01           A     1          A1 experimental, greenhouse
##           lat        long
## 1  -27.18648° -109.43542°
## 2  -27.18648° -109.43542°
## 3  -27.18648° -109.43542°
## 4  -27.18648° -109.43542°
## 5  -27.18648° -109.43542°
## 6  -27.18648° -109.43542°
## 7  -27.18351° -109.44268°
## 8  -27.18351° -109.44268°
## 9  -27.18351° -109.44268°
## 10 -27.18351° -109.44268°
```

In this case we can use the function `na.locf()` in the `zoo` package **or** the `fill()` function in `tidyr`. Both of these functions will fill in missing values in a data frame by moving either forward or backward through its values.

```r
na.locf(object = raw_csv$test_date)

##  [1] "2016-01-01" "2016-01-02" "2016-01-02" "2016-01-02" "2016-01-02"
##  [6] "2016-01-01" "2016-01-04" "2016-01-05" "2016-01-06" "2016-01-01"
```

`fill()` is more suited to working directly with a data frame:

```r
fill(data = raw_csv, test_date)

##     test_date which_group value group_value                    notes
## 1  2016-01-01           A     1          A1 experimental, greenhouse
## 2  2016-01-02           A     5          A5 experimental, greenhouse
## 3  2016-01-02           B    75         B75        experimental, lab
## 4  2016-01-02           B     4          B4 experimental, greenhouse
## 5  2016-01-02           A     2          A2        experimental, lab
## 6  2016-01-01           A     1          A1 experimental, greenhouse
## 7  2016-01-04           A     1          A1        experimental, lab
## 8  2016-01-05           A   544        A544 experimental, greenhouse
## 9  2016-01-06           B    45         B45        experimental, lab
## 10 2016-01-01           A     1          A1 experimental, greenhouse
##           lat        long
## 1  -27.18648° -109.43542°
## 2  -27.18648° -109.43542°
## 3  -27.18648° -109.43542°
## 4  -27.18648° -109.43542°
## 5  -27.18648° -109.43542°
## 6  -27.18648° -109.43542°
## 7  -27.18351° -109.44268°
## 8  -27.18351° -109.44268°
## 9  -27.18351° -109.44268°
## 10 -27.18351° -109.44268°
```

**4. Working with duplicate data**

There are multiple ways to get duplicate rows from a data frame in R. `get_dupes()` from `janitor` is straightforward. It also appends a new column to your input data frame called dupe_count that indicates the number of rows duplicated for each unique record.

```r
get_dupes(raw_csv)

## No variable names specified - using all columns.

## # A tibble: 2 x 8
##   test_date  which_group value group_value notes    lat    long  dupe_count
##
## 1 2016-01-01 A               1 A1          experim~ -27.1~ -109~          2
## 2 2016-01-01 A               1 A1          experim~ -27.1~ -109~          2
```

We can also do something similar in base R using `duplicated()`. However, it has fewer bells and whistles. We can see which rows are duplicates:

```r
duplicated(raw_csv)

##  [1] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE FALSE
```

Note that this includes one less duplicate than `get_dupes()`. This function doesn't count the first entry as a duplicate, only the repeats.

```r
raw_csv[duplicated(raw_csv), ]

##    test_date which_group value group_value                    notes
## 6 2016-01-01           A     1          A1 experimental, greenhouse
##          lat        long
## 6 -27.18648° -109.43542°
```

**5. Splitting rows based on a delimited value**

You may run into a situation where you have a variable that has multiple values within each of its rows. Perhaps this is a "Notes" column, for example. Depending on the situation you'll either want to put these in their own rows or columns. That is doable using `separate()` or `separate_rows()` from tidyr.

Use `separate()` to create new columns. We can specify the new column names with `into`.

```r
separate(data = raw_csv, col = notes, into = c("type", "location"), sep = ", ")

##     test_date which_group value group_value         type   location
## 1  2016-01-01           A     1          A1 experimental greenhouse
## 2  2016-01-02           A     5          A5 experimental greenhouse
## 3  2016-01-02           B    75         B75 experimental        lab
## 4                   B     4          B4 experimental greenhouse
## 5                   A     2          A2 experimental        lab
## 6  2016-01-01           A     1          A1 experimental greenhouse
## 7  2016-01-04           A     1          A1 experimental        lab
## 8  2016-01-05           A   544        A544 experimental greenhouse
## 9  2016-01-06           B    45         B45 experimental        lab
## 10 2016-01-01           A     1          A1 experimental greenhouse
##           lat        long
## 1  -27.18648° -109.43542°
## 2  -27.18648° -109.43542°
## 3  -27.18648° -109.43542°
## 4  -27.18648° -109.43542°
## 5  -27.18648° -109.43542°
## 6  -27.18648° -109.43542°
## 7  -27.18351° -109.44268°
## 8  -27.18351° -109.44268°
## 9  -27.18351° -109.44268°
## 10 -27.18351° -109.44268°
```

Alternatively, you can use `separate_rows()` to create new rows from the data instead.

```r
separate_rows(data = raw_csv, notes, sep = ", ") %>% head()

##    test_date which_group value group_value        notes        lat
## 1 2016-01-01           A     1          A1 experimental -27.18648°
## 2 2016-01-01           A     1          A1   greenhouse -27.18648°
## 3 2016-01-02           A     5          A5 experimental -27.18648°
## 4 2016-01-02           A     5          A5   greenhouse -27.18648°
## 5 2016-01-02           B    75         B75 experimental -27.18648°
## 6 2016-01-02           B    75         B75          lab -27.18648°
##          long
## 1 -109.43542°
## 2 -109.43542°
## 3 -109.43542°
## 4 -109.43542°
## 5 -109.43542°
## 6 -109.43542°
```

### Scripts

So now your data is beautiful. But your script isn't! It is easy to treat a script as something that only needs to run, and doesn't need to be polished. Often this will work, too. We can write scripts that may be hard to read but will run if we ask them.

If you're trying to make a reproducible analysis a script won't be very useful for the next user if they can't interpret it.

One way to ensure some readability in scripts is to follow a style guide. For example, the tidyverse provides one here: https://style.tidyverse.org/

This style guide goes into many specifics, which I won't rewrite here, but for example:

**Names of objects should use underscores, not periods.**

```r
hour_sequence <- seq(from = 1, to = 24, by = 1)

# NOT

hour.sequence <- seq(from = 1, to = 24, by = 1)
```

**Operators should typically have spaces on either side.**

```r
filter(iris, Sepal.Width >= 3)

# NOT

filter(iris, Sepal.Width>=3)
```

**Long lines (> 80 characters) are bad news.** Avoid letting the code run longer than this on one line.

```r
iris %>%
  filter(Sepal.Width >= 3) %>%
  select(Sepal.Width, Species) %>%
  group_by(Species) %>%
  summarise(mean = mean(Sepal.Width))

# NOT

iris %>% filter(Sepal.Width >= 3) %>% select(Sepal.Width, Species) %>% group_by(Species) %>% summarise(mean = mean(Sepal.Width))
```

Despite your best efforts you may find yourself missing some of the style points once you've finished a script. Have no fear! You can use the `lintr` package to check your script for style automatically.

```r
lint("example_script.R")
```

Where "example_script.R" looks like

```r
#This is an example script with some messy code

iris.sepal=iris %>% select(Sepal.Length, Sepal.Width, Species)

iris.petal.means <- iris %>% select(Petal.Length, Petal.Width, Species) %>% group_by(Species) %>% summarise(mean=mean(Petal.Length))
```

and the lintr output is

![](lintr-output.jpg)![lintr-output](https://cougrstats.files.wordpress.com/2020/01/lintr-output.jpg)

If you have specific aspects of style that you'd like to check, you can specify specific linters from within the `lint()` call. Available linters can be viewed using `?linters()`

#### Sources:

<https://style.tidyverse.org/index.html>
