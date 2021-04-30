---
title: Formatting data for use with R
author: Matt Brousil
date: '2020-10-21'
categories:
  - Introduction to R
tags:
  - data formatting
  - janitor
slug: formatting-data-for-use-with-r
---

_By Matt Brousil_

This post walks through some best practices for formatting and preparing your data for use with R. Some of the suggestions here are drawn from [Data Carpentry](https://datacarpentry.org/spreadsheet-ecology-lesson/), [Broman and Woo (2018)](https://www.tandfonline.com/doi/full/10.1080/00031305.2017.1375989), and the [BES Guide to Reproducible Code](https://www.britishecologicalsociety.org/wp-content/uploads/2017/12/guide-to-reproducible-code.pdf). The required dataset is available [here](https://drive.google.com/drive/folders/1DB_HnYme0pJ8bxqbAwut1Uaq3Zuk_NMB?usp=sharing). A previous version of this post that deals with cleaning both data and scripts is available [here](https://cougrstats.wordpress.com/2019/04/10/cleaning-messy-scripts-and-data/).

```r
library(tidyverse)
library(readxl)
library(janitor)
library(lubridate)
```

### 1. Use .csv instead of .xlsx or other proprietary file formats when possible.

The `.csv` filetype can be read easily by many software packages, including base R. This isn't necessarily the case with `.xlsx`. Instead, we use the `readxl` package here. In my experience, other packages for reading Excel files can have issues installing on many computers due to their installation requirements.
```r
raw_data <- read_excel(path = "cool project 2020.xlsx")
```
Additional notes:

  * If your `.xlsx` has multiple sheets, then make multiple files. This is a more reliable storage method, and `.csv` files don't allow for multiple sheets.
  * Don't use **formatting** to store data. R can't decipher things like highlighting easily and the ways of documenting formatting meaning often leave a lot to be desired. But if you need to detect Excel formatting from R, check out [this blog post](https://www.r-bloggers.com/2014/08/when-life-gives-you-coloured-cells-make-categories/).

### 2. File naming

`cool project 2020.xlsx` isn't a good name! There are a few points we want to keep in mind with file naming:

  * Machine readability
    * Don't use spaces in filenames
    * Don't use characters other than letters, numbers, and _ or -
  * Human readability
    * Make sure the name of the file is descriptive, try to follow a consistent naming convention

Something like `brousil_thesis_data_2020.csv` is a better name, although you might want to make yours more specific.``

### 3. Column naming

Let's take a look at our column names:
```r
names(raw_data)

## [1] "start date"   "end date"
## [3] "which group?" "value"
## [5] "\"Notes\""    "lat"
## [7] "long"
```
Here's what the dataset itself looks like:
```r
head(raw_data)

## # A tibble: 6 x 7
##   `start date` `end date`
##          <dbl> <dttm>
## 1        40142 2010-05-05 00:00:00
## 2        40143 2010-05-06 00:00:00
## 3        40143 2010-05-06 00:00:00
## 4           NA 2010-05-08 00:00:00
## 5           NA 2010-05-09 00:00:00
## 6        40142 2010-05-05 00:00:00
## # ... with 5 more variables: `which
## #   group?` <chr>, value <dbl>,
## #   `"Notes"` <chr>, lat <chr>, long <chr>
```
The column naming in this dataset is a mess! Note that the formatting of the column names changes between the vector output of `names()` and the tibble version from `head()`. We could have avoided this instability. When naming columns in a spreadsheet for use in R,
we should avoid:

  * Spaces
  * Special characters
  * Capitalization

Spaces in particular make it very difficult to refer to column names, because you have to use backticks or quotes when referencing them. Capitalization isn't a huge deal, but it adds extra keystrokes to your names and also makes it easier to misspell them.
```r
raw_data$`which group?`

# This won't work
raw_data %>% select(which group?)

# This will work
raw_data %>% select("which group?")
```
We can take care of the names quickly using `clean_names()` from `janitor`.

```r
raw_data <- clean_names(raw_data)

names(raw_data)

## [1] "start_date"  "end_date"    "which_group"
## [4] "value"       "notes"       "lat"
## [7] "long"
```

### 4. Layout of the data

The next step is to consider the layout of the data. For example, is the dataset in [tidy format](https://twitter.com/juliesquid/status/1315710359404113920?s=20)? Let's take a look:

```r
raw_data

## # A tibble: 10 x 7
##    start_date end_date            which_group
##         <dbl> <dttm>              <chr>
##  1      40142 2010-05-05 00:00:00 A
##  2      40143 2010-05-06 00:00:00 A
##  3      40143 2010-05-06 00:00:00 B
##  4         NA 2010-05-08 00:00:00 B
##  5         NA 2010-05-09 00:00:00 A
##  6      40142 2010-05-05 00:00:00 A
##  7      40148 2010-05-11 00:00:00 A
##  8      40148 2010-05-11 00:00:00 A
##  9      40149 2010-05-12 00:00:00 B
## 10      40142 2010-05-05 00:00:00 A
## # ... with 4 more variables: value <dbl>,
## #   notes <chr>, lat <chr>, long <chr>
```

This dataset is close, but not quite in **tidy** format.

Good qualities of the layout:
  * A single table
  * Variables are in columns
  * Observations are in rows

Bad qualities of the layout:
  * Multiple pieces of data in the `notes` column
  * Duplicated rows

To start, let's separate the notes column into multiple columns.

```r
clean_data <- separate(data = raw_data, col = notes, into = c("type", "location"),
                    sep = ", ", remove = FALSE)

head(clean_data)

## # A tibble: 6 x 9
##   start_date end_date            which_group
##        <dbl> <dttm>              <chr>
## 1      40142 2010-05-05 00:00:00 A
## 2      40143 2010-05-06 00:00:00 A
## 3      40143 2010-05-06 00:00:00 B
## 4         NA 2010-05-08 00:00:00 B
## 5         NA 2010-05-09 00:00:00 A
## 6      40142 2010-05-05 00:00:00 A
## # ... with 6 more variables: value <dbl>,
## #   notes <chr>, type <chr>, location <chr>,
## #   lat <chr>, long <chr>
```

Next, let's investigate the duplicate rows. We'll print any rows that aren't unique using `get_dupes()` from `janitor` and then remove the repeated row with help from `duplicated()`.

```r
# From janitor
get_dupes(clean_data)

## No variable names specified - using all columns.

## # A tibble: 2 x 10
##   start_date end_date            which_group
##        <dbl> <dttm>              <chr>
## 1      40142 2010-05-05 00:00:00 A
## 2      40142 2010-05-05 00:00:00 A
## # ... with 7 more variables: value <dbl>,
## #   notes <chr>, type <chr>, location <chr>,
## #   lat <chr>, long <chr>, dupe_count <int>

# From base R. Note that it prints out a logical vector.
duplicated(clean_data)

##  [1] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
##  [8] FALSE FALSE FALSE
```

Drop the extra row using `duplicated()`:

```r
clean_data <- clean_data[!duplicated(clean_data), ]
```

### 5. Dates

Dates are **tricky** in Excel. It has a lot of automatic formatting options that are intended to be helpful. They often lead to problems, though. Moreover, things that aren't supposed to be dates are interpreted by Excel to be dates.

This dataset shows multiple potential pitfalls with dates.
  1. The `start_date` column contains [Excel serial number dates](https://www.lifewire.com/serial-number-serial-date-3123991) that haven't translated over to R.
  2. The `end_date` column has imported correctly! But when it was entered into Excel, it was formatted like this: `5/11/10`. This isn't trustworthy, and 5, 11, and 10 are all realistic values for the year, month, or day.

Some of the safest ways to enter dates are as follows:
  * As separate columns in your spreadsheet: `year`, `month`, `day`
  * As ISO 8601: `YYYY-MM-DD` (e.g., 2020-10-21)
    * ISO = International Organization for Standardization

Luckily we can clean up the Excel serial formatted dates:

```r
clean_data$start_date <- excel_numeric_to_date(as.numeric(clean_data$start_date))
```

If we want to save the data as a .csv for later use in Excel, we might want to split the dates up still and drop the original columns.

```r
clean_data <- clean_data %>%
mutate(start_year = year(start_date),
       start_mo = month(start_date),
       start_day = day(start_date),
       end_year = year(end_date),
       end_mo = month(end_date),
       end_day = day(end_date)) %>%
  select(-start_date, -end_date)

head(clean_data)

## # A tibble: 6 x 13
##   which_group value notes type  location lat
##   <chr>       <dbl> <chr> <chr> <chr>    <chr>
## 1 A               1 expe~ expe~ greenho~ -27.~
## 2 A               5 expe~ expe~ greenho~ -27.~
## 3 B              75 expe~ expe~ lab      -27.~
## 4 B               4 expe~ expe~ greenho~ -27.~
## 5 A               2 expe~ expe~ lab      -27.~
## 6 A               1 expe~ expe~ lab      -27.~
## # ... with 7 more variables: long <chr>,
## #   start_year <dbl>, start_mo <dbl>,
## #   start_day <int>, end_year <dbl>,
## #   end_mo <dbl>, end_day <int>
```

### 6. Missing values

Many datasets you work with will likely contain missing values. It's important to know why data can be missing, and how to treat it differently based on the reason for its absence.

  * Make sure that you enter 0 when your data is supposed to contain zero! Often people will leave zeroes blank during data entry, and it's not clear to the user whether these are intended to be missing data or actual 0 values.
  * There's not uniform agreement about how to code in **truly** missing data. But there are multiple options. Either a **blank** cell or a manually entered **NA** value is best for data that truly are gaps in the dataset. My thought is that `NA` is probably best, i.e. it is clear that the data are missing and not just forgot to enter (Broman & Woo, 2018).
    * e.g., An experimental replicate was lost, data logger corrupted, etc.
  * Always fill in values, even when they are just repeats of dates in the rows above!

### 7. Miscellaneous

Lastly, you'll want to avoid including special characters or units inside of cells with numeric data (e.g., `lat`/`long`). There's a few reasons for this:

  * These characters or units won't typically add anything to your analytical abilities in R
  * Special characters may be difficult to wrangle in R
  * The presence of a special character in a numeric column will likely force that column to be character rather than numeric data

My suggestion is either don't include them at all, or you can reference them in column name, e.g. `distance_m`.

We can drop them from our dataset using `gsub()`:

```r
clean_data$lat <- gsub(pattern = "°", replacement = "", x = clean_data$lat)
clean_data$long <- gsub(pattern = "°", replacement = "", x = clean_data$long)
```

### 8. Keep your raw data untouched and separate from cleaned data!

In case a transcription or cleaning error happens, you need to be able to compare your original dataset (untouched) to the cleaned version. Save a new .csv separately from the old data.

```r
write.csv(x = clean_data,
          file = "brousil_cleaned_thesis_data.csv",
          row.names = FALSE)
```

### Sources:

  * Cooper, N., & Hsing, P. Y. (2017). A guide to reproducible code in ecology and evolution. Technical report, British Ecological Society. Available at <https://www.britishecologicalsociety.org/wp-content/uploads/2017/12/guide-to-reproducible-code.pdf>.
  * Karl W. Broman & Kara H. Woo (2018) Data Organization in Spreadsheets, The American Statistician, 72:1, 2-10, DOI: 10.1080/00031305.2017.1375989
  * Peter R. Hoyt, Christie Bahlai, Tracy K. Teal (Eds.), Erin Alison Becker, Aleksandra Pawlik, Peter Hoyt, Francois Michonneau, Christie Bahlai, Toby Reiter, et al. (2019, July 5). datacarpentry/spreadsheet-ecology-lesson: Data Carpentry: Data Organization in Spreadsheets for Ecologists, June 2019 (Version v2019.06.2). Zenodo. <http://doi.org/10.5281/zenodo.3269869>
