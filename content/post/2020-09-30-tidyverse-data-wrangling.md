---
title: Tidyverse Data Wrangling
author: Ben Leonard
date: '2020-09-30'
tags:
  - data wrangling
  - tidyverse
slug: tidyverse-data-wrangling
---

_By Ben Leonard_

## What is Data Wrangling?

Most of the time datasets will not come "out of the box" ready to use for analysis. Summarizing data and presenting audience friendly tables and figures requires quite a bit of data manipulation. A data wrangling task is performed anytime a dataset is cleaned, tweaked, or adjusted to fit a subsequent analytical step.

## Why Use R?

Programs that provide an easy to use graphical user interface (GUI) such as Excel can be used to perform data wrangling tasks. Since it can be faster to manipulate data is Excel why should anyone take extra time to write code in R?

  1. **Repeatability.** A cornerstone of the scientific process is producing a replicable result. If a dataset has to be heavily massaged to produce the desired result these steps must be documented. Otherwise it is easy for errors to creep into the final output. Without transparency it is difficult for reviewers to differentiate between honest mistakes and purposeful data fabrication. It is also difficult to perform any type of quality assurance protocol without proper documentation. By coding all analytical steps in R it is actually easier to leave a trail of evidence showing data wrangling steps than trying to do so in Excel by heavily annotating workbooks.

  2. **Data Integrity.** Excel often does unexpected things to data. For example, Excel will attempt to auto-recognize data types when entering data. If I try to enter the value "1-15" this automatically becomes the date "January 15, 2020". Excel also does not always respect the preservation and display of significant digits. Some formulas don't follow sounds statistical philosophy. Many advanced data maneuvers are absent from or really difficult to perform in Excel.

  3. **Work Flow.** If R is required eventually for statistics, modeling, rmarkdown, shiny, etc. then keeping all steps "in house" just makes sense. Since R and RStudio provide most of the tools a data scientist needs why muddy the waters by switching back and forth with Excel. However, it should be noted that there are many packages that make it easy to integrate the two approaches. For example, _readxl_ is a tidyverse package for reading Excel workbooks. It is also possible to code Excel procedures using Visual Basic for Applications (VBA) code and then programmatically execute this code in R. Many choose a hybrid approach in which Excel is used as a data exploration tool that can be used to figure out which steps need to be taken to accomplish a task in R.

## Tidyverse Packages

```r
# Installing tidyverse packages
# install.packages("tidyverse")

# Loading tidyverse packages
# library("tidyverse")

# Tidyverse information
# ?tidyverse
```

<https://www.tidyverse.org/>
<blockquote>
The tidyverse is an opinionated collection of R packages designed for data science. All packages share an underlying design philosophy, grammar, and data structures.

Install the complete tidyverse with:

install.packages("tidyverse")
</blockquote>

Loading the _tidyverse_ library is a great way to load many useful packages in one simple step. Several packages included in this distribution are great tools for data wrangling. Notably _dplyr_, _readr_, and _tidyr_ are critical assets. The general philosophy is that if a number of steps are needed for a data wrangling task these can be modularized into a stream-lined set into a human readable commands.

<https://dplyr.tidyverse.org/>

<https://readr.tidyverse.org/>

<https://tidyr.tidyverse.org/>

### Criticism

Some argue that tidyverse syntax is not intuitive and that it should not be taught to students first learning R. Much of the basis for this comes from the avoidance of certain base R staples such as the "$" operator, "[[]]", loops, and the plot command.

<https://github.com/matloff/TidyverseSkeptic>

## Pipe Operator

"%>%"

The pipe operator is the crux of all tidyverse data operations. It strings together multiple functions without the need for subsetting. If a number of operations are needed to be performed on a single dataframe this approach simplifies the process. The following image shows the mathematical principle of how the pipe operator works by bridging functions with explicitly subsetting arguments. In this case, steps A %>% B %>% C would represent the tidyverse "pipe syntax" while f(g(x)) is the base R approach.

