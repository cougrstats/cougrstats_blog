---
title: Sharing and cleaning data
author: Abigail Hudak
date: '2020-04-01'
categories:
  - Package Introductions
tags:
  - cleaning
  - formatting
  - janitor
  - sharing code
slug: sharing-and-cleaning-data
---

_By Abigail Hudak_

# Overview

The goal of this document is to share some tips and ideas about structuring and cleaning data for sharing and collaborating. None of the concepts are comprehensive, but I hope you find some useful tips.

# Cleaning data

**Favorites of janitor**

The package janitor is awesome for data cleaning. Consider learning this package if using a lot of Excel sheets from other users. Excel sheets may have bad columns names (i.e. with "?" or upper and lowercase letters) or empty data, etc. You want your R objects to be clean 1) for your sanity, 2) for readability of your code, and 3) for ease of coding.

A couple useful links for this package:
1) <https://github.com/sfirke/janitor>
2) <https://garthtarr.github.io/meatR/janitor.html>

Making sure column names are clean

```r
library(janitor)
library(tidyverse)
data("iris")

colnames(iris) #view current column names

## [1] "Sepal.Length" "Sepal.Width"  "Petal.Length" "Petal.Width"  "Species"

colnames(clean_names(iris, case = "screaming_snake")) #change column names to all caps and separted by underscore

## [1] "SEPAL_LENGTH" "SEPAL_WIDTH"  "PETAL_LENGTH" "PETAL_WIDTH"  "SPECIES"

colnames(clean_names(iris)) #change column names to lower case and separted by underscore

## [1] "sepal_length" "sepal_width"  "petal_length" "petal_width"  "species"

iris<-clean_names(iris) #keep this one
```

Evaluate your data: make a frequency table. tabyl() similar to table() in base R, but better (returns a data.frame and has other features).

```r
tabyl(iris, species)

##     species  n   percent
##      setosa 50 0.3333333
##  versicolor 50 0.3333333
##   virginica 50 0.3333333

iris %>% tabyl(species) #can be piped-in, if you are into that

##     species  n   percent
##      setosa 50 0.3333333
##  versicolor 50 0.3333333
##   virginica 50 0.3333333

iris %>% tabyl(species) %>% adorn_totals("row") #add total count row

##     species   n   percent
##      setosa  50 0.3333333
##  versicolor  50 0.3333333
##   virginica  50 0.3333333
##       Total 150 1.0000000

#adorn_() functions ahve lots of basic reporting features!
```

Other great functions

```r
get_dupes() #find duplicate rows
excel_numeric_to_date() #converts Excel serial number dates (42223) to a class date ("2020-04-1")
remove_empty() #remove columns and/or rows that are entirely empty
```

**Favorites of Tidyverse**

Qucikly manipulate data into new structures, change column names, etc. See "cheat sheat" below for data warngling technqiues using dplyr and tidyr.

<https://rstudio.com/wp-content/uploads/2015/02/data-wrangling-cheatsheet.pdf>

Reshaping data

```r
unite() #unites several columns into one
separate() #separate one column into several
spread() #spread rows into columns. Long data->wide data
gather() #gather columns into rows. Wide data->long data
arrange() #order rows by values ina  column (ascending)
arrange(x, desc(y)) #descending order
rename() #rename individual columns (not good for changing a lot)
```

# Script writing

**General tips**

_Your code should be readable for your own sanity and for reproducibility._
- Use `::` to show which package does what `dplyr::lef_join(a, b, by = "x1")`
- Spacing before and after operator `function = print()`
- Indentation doesn't have any meaning in R like it does in other languages, but it is critical in making your code readable.
- Annotate your code!! Good to annotate above or next to a line.

```r
#gross
new<-data.frame %>% select(this_column)%>% group_by(this_variable) %>%mutate(new_column = mean(that_column))

#better
new <- data.frame %>% #select data.frame to manipulate
      select(this_column, that_column) %>% #select columns to keep
      group_by(that_column) %>% #group together by a column
      mutate(new_column = mean(that_column)) #make a new column of the means

#alternative styles

new <- data.frame %>%                          #select data.frame to manipulate
      select(this_column, that_column) %>%     #select columns to keep
      group_by(that_column) %>%                #group together by a column
      mutate(new_column = mean(that_column))   #make a new column of the means

       #select data.frame to manipulate
new <- data.frame %>%
       #select columns to keep
       select(this_column, that_column) %>%
       #group together by a column
       group_by(that_column) %>%
       #make a new column of the means
       mutate(new_column = mean(that_column))
```

# Script writing mediums

**R markdown**

RMD (what this document is) is _really_ awesome.

Some key features allow for flexibility in visualization of code and data sharing depedning on your audience. For a reader who may not be interested in the code, you can hide it and only show the output. However, if your reader would want to see what packagaes you used, the code, etc. you can have that shown as well.

**common chunk options**

hide message: message = FALSE

hide warning: warning = FALSE

hide all : include = FALSE

hide results : results = "hide" or results = FALSE

only print output: echo = FALSE

prevent code from running: eval = FALSE

<https://cougrstats.wordpress.com/2019/09/12/a-tour-of-r-markdown/>

**R script**

I am personally not a fan because I: 1) don't like autofill and 2) like to View() my data a lot so I don't like having my script in that same spot.

**Notepad++**

Big fan. Perks: no autofill, automatic indentation, can have a seprate window for code and RStudio (especially nice when you have a monitor)

**Notepad**

Before you judge me...there are perks! I like to use this as my scratch space to play around with code. What's great about saving code in a text file is that you can search in your file explorer for key terms to help you find a code. I find this extremely helpful so I can go back and find a function/code/etc. I want to use again. Downside: can only Ctrl + Z once (why this is good to serve as scratch space) and no automatic indentation.

# Posting for help on Stack Overflow

<https://stackoverflow.com/>

To get good feedback, you need to post good questions. For others to help you: 1) your data structure should be clearly laid out, 2) your goal should be clearly stated, and 3) your error/problem/question should be clearly addressed. Usually also good to post code that you have already tried and the outcome or error message. If possible, post an example of what you want the outcome to look like.

Usually good to post dummy data that have intuitive variables and easy to use numbers (if possible). Remember if you are posting biologically-related concepts, you are limiting who can help you if you aren't being clear. To post dummy data use `rnorm(n, mean = , sd = )` to make a normal distribution of numbers or `runif(n, min = , max = )` to generate numbers from uniform distribution.

# Publicly sharing code

RPubs _easy_ to use and free.

Github is widely used and allows for version control.
<http://swcarpentry.github.io/git-novice/>
