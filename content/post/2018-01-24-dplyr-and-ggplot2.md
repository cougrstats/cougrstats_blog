---
title: Resources for dplyr and ggplot2
author: cougrstats
date: '2018-01-24'
categories:
  - Package Introductions
tags:
  - dplyr
  - ggplot2
  - resource
  - tidyverse
slug: dplyr-and-ggplot2
---

Today we introduced the R packages 'dplyr' and 'ggplot2'. We only had time for a few brief demos, but these packages are very powerful and you may be using them quite a bit!

**More about dplyr**

dplyr is useful for manipulating data. Most of the time you'll be using one of 5 main functions:

filter(): subsets rows based on a condition

select(): selects specific columns

mutate(): creates a new column

group_by(): groups data by some variable

summarize(): returns new data frame with specified summary statistics

These aren't the only functions in the dplyr package, but you can get pretty far with your data manipulation with only these 5 functions!

_Some dplyr resources:_

Main dplyr [webpage](http://dplyr.tidyverse.org/)

dplyr [cheatsheet ](https://www.rstudio.com/wp-content/uploads/2015/02/data-wrangling-cheatsheet.pdf)(includes some functions from package tidyr)

[Tutorial](https://rpubs.com/justmarkham/dplyr-tutorial) from RStudio

[Tutorial ](http://genomicsclass.github.io/book/pages/dplyr_tutorial.html)with biological data

**More about ggplot2**

You can make plots using base R (i.e. no packages loaded), but sometimes you may want to make certain plots that are a challenge in base R. ggplot2 is the main graphics package people use in R: it's very powerful and you can make great visualizations with it.

To best understand ggplot2, you'll need to start thinking in terms of "the grammar of graphics." It can take a while to get a hang of the ggplot2 syntax, particularly the aesthetics, or aes(), portion, but with it you can really fine tune your graphics.

_Some ggplot2 resources:_

Main ggplot2 [website ](http://ggplot2.tidyverse.org/reference/)

ggplot2 [cheatsheet ](https://www.rstudio.com/wp-content/uploads/2015/03/ggplot2-cheatsheet.pdf)

[Tutorial ](http://tutorials.iq.harvard.edu/R/Rgraphics/Rgraphics.html)using social science data

[Tutorial ](http://uc-r.github.io/ggplot)on making different kinds of plots

Graphics [gallery ](https://plot.ly/ggplot2/)(with code)

Another graphics [gallery](https://www.r-graph-gallery.com/) (with code)

**Welcome to the tidyverse!**

This is also our first introduction to the "[tidyverse](https://www.tidyverse.org/)" - R packages for data science that are designed to work well together. You can learn more about the the idea and implementation of the R tidyverse [here](https://rviews.rstudio.com/2017/06/08/what-is-the-tidyverse/).