![](https://res.cloudinary.com/dyd911kmh/image/upload/f_auto,q_auto:best/v1510846626/Pipe-Mathematical_gczmab.png)

The examples below show how to perform a few simple tasks in both base R and tidyverse "pipe syntax". Note that for both of these cases the base R syntax may actually be preferred in terms of brevity, but the tidyverse approaches are slightly more readable.

```r
## Task #1: Determine the mean of a vector of three doubles.

# Create a vector of values
a <- c(12.25, 42.50, 75.00)

# Base R
round(mean(a), digits = 2)

## [1] 43.25

# Tidyverse
a %>%
  mean() %>%
  round(digits = 2)

## [1] 43.25

## Task #2: Extract the unique names of all storms in the "storms" dataset and view the first few results.

# Base R
head(unique(storms$name))

## [1] "Amy"      "Caroline" "Doris"    "Belle"    "Gloria"   "Anita"

# Tidyverse
storms %>%
  pull(name) %>%
  unique() %>%
  head()

## [1] "Amy"      "Caroline" "Doris"    "Belle"    "Gloria"   "Anita"
```

## Reading Data

_read_csv()_ and _write_csv()_

While base R does provide analogous functions (read.csv, and write.csv) the versions included in readr are 5 to 10 times faster. This speed, in addition to a loading bar, makes these functions preferred for large files. The dataframes produced are also always tibbles and don't convert columns to factors or use rownames by default. Additionally, read_csv is able to make better determinations about data types and has more sensible defaults.

The example below shows how to read.csv is unable to identify time series data automatically and assigns a column class of "character". However, read_csv correctly reads in the data without having to specify any column data types.

```r
## Task #1: Read in a dataset of time series data and determine the default class assignments for each column data type.

# Base R
sapply(read.csv("weather.csv"), class)

##   timestamp       value
## "character"   "numeric"

# Tidyverse
read_csv("weather.csv") %>%
  sapply(class)

## Parsed with column specification:
## cols(
##   timestamp = col_datetime(format = ""),
##   value = col_double()
## )

## $timestamp
## [1] "POSIXct" "POSIXt"
##
## $value
## [1] "numeric"
```

_tribble()_

Sometimes it is necessary to define a small dataframe in your code rather than reading data from an external source such as a csv file. The _tribble()_ function makes this very easy by allowing row-wise definition of dataframes in tibble format.

**Note.** A tibble is a type of dataframe specific to the tidyverse. See the following description:

<blockquote>
A tibble, or tbl_df, is a modern reimagining of the data.frame, keeping what time has proven to be effective, and throwing out what is not. Tibbles are data.frames that are lazy and surly: they do less (i.e. they don't change variable names or types, and don't do partial matching) and complain more (e.g. when a variable does not exist). This forces you to confront problems earlier, typically leading to cleaner, more expressive code. Tibbles also have an enhanced print() method which makes them easier to use with large datasets containing complex objects.
</blockquote>

<https://tibble.tidyverse.org/>

The example below shows how much more intuitive it is to create data frames using tribble. Row-wise definitions make it simple to enter tabular data and manually update datasets when need be. The use of tribble also guarantees a tibble output which is then going to be fully compatible with all tidyverse functions. A tibble is also achieved without row-wise syntax using _tibble()_ (formerly _data_frame()_).

```r
## Task #2: Manually create a data frame.

# Base R
class(data.frame("col1" = c(0.251, 2.253),
                 "col2" = c(1.231, 5.230)))

## [1] "data.frame"

# Tidyverse #1
class(tibble("col1" = c(0.251, 2.253),
             "col2" = c(1.231, 5.230)))

## [1] "tbl_df"     "tbl"        "data.frame"

# Tidyverse #2
tribble(
  ~col1, ~col2,
  0.251, 1.231,
  2.253, 5.230,
  1.295, 3.192, # New Data
  ) %>%
  class()

## [1] "tbl_df"     "tbl"        "data.frame"
```

## Manipulating Data

Much of data wrangling comes down to data manipulations performed over and over again. A compact set of functions make this easy in tidyverse without having to nest functions or define a bunch of different variables. While many base R equivalents exist the example below performs a set of commands using only tidyverse syntax.

_select()_ extracts columns and returns a tibble.

_arrange()_ changes the ordering of the rows.

_filter()_ picks cases based on their values.

_mutate()_ adds new variables that are functions of existing variables.

_rename()_ easily changes the name of a column(s)

_pull()_ extracts a single column as a vector.

```r
# Task #1: Perform numerous data manipulation operations on a dataset.

ToothGrowth %>%
  mutate(dose2x = dose*2) %>% # Double the value of dose
  select(-dose) %>% # Remove old dose column
  arrange(-len) %>% # Sort length from high to low
  filter(supp == "OJ") %>% # Filter for only orange juice supplement
  rename(length = len) %>% # Rename len to be more explicit
  pull(length) %>% # Extract length as a vector
  head()

## [1] 30.9 29.4 27.3 27.3 26.4 26.4
```

## Summarizing Data

_group_by()_ Most data operations are done on groups defined by variables. _group_by()_ takes an existing tbl and converts it into a grouped tbl where operations are performed "by group". _ungroup()_ removes grouping.

_summarize()_ creates a new data frame. It will have one (or more) rows for each combination of grouping variables; if there are no grouping variables, the output will have a single row summarising all observations in the input. It will contain one column for each grouping variable and one column for each of the summary statistics that you have specified.

_summarise() and summarize() are synonyms._

_pivot_wider()_ "widens" data, increasing the number of columns and decreasing the number of rows.

_pivot_longer()_ "lengthens" data, increasing the number of rows and decreasing the number of columns.

Data summarization often requires some difficult maneuvering. Since data summaries may then be used for subsequent analyses and may even be used as a deliverable it is important to have a well documented and clear set of procedures. The following procedures are used to create tabular data summaries much like pivot tables in Excel. However, unlike pivot tables in Excel the steps here are well documented.

```r
## Task #1: Summarize the prices of various diamond cuts using a variety of statistical measures and then properly format the results.

diamonds %>%
  group_by(cut) %>%
  summarize(mean = mean(price)) %>%
  mutate(mean = dollar(mean))

## `summarise()` ungrouping output (override with `.groups` argument)

## # A tibble: 5 x 2
##   cut       mean
##   <ord>     <chr>
## 1 Fair      $4,358.76
## 2 Good      $3,928.86
## 3 Very Good $3,981.76
## 4 Premium   $4,584.26
## 5 Ideal     $3,457.54

# Tip: Using _at will apply one or more functions to one or more variables.
diamonds %>%
  group_by(cut) %>%
  summarize_at(vars(price), funs(mean, sd, min, median, max)) %>%
  mutate_at(vars(-cut), dollar)

## Warning: `funs()` is deprecated as of dplyr 0.8.0.
## Please use a list of either functions or lambdas:
##
##   # Simple named list:
##   list(mean = mean, median = median)
##
##   # Auto named with `tibble::lst()`:
##   tibble::lst(mean, median)
##
##   # Using lambdas
##   list(~ mean(., trim = .2), ~ median(., na.rm = TRUE))
## This warning is displayed once every 8 hours.
## Call `lifecycle::last_warnings()` to see where this warning was generated.

## # A tibble: 5 x 6
##   cut       mean      sd        min   median    max
##   <ord>     <chr>     <chr>     <chr> <chr>     <chr>
## 1 Fair      $4,358.76 $3,560.39 $337  $3,282.00 $18,574
## 2 Good      $3,928.86 $3,681.59 $327  $3,050.50 $18,788
## 3 Very Good $3,981.76 $3,935.86 $336  $2,648.00 $18,818
## 4 Premium   $4,584.26 $4,349.20 $326  $3,185.00 $18,823
## 5 Ideal     $3,457.54 $3,808.40 $326  $1,810.00 $18,806

## Task #2: a) Create a presence absence table for fish encounters where each station is a different column. b) Then condense the table to get a total fish counts per station.

# a)
df <- fish_encounters %>%
  mutate(seen = "X") %>% # Set value to X for seen
  pivot_wider(names_from = station, values_from = seen) # Move stations to columns

df %>% head()

## # A tibble: 6 x 12
##   fish  Release I80_1 Lisbon Rstr  Base_TD BCE   BCW   BCE2  BCW2  MAE   MAW
##   <fct> <chr>   <chr> <chr>  <chr> <chr>   <chr> <chr> <chr> <chr> <chr> <chr>
## 1 4842  X       X     X      X     X       X     X     X     X     X     X
## 2 4843  X       X     X      X     X       X     X     X     X     X     X
## 3 4844  X       X     X      X     X       X     X     X     X     X     X
## 4 4845  X       X     X      X     X       <NA>  <NA>  <NA>  <NA>  <NA>  <NA>
## 5 4847  X       X     X      <NA>  <NA>    <NA>  <NA>  <NA>  <NA>  <NA>  <NA>
## 6 4848  X       X     X      X     <NA>    <NA>  <NA>  <NA>  <NA>  <NA>  <NA>

# b)
df %>%
  pivot_longer(-fish, names_to = "station") %>% # Move back to long format
  group_by(station) %>%
  filter(!is.na(value)) %>% # Remove NAs
  summarize(count = n()) # Count number of records

## `summarise()` ungrouping output (override with `.groups` argument)

## # A tibble: 11 x 2
##    station count
##    <chr>   <int>
##  1 Base_TD    11
##  2 BCE         8
##  3 BCE2        7
##  4 BCW         8
##  5 BCW2        7
##  6 I80_1      19
##  7 Lisbon     13
##  8 MAE         5
##  9 MAW         5
## 10 Release    19
## 11 Rstr       12
```

## Complex Example

While this document follows some pretty simple examples using real-life data can get really complicated quickly. In the last example, I use real data from a study looking at tree transpiration. Data received from Campbell data loggers must be heavily manipulated to calculate "v" or the velocity of sap movement for each timestamp. A function is defined which performs all of the data wrangling steps and allows for the user to change the data sources and censoring protocols. While there is no need to fully understand what is going on with this example it is important to note that each step is documented with in line comments. This tidyverse _recipe_ which is saved as a function can then be added to a custom package and loaded as needed.

```r
# Define a function that accomplishes numerous data wrangling steps given several input variables.
tdp <- function(
  path, # Path to data files
  meta, # Name of metadata file
  min, # Minimum accepted value
  max, # Maximum accepted value
  mslope # Minimum accepted slope
) {

  list.files(path = path, # Define subfolder
                  pattern = "*.dat", # Pattern for file suffix
                  full.names = TRUE, # Use entire file name
                  recursive = TRUE) %>% # Create list of dat files
  map_df(~ read_csv(
    .x,
    skip = 4, # Skip first four lines
    col_names = F, # Don't auto assign column names
    col_types = cols(), # Don't output
    locale = locale(tz = "Etc/GMT+8") # Set timezone
  ) %>% # Read in all dat files
    select(-c(37:ncol(.))) %>% # Remove extra columns
    mutate(temp = as.integer(str_extract(.x, "(?<=_)\\d{1}(?=_TableTC.dat)")))) %>% # Extract site number from file name
  `colnames<-`(c("timestamp", "record", "jday", "jhm", 1:32, "plot_num")) %>% # Manually define column names
  select(plot_num, everything()) %>% # Move plot_num to be the first column
  pivot_longer(
    names_to = "channel",
    values_to = "dTCa",
    -(1:5),
    names_transform = list(channel = as.double)) %>% # Flatten data
  left_join(read_csv(meta,
                     col_types = cols())) %>% # Merge tree metadata
  filter(!is.na(tree_num)) %>% # Remove NAs associated with channels lacking a tree number
  unite(tree_id,
        c(plot_num, tree_num, tree_type), # Combine three variables
        sep = "-", # Use - as delimiter
        remove = FALSE) %>% # Create tree IDs
  arrange(plot_num, channel, timestamp) %>%
  mutate(date = as.Date(timestamp, tz = "Etc/GMT+8"), # Extract date
         hour = hour(timestamp), # Extract hour of day
         am = if_else(hour < 12, T, F), # True vs False for morning hours
         slope = dTCa - lag(dTCa), # Calculate dTCa slope for each timestep
         flag = ifelse(dTCa < min | dTCa > max | slope > mslope, TRUE, FALSE)) %>% # Flag values that are out of bounds
  filter(!flag) %>% # Filter and remove values that are out of bounds
  group_by(plot_num, channel) %>% # Group data by day/site/channel
  filter(date != min(date)) %>% # Remove first day of data collection
  group_by(plot_num, channel, date, am) %>% # include date and morning in grouping
  mutate(dTM = max(dTCa)) %>% # Calculate maximum temperature difference per day/site/channel
  ungroup() %>%
  mutate(baseline = if_else(dTCa == dTM & am, dTM, NA_real_), # Force dTM to occur in the morning
         diff = difftime(timestamp, lag(timestamp), units = "mins"), # Calculate time difference
         id = if_else(diff != 15 | is.na(diff), 1, 0), # Identify non-contiguous periods of time
         id = cumsum(id)) %>% # Unique IDs will be produced for contiguous periods of data collection
  group_by(plot_num, channel, id) %>%
  mutate(baseline = na.approx(baseline, na.rm = F, rule = 2)) %>% # Interpolate between baselines
  ungroup() %>%
  mutate(k = (baseline - dTCa) / dTCa, # Calculate the sap flux index
         v = 0.0119 * (k ^ 1.231) * 60 * 60, # Calculate sap velocity in cm/hr using Granier formula
         v = replace_na(v, 0)) %>% # Replace NAs with 0s
  group_by(tree_id, date, probe_depth) %>%
  summarize(sum_v = sum(v)) # Select important variables
}

# Perform data wrangling steps
tdp(path = "data", meta = "channels.csv", min = 2, max = 20, mslope = 1) %>%
  head()

## Joining, by = c("plot_num", "channel")

## `summarise()` regrouping output by 'tree_id', 'date' (override with `.groups` argument)

## # A tibble: 6 x 4
## # Groups:   tree_id, date [2]
##   tree_id date       probe_depth sum_v
##   <chr>   <date>           <dbl> <dbl>
## 1 1-1-DF  2020-07-03          15 155.
## 2 1-1-DF  2020-07-03          25  79.2
## 3 1-1-DF  2020-07-03          50 185.
## 4 1-1-DF  2020-07-03          90  29.6
## 5 1-1-DF  2020-07-04          15 156.
## 6 1-1-DF  2020-07-04          25  83.4
```
