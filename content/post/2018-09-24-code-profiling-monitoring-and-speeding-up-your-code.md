---
title: 'Code Profiling: Monitoring and Speeding up your code'
author: Julia Piaskowski
date: '2018-09-24'
categories:
  - Package Introductions
tags:
  - advanced
  - best practices
  - code profiling
  - speed
slug: code-profiling-monitoring-and-speeding-up-your-code
---

_By Julia Piaskowski_

##### Sources

Thomas Lumley, Github repo [useRfasteR](https://github.com/tslumley/useRfasteR)
Hadley Wickham, [Profiling](http://adv-r.had.co.nz/Profiling.html), _Advanced R_
Dirk Eddelbuettel, [Rcpp](http://www.rcpp.org/)

#### The Process for Improving Code:
(quote from _Advanced R_)


>   1. Find the biggest bottleneck (the slowest part of your code).
>
>   2. Try to eliminate it (you may not succeed but that's ok).
>
>   3. Repeat until your code is fast enough.


**Easy peasy, right???**

![](https://cougrstats.files.wordpress.com/2018/09/owl.png)

#### Some general guidelines for speeding up R code

  1. Use data frames less - they are expensive to create, often copied in whole when modified, and their rownames attribute can really slow things down.

  2. Be wary of using functions that copy objects in whole: c(), append(), cbind(), rbind(), or paste(). When used in loops, you can get a massive proliferation of objects in memory.

  3. Use vectorised functions:

    * apply, lapply, sapply, vapply, tapply, mapply

    * rowSums, colSums, rowMeans, colMeans, cumsum, diff

  4. Base functions are designed to handle wildly different input. Consider rewriting base functions for highly repetitive tasks.

  5. Use parallel::mclapply for parallelising functions.

  6. Consider an optimized matrix algebra library (beyond BLAS) for better performance (e.g. [Apple vecLib BLAS](https://developer.apple.com/documentation/accelerate/blas), [openBLAS](https://www.openblas.net/)).

  7. If you work with sparse matrices, use tools for them like the package 'Matrix'.

  8. For huge objects, consider storing the information in a database and accessing it with 'dbplyr'. The packages 'dbglm' and 'tidypredict' will also do model fitting with data inside a database.

  9. Another solution for large objects are specialized formats like [HDF5](https://portal.hdfgroup.org/display/support) or [netCDF](https://www.unidata.ucar.edu/software/netcdf/).

  10. Take advantage of the Rcpp suite of programs - not just for C/C++ programmers (e.g. RcppArmadillo::fastlm).

  11. Use an alternative implementation of R (e.g., [fastR](https://github.com/oracle/fastr%5D), [pqR](http://www.pqr-project.org/)).

  12. Check your code with benchmarking!!!

#### Let's do some benchmarking!

Important: don't (re)install 'compiler'; you should just be able to load it in R v3.5 and later.

```r
pck <- c("pryr","microbenchmark", "profvis", "compiler", "mnormt")
invisible(lapply(pck, library, character.only = T))

## Warning: package 'pryr' was built under R version 3.5.1

##
## Attaching package: 'pryr'

## The following object is masked from 'package:data.table':
##
##     address

## Warning: package 'microbenchmark' was built under R version 3.5.1

## Warning: package 'profvis' was built under R version 3.5.1
```

First, Turn off the just-in-time compiler. Note that return value is what the JIT was set at previously (default = 3).

```r
enableJIT(0)

## [1] 3
```

##### The microbenchmark function

  * for evaluating small snippets of code
  * below is a comparison of several approaches to calculating a mean

```r
a <- function() {
  m <- sample(1:100, 2)
  data.x <- lapply(m, function(x) rnorm(1e4, mean = x))
  do.call("cbind", data.x)
}

some_data <- a()
dim(some_data)

## [1] 10000     2

microbenchmark(
  mean_loop = apply(some_data, 2, mean),
  mean_vec = colMeans(some_data),
  mean_manual = apply(some_data, 2, function(x) sum(x)/length(x)),
  mean_manual_ultra = apply(some_data, 2, function(x){
    total = 0
    n = 0
    i = 1
    while(!is.na(x[i])) {
      total = total + x[i]
      n = n+1
      i = i+1
    }
    total/n
  })
)

## Unit: microseconds
##               expr       min         lq        mean     median         uq
##          mean_loop   161.333   178.4915   211.83635   196.1325   234.3010
##           mean_vec    21.491    24.5375    33.40574    30.6315    39.7725
##        mean_manual   135.673   148.0220   181.27308   169.9925   203.6700
##  mean_manual_ultra 26512.007 26947.7305 28382.64290 27481.9230 28278.1590
##        max neval
##    388.737   100
##    118.353   100
##    324.268   100
##  39815.319   100
```

##### Prevent multiple dispatch:

  * the function mean() is meant to handle several different types of data
  * specifying the method (thus implying a certain type of input) can speed up the process for small data sets

```r
# the function mean() calls a different function depending on the object specified
methods(mean)

## [1] mean.Date     mean.default  mean.difftime mean.IDate*   mean.POSIXct
## [6] mean.POSIXlt
## see '?methods' for accessing help and source code

x1 <- list(e2 = runif(1e2), e4 = runif(1e4), e6 = runif(1e6))

lapply(x1, function(x)
  microbenchmark(
    mean(x),
    mean.default(x)
  )
)

## $e2
## Unit: nanoseconds
##             expr  min   lq    mean median   uq   max neval
##          mean(x) 3528 3529 4189.61   3849 3850 23735   100
##  mean.default(x)  642  963 1322.17    963 1283 15076   100
##
## $e4
## Unit: microseconds
##             expr    min     lq     mean median     uq    max neval
##          mean(x) 21.169 21.491 23.26722 21.811 22.774 50.036   100
##  mean.default(x) 18.282 18.603 19.61392 18.604 19.566 38.489   100
##
## $e6
## Unit: milliseconds
##             expr      min       lq     mean   median       uq      max
##          mean(x) 1.858365 1.901665 1.934968 1.923636 1.955228 2.134843
##  mean.default(x) 1.842008 1.880336 1.911076 1.905353 1.938871 2.048243
##  neval
##    100
##    100

# I suspect the improvement in speed for smaller objects but larger objects is related to big O notation -- these smaller objects are impacted by constants

# tracking package type, etc
otype(mean)

## [1] "base"

ftype(mean)

## [1] "s3"      "generic"

showMethods(mean) #for S4

##
## Function "mean":
##  <not an S4 generic function>

methods(mean)

## [1] mean.Date     mean.default  mean.difftime mean.IDate*   mean.POSIXct
## [6] mean.POSIXlt
## see '?methods' for accessing help and source code

#this doesn't always work:
methods(var)

## Warning in .S3methods(generic.function, class, parent.frame()): function
## 'var' appears not to be S3 generic; found functions that look like S3
## methods

## [1] var.test          var.test.default* var.test.formula*
## see '?methods' for accessing help and source code

getAnywhere(var)

## A single object matching 'var' was found
## It was found in the following places
##   package:stats
##   namespace:stats
## with value
##
## function (x, y = NULL, na.rm = FALSE, use)
## {
##     if (missing(use))
##         use <- if (na.rm)
##             "na.or.complete"
##         else "everything"
##     na.method <- pmatch(use, c("all.obs", "complete.obs", "pairwise.complete.obs",
##         "everything", "na.or.complete"))
##     if (is.na(na.method))
##         stop("invalid 'use' argument")
##     if (is.data.frame(x))
##         x <- as.matrix(x)
##     else stopifnot(is.atomic(x))
##     if (is.data.frame(y))
##         y <- as.matrix(y)
##     else stopifnot(is.atomic(y))
##     .Call(C_cov, x, y, na.method, FALSE)
## }
## <bytecode: 0x00000000117ce320>
## <environment: namespace:stats>
```

##### Find the bottlenecks with Rprof()

  * writes stack calls to disk along with memory usage and vector duplication
  * you create a .prof file to do this and then close it when done with profiling

```r
Rprof("permute.prof", memory.profiling = T)

sigma.mv <- diag(1, nrow = 5, ncol = 5)
sigma.mv[upper.tri(sigma.mv)] = 0.5
sigma.mv[lower.tri(sigma.mv)] = 0.5

mvn.data <- rmnorm(1e3, mean = rep(0, 5), varcov = sigma.mv)
colnames(mvn.data) <- c(paste0("x",1:5))

kmeans.Ftest <- function(kmean_obj) {
  df.1 = length(kmean_obj$size) - 1
  df.2 = length(kmean_obj$cluster) - length(kmean_obj$size)
  betw_ms <- kmean_obj$tot.withinss/df.1
  with_ms <- kmean_obj$betweenss/df.2
  fratio = betw_ms/with_ms
  pval <- pf(fratio, df1 = df.2, df2 = df.1, lower.tail = F)
  stuff = c(fratio, df.1, df.2, pval)
  names(stuff) <- c('F-ratio', 'df 1','df 2', 'p-value')
  return(stuff)
}

kmeans.optimiz <- lapply(2:10, function(x) {
    results = kmeans(mvn.data, centers = x, nstart = 15, algorithm = "MacQueen",
                        iter.max = 50)
    kmeans.Ftest(results)
})

kmeans.final <- do.call("rbind", kmeans.optimiz)

Rprof(NULL)
summaryRprof("permute.prof") #, memory = "both")

## $by.self
##           self.time self.pct total.time total.pct
## ".C"           0.10    71.43       0.10     71.43
## "apply"        0.02    14.29       0.02     14.29
## "as.list"      0.02    14.29       0.02     14.29
##
## $by.total
##                       total.time total.pct self.time self.pct
## "block_exec"                0.14    100.00      0.00     0.00
## "call_block"                0.14    100.00      0.00     0.00
## "doTryCatch"                0.14    100.00      0.00     0.00
## "eval"                      0.14    100.00      0.00     0.00
## "evaluate"                  0.14    100.00      0.00     0.00
## "evaluate::evaluate"        0.14    100.00      0.00     0.00
## "evaluate_call"             0.14    100.00      0.00     0.00
## "FUN"                       0.14    100.00      0.00     0.00
## "handle"                    0.14    100.00      0.00     0.00
## "in_dir"                    0.14    100.00      0.00     0.00
## "kmeans"                    0.14    100.00      0.00     0.00
## "knit"                      0.14    100.00      0.00     0.00
## "knit2wp"                   0.14    100.00      0.00     0.00
## "lapply"                    0.14    100.00      0.00     0.00
## "process_file"              0.14    100.00      0.00     0.00
## "process_group"             0.14    100.00      0.00     0.00
## "process_group.block"       0.14    100.00      0.00     0.00
## "source"                    0.14    100.00      0.00     0.00
## "timing_fn"                 0.14    100.00      0.00     0.00
## "try"                       0.14    100.00      0.00     0.00
## "tryCatch"                  0.14    100.00      0.00     0.00
## "tryCatchList"              0.14    100.00      0.00     0.00
## "tryCatchOne"               0.14    100.00      0.00     0.00
## "withCallingHandlers"       0.14    100.00      0.00     0.00
## "withVisible"               0.14    100.00      0.00     0.00
## ".C"                        0.10     71.43      0.10    71.43
## "do_one"                    0.10     71.43      0.00     0.00
## "unique"                    0.04     28.57      0.00     0.00
## "unique.matrix"             0.04     28.57      0.00     0.00
## "apply"                     0.02     14.29      0.02    14.29
## "as.list"                   0.02     14.29      0.02    14.29
## "alist"                     0.02     14.29      0.00     0.00
##
## $sample.interval
## [1] 0.02
##
## $sampling.time
## [1] 0.14
```

##### Use profvis to visualize performance

  * nice graphical output
  * native in RStudio (lots of [documentation](https://support.rstudio.com/hc/en-us/articles/218221837-Profiling-with-RStudio))

```r
p <- profvis({
  mean_loop = apply(some_data, 2, mean)
  mean_vec = colMeans(some_data)
  mean_manual = apply(some_data, 2, function(x) sum(x)/length(x))
  mean_manual_ultra = apply(some_data, 2, function(x){
    total = 0
    n = 0
    i = 1
    while(!is.na(x[i])) {
      total = total + x[i]
      n = n+1
      i = i+1
    }
    total/n
  })
})
htmlwidgets::saveWidget(p, "profile.html")

# Can open in browser from R
browseURL("profile.html")
```

##### Explore source code

**How to access function source code**
(if you didn't write the function yourself)

  1. Type the function name (without parentheses): `eigen`
  2. Find namespace and methods associated: `methods("princomp"); getAnywhere("princomp.default")`
  3. Use the package _pryr_ to search for C code on GitHub
  4. Download the entire package and explore the code

```r
svd
La.svd

# routes us to search on GitHub (which may or may not be helpful)
try(show_c_source(.Internal(La_svd(x))))
show_c_source(.Internal(mean(x)))

# download.packages("broman", repos = "https://cloud.r-project.org", destdir = getwd(), type = "source")
```

##### Trace objects copied

  * use tracemem() to track particular objects

```r
a <- letters[sample(10)]
tracemem(a)

## [1] "<0000000030B1AD78>"

a[1] <- "Z"

## tracemem[0x0000000030b1ad78 -> 0x0000000030b1b508]: eval eval withVisible withCallingHandlers doTryCatch tryCatchOne tryCatchList tryCatch try handle timing_fn evaluate_call <Anonymous> evaluate in_dir block_exec call_block process_group.block process_group withCallingHandlers process_file knit knit2wp eval eval withVisible source

b <- a[1:5]  # not copied
```

##### Memory

  * How much memory is being used? Note that R requests memory from your computer in big chunks then manages it itself.

```r
mem_used()

## 285 MB

object.size(x1) #base

## 8081384 bytes

object_size(x1) #pryr

## 8.08 MB

compare_size(x1) #between base R and pryr

##    base    pryr
## 8081384 8081384
```

Read the [documentation for pryr functions](https://www.rdocumentation.org/packages/pryr/versions/0.1.4) for more useful functions.

Now that we are all done, turn the JIT compiler back on:

```r
enableJIT(3)

## [1] 0
```

##### More Tips from _Advanced R_

These are designed to reduce internal checks

  1. read.csv(): specify known column types with colClasses.
  2. factor(): specify known levels with levels.
  3. cut(): don't generate labels with labels = FALSE if you don't need them, or, even better, use findInterval().
  4. unlist(x, use.names = FALSE) is much faster than unlist(x).
  5. interaction(): if you only need combinations that exist in the data, use drop = TRUE.

### Remember!

![](http://cougrstats.files.wordpress.com/2018/09/xkcd1205.png)
[xckd comic](https://xkcd.com/1205/)

_Top image from [HackerImage website](https://www.hackerearth.com/blog/python/faster-python-code/)._
