---
title: Basics of R Markdown
author: cougrstats
date: '2018-02-12'
categories:
  - Package Introductions
tags:
  - collaboration
  - Rmarkdown
  - Rstudio
slug: basics-of-r-markdown-rmd
---

_Author: Alli N. Cramer_

### R Markdown

R Markdown is an easy way to share and communicate your results from R. Markdown is a simple formatting syntax for authoring HTML, PDF, and MS Word documents that comes with R Studio.

To make a new R markdown document, go to File -> New File -> R Markdown.

New R Markdown documents always have a simple test document, which uses the cars and pressure datasets. To see how this creates an easily read html, pdf, or MS word file simply click the "Knit" button at the top left of the Markdown scripting window. The test document includes the chunks below:

### Basic test R Markdown

When you click the **Knit** button a document will be generated that includes both content as well as the output of any embedded R code chunks within the document. You can embed an R code chunk like this:

```r
summary(cars)

##      speed           dist
##  Min.   : 4.0   Min.   :  2.00
##  1st Qu.:12.0   1st Qu.: 26.00
##  Median :15.0   Median : 36.00
##  Mean   :15.4   Mean   : 42.98
##  3rd Qu.:19.0   3rd Qu.: 56.00
##  Max.   :25.0   Max.   :120.00
```

#### Including Plots

You can also embed plots, for example:

![plot of chunk pressure](http://cougrstats.files.wordpress.com/2018/02/pressure-1.png)

Note that the `echo = FALSE` parameter was added to the code chunk to prevent printing of the R code that generated the plot.

## Using R Markdown

As you are scripting, each r chunk needs to be coded using a "`{r}....`" syntax. The example document shows you this. To run a chunk as you are scripting you can click the green arrow on the top right of each chunk. To change what portions of the R chunk are shown in the final document (for example, do you want to see the code or just the plot? any warnings? etc.) you add commands within the `{r}` brackets. You can also point and click these commands in by clicking the settings button (it looks like a gear) at the top of the r chunk by the green arrow.

Attached to this post is the script, example html, and images used in generating the html for an example R Markdown document provided by Michael Meyer. This exmple script includes a table of contents, slides, linear models, and a use of a cool package called mathpix which lets you embed math equations from images.

The best way to learn R Markdown is to use it, so have fun!

For more details on using R Markdown see <http://rmarkdown.rstudio.com>.

[Example Markdown Script
](https://drive.google.com/uc?export=download&id=1dL7m-niwJSZbW3e62nuei9WmnSfsk4Mt)[Example Markdown HTML](https://drive.google.com/uc?export=download&id=1sZKdHorBVB88B5EVXE-YI-Ms9y4zSdCR)
Example script pictures: [Capture_normal](https://s3.wp.wsu.edu/uploads/sites/95/2018/02/Capture_normal.png) [Capture_variance](https://s3.wp.wsu.edu/uploads/sites/95/2018/02/Capture_variance.png)
