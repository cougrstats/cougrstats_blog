---
title: An introduction to working with lists using purrr
author: cougrstats
date: '2020-02-19'
categories:
  - Package Introductions
tags:
  - advanced
  - loops
  - purrr
  - tidyverse
slug: an-introduction-to-working-with-lists-using-purrr
---

_By Matt Brousil_

This week I'm going to walk through some examples of applying functions to every item in one (or more) lists. Basically this gives an overview answering the question: "If I have a list of data, how do I loop through that list manipulating and running analyses on its data without using `for()` loops?" The goal will be to apply our manipulations and analyses the same way to every item in the list.

We can use the `purrr` package to replace loops. In my experience there is sometimes a speed tradeoff, but we can gain some very important confidence in the reproducibility and accuracy of our code with `purrr.` It can help us write more concise code that is structured in very consistent ways. This should be familiar to some degree if you saw [Vera Pfeiffer's](https://twitter.com/verawp) [talk](https://cougrstats.wordpress.com/2020/02/12/r-functions-and-the-apply-family/) on functions and using `lapply()`.

Today we'll analyze a dataset using several common tools from `purrr`, starting from reading in data using `purrr`. We'll do the following:

  1. Read in many CSVs as a list of data frames

  2. Apply a model to the data for each separate data frame

  3. Cover how to handle errors while iterating over lists

  4. Filter the data for each data frame separately, then combine into single data frame

  5. Split a data frame into a new list

  6. Plot and export .png files for many figures all at once

You can access a compressed file [here](https://drive.google.com/drive/folders/1HDeAg0EtqE_T1PuRBjKsczR8_ev3XKIA?usp=sharing) with the data and folder structure for this exercise. Note that the data are taken and modified from [here](https://www.spc.noaa.gov/wcm/).

## 1. Reading in data

Load the tidverse, which includes purrr and some other packages:

```r
library(tidyverse)
```

Our first step is to read in our data. We have several .csv files of tornado-related data, all structured in a similar way.

Let's look at the names. There's 11 csv files in our data directory.

```r
dir("data/", pattern = ".csv", full.names = TRUE)

##  [1] "data/2008_torn.csv" "data/2009_torn.csv" "data/2010_torn.csv"
##  [4] "data/2011_torn.csv" "data/2012_torn.csv" "data/2013_torn.csv"
##  [7] "data/2014_torn.csv" "data/2015_torn.csv" "data/2016_torn.csv"
## [10] "data/2017_torn.csv" "data/2018_torn.csv"
```

Using `purrr::map` we're able to read them all in at once. Here's how a map statement works:

    map(.x = , # Here we supply the vector or list of values (in this case filenames)
        .f = ~ ) # Here we supply the function we want to feed those values into

Compare this with `lapply()`, which is very similar:

```r
lapply(X = , # Vector or list of values
       FUN = ) # Function to apply to them
```

Jenny Bryan has a blog post [here](https://jennybc.github.io/purrr-tutorial/bk01_base-functions.html) that compares `purrr` functions to other R iteration options if you'd like to read more.

Ok, let's get started mapping:

```r
# Create vector of all csv filenames
filenames <- dir("data/", pattern = ".csv", full.names = TRUE)

# For each name in the vector, read it and make a dataframe out of it
tornado_data_list <- map(.x = filenames,
                         # .x signifies one item in our list of filenames
                         .f = ~ read.csv(file = .x,
                                         stringsAsFactors = FALSE))
```

Great, now what's the output of our `map()` statement look like?

```r
# str() is messy:
str(tornado_data_list)

# length() might be helpful. 11 dataframes
length(tornado_data_list)

## [1] 11

# We can look at individual ones
head(tornado_data_list[[1]])

##   om   yr mo dy       date     time tz st stf stn mag inj fat  loss closs  slat
## 1  1 2008  1  7 2008-01-07 14:22:00  3 MO  29   0   0   0   0  0.00     0 38.12
## 2  2 2008  1  7 2008-01-07 14:54:00  3 MO  29   0   0   0   0  0.02     0 38.36
## 3  3 2008  1  7 2008-01-07 15:30:00  3 IL  17   0   3   5   0  4.00     0 42.39
## 4  4 2008  1  7 2008-01-07 15:55:00  3 MO  29   0   0   0   0  0.00     0 39.07
## 5  5 2008  1  7 2008-01-07 16:02:00  3 WI  55   0   3   5   0 13.81     0 42.55
## 6  6 2008  1  7 2008-01-07 16:39:00  3 WI  55   0   1   0   0  7.93     0 42.62
##     slon  elat   elon   len wid ns sn sg  f1  f2 f3 f4 fc
## 1 -93.77 38.12 -93.77  0.07  20  1  1  1 185   0  0  0  0
## 2 -93.30 38.36 -93.30  0.17  25  1  1  1  15   0  0  0  0
## 3 -88.83 42.46 -88.60 13.20 100  1  1  1   7 111  0  0  0
## 4 -91.95 39.07 -91.95  0.30  40  1  1  1   7   0  0  0  0
## 5 -88.33 42.60 -88.14 10.78 200  1  1  1 127  59  0  0  0
## 6 -87.87 42.63 -87.82  2.48  75  1  1  1  59   0  0  0  0

# Or all of them
tornado_data_list
```

This is great: Instead of writing the same function (`read.csv()`) 11 times, we just did it once and got the same output essentially, albeit in list form.

## 2. Iteratively performing analyses

If you had just one of these data frames you might want to run a linear model using its data. We have 11, but we can still run models for each of them using `map()`. We'll model tornado rating (`mag`) as a function of estimated property loss (`loss`):

```r
map(.x = tornado_data_list,
    .f = ~  lm(formula = mag ~ loss, data = .x))

## Warning in storage.mode(v) <- "double": NAs introduced by coercion

## Error in lm.fit(x, y, offset = offset, singular.ok = singular.ok, ...): NA/NaN/Inf in 'y'
```

Whoops! You should have gotten an error. This happens, but when you have large lists and you're iterating over them it can be frustrating to run into an error that shuts down your whole analysis. What if you were using `map()` to run a function 100 times?

Luckily, `purrr` has some functions that allow us to continue pushing through past errors and to handle them elegantly. One of these is `safely()`, which for each list item you iterate over returns both a **result** and **error**. If the function runs without an error on a list item then it leaves you a `NULL` value for `error`, otherwise the error will be captured there. `result` will contain the output of the function, or `NULL` or another value you specify if an error occurs.

Let's use it:

```r
# We use the same function syntax as with map()
safe_model <- safely(.f = ~ lm(formula = mag ~ loss, data = .x),
                     # This is the default, just illustrated here to help
                     otherwise = NULL)

# Then we feed this newly wrapped function into the map statement we used that
# caused our earlier error.
safe_model_output <- map(.x = tornado_data_list,
                         .f = ~ safe_model(.x))

## Warning in storage.mode(v) <- "double": NAs introduced by coercion
```

The result is a list of lists...Each list item contains a list of two other items:
1. result, 2. error

```r
safe_model_output[[1]]

## $result
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##     0.55972      0.03637
##
##
## $error
## NULL
```

Great...This list is complicated now, though. We can use `transpose()` to invert it. This function will turn our list of paired result/errors and return to us **one list of results** and **one list of errors**. Dig it:

```r
transpose(safe_model_output)

## $result
## $result[[1]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##     0.55972      0.03637
##
##
## $result[[2]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##     0.50383      0.03762
##
##
## $result[[3]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##    0.602615     0.004762
##
##
## $result[[4]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##    0.786864     0.002123
##
##
## $result[[5]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##    0.568803     0.007743
##
##
## $result[[6]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##     0.61657      0.00275
##
##
## $result[[7]]
## NULL
##
## $result[[8]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##     0.49408      0.09331
##
##
## $result[[9]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##   2.515e-01    2.554e-07
##
##
## $result[[10]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##   2.534e-01    1.449e-08
##
##
## $result[[11]]
##
## Call:
## lm(formula = mag ~ loss, data = .x)
##
## Coefficients:
## (Intercept)         loss
##   3.846e-01    2.009e-08
##
##
##
## $error
## $error[[1]]
## NULL
##
## $error[[2]]
## NULL
##
## $error[[3]]
## NULL
##
## $error[[4]]
## NULL
##
## $error[[5]]
## NULL
##
## $error[[6]]
## NULL
##
## $error[[7]]
##
##
## $error[[8]]
## NULL
##
## $error[[9]]
## NULL
##
## $error[[10]]
## NULL
##
## $error[[11]]
## NULL
```

This is helpful because we can now just pull out the results portion and drop the null values (or, fix the errors and re-run if you choose).

    successful_models %
      discard(is.null)

    length(successful_models)

    ## [1] 10

Based on error output, it looks like we have an issue with the `mag` column in data frame 7.

```r
tornado_data_list[[7]]$mag %>% unique()

## [1] "0"            "2"            "1"            "3"            "4"
## [6] "cheeseburger"
```

My bad, I had burgers on the brain.

## 3. Summarizing and condensing datasets

Maybe we're sick of having 11 data frames now. Let's summarize the data a bit, and then have `purrr` spit the output back to us as a single, condensed data frame. The `_df` tacked onto `map` signifies that it's returning a single data frame as its output instead of a list. There are other output options as well.

    tornado_summary %
                                mutate(mag = as.numeric(mag)) %>%
                                filter(
                                  # Remove unknown values
                                  mag != -9,
                                  # Tornadoes not crossing state lines
                                  ns == 1,
                                  # Entire track in current state
                                  sn == 1,
                                  # Entire track, not a portion of the track
                                  sg == 1) %>%
                                select(om, date, yr, st, mag, loss, closs))

    ## Warning: NAs introduced by coercion

    head(tornado_summary)

    ##   om       date   yr st mag  loss closs
    ## 1  1 2008-01-07 2008 MO   0  0.00     0
    ## 2  2 2008-01-07 2008 MO   0  0.02     0
    ## 3  3 2008-01-07 2008 IL   3  4.00     0
    ## 4  4 2008-01-07 2008 MO   0  0.00     0
    ## 5  5 2008-01-07 2008 WI   3 13.81     0
    ## 6  6 2008-01-07 2008 WI   1  7.93     0

    tail(tornado_summary)

    ##           om       date   yr st mag  loss closs
    ## 12966 617019 2018-12-27 2018 LA   1  7000     0
    ## 12967 617020 2018-12-27 2018 LA   1  7000     0
    ## 12968 617021 2018-12-27 2018 MS   0 15000     0
    ## 12969 617022 2018-12-31 2018 KY   1 55000     0
    ## 12970 617023 2018-12-31 2018 IN   1 50000     0
    ## 12971 617024 2018-12-31 2018 IN   1 20000     0

## 4. Splitting into lists and extracting list items

Previously the data had been separated into a list by year, but maybe what we really want is to get them separated at the state level. We can do this!

    tornado_by_state %
      # x is our data frame to split
      split(x = .,
            # f is the factor to use in splitting (state in this case)
            f = list(.$st))

    # How many list items do we have now?
    length(tornado_by_state)

    ## [1] 51

Let's plot yearly data, but we're not sure it will work so we'll use safely() again.

    safe_plot % ggplot() + geom_boxplot(aes(group = yr, y = loss)),
                        otherwise = NULL)
    plot_test <- map(.x = tornado_by_state,
                     .f = ~ safe_plot(.x))

There are a couple of ways to extract list items, but one method we can use is `pluck()`

    plot_results %
      transpose() %>%
      pluck("result")

## 5. Iterating over multiple vectors or lists

Now we can save each of these plots we've created. We'll want to have names ready for their filenames, though. To combine our state names with our state plots we'll use `map2()`, which iterates over two vectors or lists (.x & .y) simultaneously. **Note** that this iteration is in parallel! This means that .x[1] and .y[1] are both used simultaneously, then .x[2] and .y[2], etc. The two vectors are not crossed, but this can be done using the `purrr::cross()` function if you'd like. Also note that because they are done in parallel, .x and .y have to have the same length!

We'll make a plot for each state, named `_tornado_plot.png`.

```r
# Are the data frame names and the plot list compatible for map2?
length(names(tornado_by_state)) == length(plot_results)

## [1] TRUE

map2(.x = names(tornado_by_state),
     .y = plot_results,
     .f = ~ ggsave(filename = paste0("figures/", .x, "_tornado_plot.png"),
                   plot = .y, device = "png", width = 8, height = 6,
                   units = "in"))
```

## References:

  * <https://purrr.tidyverse.org/>

  * <https://jennybc.github.io/purrr-tutorial/bk01_base-functions.html>
