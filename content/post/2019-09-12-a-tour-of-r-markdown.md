---
title: A Tour of R Markdown
author: cougrstats
date: '2019-09-12'
categories:
  - Package Introductions
tags:
  - html
  - reproducibility
  - Rmarkdown
slug: a-tour-of-r-markdown
---

_By Matt Brousil_

Graduate students and other researchers often find themselves pasting figures or tables into Microsoft Word or other word processing software in order to share them with collaborators or PIs. Anyone who has tried to format text and images in the same Word document knows that this is a harrowing experience. Luckily, the `rmarkdown` package in R allows us to avoid this altogether. [R Markdown](https://rmarkdown.rstudio.com/) lets us combine narrative text (e.g., an Intro, Methods, Discussion) with code (R or some other languages), figures, and even interactive effects. Not only can this be more reliable than using software like Word, it is also more reproducible and allows us to explain the thoughts behind our scripts in the same file we use to flesh out the script.

R Markdown's capabilities are also very extensive. You can generate things like HTML, PDF, or Word reports; websites (like this blogs post!); slideshows; and interactive documents that use [Shiny](http://shiny.rstudio.com/).

In this walkthrough we'll take a look at the basics of R Markdown and finish up by generating an example report. It will look something like this:

![template_output_scrn](https://cougrstats.files.wordpress.com/2019/09/template_output_scrn.jpg)

# 1. Install

The first thing you'll need to do is install some packages. The process is
described by Yihui Xie [here](https://bookdown.org/yihui/rmarkdown/installation.html) but if you are an RStudio user, the general process is:

  1. Install the `rmarkdown` and `tinytex` packages.

  2. Use the function `tinytex::install_tinytex()` to give yourself the ability
to generate PDF documents via LaTex with R Markdown.

# 2. Basic overview

Before getting started, note that I am writing this walkthrough with RStudio users in mind. If you don't use RStudio, you should refer to Yihui Xie's [instructions](https://bookdown.org/yihui/rmarkdown/installation.html) again.

To get started making an R Markdown document, you can go to File > New File > R Markdown in RStudio. This will generate a pop-up that looks like this:

![new_rmd_popup](https://cougrstats.files.wordpress.com/2019/09/new_rmd_popup.jpg)

Provide it with a title for your document, the name of the author, and the type of document that you'd like to produce. HTML is typically the most reliable in my experience, and it often is best at formatting large tables and R console output.

Click OK and you should have a document that looks like this:

![default_rmd_scrn](https://cougrstats.files.wordpress.com/2019/09/default_rmd_scrn.jpg)

**Note that there are three parts to this document.**

The **top** of the document has a header that looks like this:

    ---
    title: "Untitled"
    author: "Matt Brousil"
    date: "September 11, 2019"
    output: html_document
    ---

This YAML text specifies some of the header info and formatting of your output document. There are guidelines on editing it [here](https://bookdown.org/yihui/bookdown/r-markdown.html).

Then there is **plain text** in the main document:

![plain_text_scrn](https://cougrstats.files.wordpress.com/2019/09/plain_text_scrn.jpg)

This is how you include narrative text within your document. It will be rendered pretty much as you see it in the final document, but there are options to do things like bold the text, add links, images, etc.

Lastly, there are **code chunks**. These will be in the R language for us, but you can include several other languages as well.

![code_chunk_scrn](https://cougrstats.files.wordpress.com/2019/09/code_chunk_scrn.jpg)

These chunks of code are run by R when you compile your final document. Each code chunk can also be run manually using the green arrow on the right side of the chunk.

Feel free to just delete everything in your new R Markdown document except the YAML header for our example. Then go ahead and save. You'll notice that the filetype for the R Markdown document is .Rmd

## How to create the output HTML or PDF files?

At any time you can have R generate the HTML or PDF file you're hoping to create by clicking the `Knit` button.

![knit_scrn](https://cougrstats.files.wordpress.com/2019/09/knit_scrn.jpg)

This also includes a dropdown that will let you switch between PDF, HTML, and Word outputs.

* * *

## Basic syntax

There are a few key things you'll want to know how to do in R Markdown.

### 2.1. Make headers

In R Markdown you can make headers using the # symbol. There are several tiers:

* * *

```r
 # The biggest header
```

# The biggest header

* * *

```r
 ## The second biggest header
```

## The second biggest header

* * *

```r
 ###### The smallest header
```

###### The smallest header

* * *

### 2.2. Write basic text

To write normal text, just type within the main document as you normally would in a word processing program. For example:

* * *

    The following section contains the results of my statistical analysis. After performing this analysis I found a significant relationship between my variable of interest and the experimental treatments.

The following section contains the results of my statistical analysis. After performing this analysis I found a significant relationship between my variable of interest and the experimental treatments.

* * *

_However_, do note that you'll need to include two spaces at the end of a line to create line breaks in your raw text. This is easily overlooked.

### 2.3. Format text

You can bold and italicize text using asterisks (*):

* * *

     **bold text**

**bold text**

* * *

     *italic text*

_italic text_

* * *

You can also do other things such as

     super^script^

superscript

and adding links:

     [the text to display](www.google.com)

[the text to display](http://www.google.com)

* * *

###

### 2.4. Add in code!

Here's the fun part! Now that we know how to insert and format text, you can also add in chunks of R code. Go to Code > Insert Chunk in RStudio to insert a chunk. You can also just type out a chunk manually using backticks and {r} to indicate R language.

    ```{r}
    print("My first R Markdown code")
    ```

R will show both the code and its result, by default.

```r
print("My first R Markdown code")

## [1] "My first R Markdown code"
```

In some cases you might want to include code but not print it out in the final document, e.g. including only the resulting figure or result. You can hide the raw code using `echo = FALSE`:

    ```{r echo=FALSE}
    print("My first R Markdown code")
    ```

    ## [1] "My first R Markdown code"

Code can be inserted into your narrative text (e.g. in a sentence) by using backticks with the letter 'r':

     The iris dataset contains the following column names: `r names(iris)`.

The iris dataset contains the following column names: Sepal.Length, Sepal.Width, Petal.Length, Petal.Width, Species.

* * *

# 3. Report example

Now let's put the topics from the above section together! Below I provide a very brief template (and its knitted output) showing how you might write up a post-analysis report to share with an advisor or PI. There's plenty to customize, but this is a skeleton that might be of use. You can download this script as a .Rmd file [here](https://drive.google.com/drive/folders/1y5cu0Mh39RcdXUzqQP-yV_-2g9VhUTQ9?usp=sharing) along with the associated dataset.

* * *

#### The script:

    # Update on my thesis progress

    ```{r echo=FALSE, message=FALSE, warning=FALSE}
    # This chunk won't be printed: We're just loading a package, so it might not be something that we want to have take up space in the final doc.
    library(tidyverse)
    library(ggpubr)
    library(knitr)
    ```

    ## New data
    I recently finished collecting additional data for my research project. In this document I will load it in and explore it.

    1. Load the data
    ```{r, }
    new_data <- read.csv(file = "new_data.csv")
    ```

    2. Here's how the newly collected data are formatted
    ```{r}
    str(new_data)

    sample_n(tbl = new_data, size = 20)
    ```

    3. Visualize the new data
    ```{r}
    ggplot(data = new_data) +
      geom_point(aes(x = season, y = growth, color = season))
    ```

    4. I ran a statistical test on the new data. Here are the results
    ```{r}
    new_anova <- lm(formula = growth ~ season, data = new_data)

    new_anova % kable()
    ```

    5. Now I plot the significance to illustrate the results
    ```{r}
    ggplot(data = new_data,
           aes(x = season, y = growth, fill = season)) +
      geom_boxplot() +
      stat_compare_means(comparisons = list(c("spring", "summer"),
                                            c("spring", "fall"),
                                            c("summer", "fall"))) +
      stat_compare_means(method = "anova")
    ```

#### The knitted output:

# Update on my thesis progress

## New data

I recently finished collecting additional data for my research project. In this document I will load it in and explore it.

  1. Load the data

```r
new_data <- read.csv(file = "new_data.csv")
```

  *

    2. Here's how the newly collected data are formatted

    str(new_data)

    ## 'data.frame':    99 obs. of  2 variables:
    ##  $ growth: num  100.9 96.3 97.3 102.5 101.3 ...
    ##  $ season: Factor w/ 3 levels "fall","spring",..: 2 2 2 2 2 2 2 2 2 2 ...

    sample_n(tbl = new_data, size = 20)

    ##       growth season
    ## 1  104.28253 summer
    ## 2  101.37707   fall
    ## 3   97.43616   fall
    ## 4   90.31059   fall
    ## 5  104.50746 summer
    ## 6  107.02942   fall
    ## 7  102.20002   fall
    ## 8  107.16437   fall
    ## 9  104.98256 summer
    ## 10 108.31785 summer
    ## 11 107.11215 summer
    ## 12  97.32140 spring
    ## 13 101.03978   fall
    ## 14 101.27251   fall
    ## 15  97.98659 spring
    ## 16  97.32749 summer
    ## 17 101.27748   fall
    ## 18  92.18833 spring
    ## 19  98.10998 summer
    ## 20 102.41306 summer

  3. Visualize the new data

```r
ggplot(data = new_data) +
  geom_point(aes(x = season, y = growth, color = season))
```

![point_plot](https://cougrstats.files.wordpress.com/2019/09/point_plot.png)

  4. I ran a statistical test on the new data. Here are the results

    new_anova <- lm(formula = growth ~ season, data = new_data)
    new_anova % kable()

<table >

<tr >

Df
Sum Sq
Mean Sq
F value
Pr(>F)
</tr>

<tbody >
<tr >

<td align="left" >season
</td>

<td align="right" >2
</td>

<td align="right" >233.8816
</td>

<td align="right" >116.94082
</td>

<td align="right" >5.015241
</td>

<td align="right" >0.008479
</td>
</tr>
<tr >

<td align="left" >Residuals
</td>

<td align="right" >96
</td>

<td align="right" >2238.4406
</td>

<td align="right" >23.31709
</td>

<td align="right" >NA
</td>

<td align="right" >NA
</td>
</tr>
</tbody>
</table>

  5.

    5. Now I plot the significance to illustrate the results

    ggplot(data = new_data,
           aes(x = season, y = growth, fill = season)) +
      geom_boxplot() +
      stat_compare_means(comparisons = list(c("spring", "summer"),
                                            c("spring", "fall"),
                                            c("summer", "fall"))) +
      stat_compare_means(method = "anova")

![boxplot](https://cougrstats.files.wordpress.com/2019/09/boxplot.png)

* * *

# 4. References:

  * <https://bookdown.org/yihui/rmarkdown/>

  * <https://bookdown.org/yihui/bookdown/r-markdown.html>

  * <https://rmarkdown.rstudio.com/>

  * <http://www.sthda.com/english/articles/24-ggpubr-publication-ready-plots/76-add-p-values-and-significance-levels-to-ggplots/>

#### Cheat sheets:

Additionally, there are some great cheat sheets available for R Markdown:

  * <https://www.rstudio.com/wp-content/uploads/2015/03/rmarkdown-reference.pdf>

  * <https://github.com/rstudio/cheatsheets/raw/master/rmarkdown-2.0.pdf>
