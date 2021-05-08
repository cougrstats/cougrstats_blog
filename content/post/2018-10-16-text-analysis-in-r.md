---
title: Text Analysis in R
author: Michael F. Meyer
date: '2018-10-16'
slug: text-analysis-in-r
---

_By Michael F. Meyer_

**For the reader**:

This document is to serve as a tutorial for the [R Working Group](https://cereo.wsu.edu/r-working-group/) at Washington State University.

For more information, please contact [Michael F. Meyer](https://labs.wsu.edu/hampton/people/michael-meyer/)

# For BeginneRs

There are three main takeaways from this tutorial. You will have learned:

  1. How to read in a text file and convert a text file to a dataframe.

  2. `dcast()` from the `reshape2` package.

  3. How to make a `for` loop.

**Initial Web of Science (WOS) Search**

Within the WOS interface we conducted an initial topic (TS) search on 08 October 2018:

**TS = "(microplastic* AND _system_" AND TS = "marine OR freshwater OR terrestrial"**

This initial search produced 370 records, and then we used WOS filters to select only primary articles in English that were tagged as the environmentally relevant subject categories. These filters produced 307 records.

We then downloaded full citations twice (one with references and one without) as text files from the WOS interface.

**Import WOS Records into R**

This R script starts with loading the necessary R packages: [reshape2](https://cran.r-project.org/web/packages/reshape2/index.html), [tidyr](https://cran.r-project.org/web/packages/tidyr/index.html), [dplyr](https://cran.r-project.org/web/packages/dplyr/index.html), and [ggplot2](https://cran.r-project.org/web/packages/ggplot2/index.html).

```r
library(reshape2)
library(ggplot2)
library(tidyr)
library(dplyr)
```

The text files were imported using `readLines`. Unnecessary header rows were removed using the command `as.character(data.frame(savedrecs.orig)[-c(1:2),])`.

```r
# Import each text file
savedrecs.orig <- readLines(con <- file("savedrecs_full_mfm_20181008.txt"))

# Remove the first two rows of each original file
savedrecs <- as.character(data.frame(savedrecs.orig)[-c(1:2), ])
```

Next, we convert the `savedrecs` object into a dataframe with extracted information for publication type (PT), authors (AU), abstract (AB), title (TI), publication name (SO), DOI (DI), publication year (PY), subject category (SC), and Web of Science category (WC). When downloading a full citation report, other WOS field tags can be selected, such as country (CU).

```r
# Select fields pertaining to the desired WOS tag. Use general pattern of '*XX *|* XX*' to select
# multiple fields with a grep statement
which <- grep("*PT *|*AU *|*AB *|*TI *|*SO *|*DI *|*PY *|*SC *|*WC *", savedrecs)
# Filter saved recs by the indexed WOS fields in 'which'
savedrecs <- savedrecs[which]
# Make sure savedrecs is all characters
savedrecs <- as.character(savedrecs)
# Isolate the savedrecs WOS field
bibtype <- as.character(substr(savedrecs, 1, 2))
# Isolate the descriptions for each of WOS tags
desc <- substr(savedrecs, 4, nchar(savedrecs))
# Build an index for each item
index <- rep(0, length(savedrecs))
# Create a df of index, WOS tag, and description
df <- data.frame(index, bibtype, desc)
# Find the index for differing publications
new <- which(df$bibtype == "PT")
newindex <- 0
# Now, we build a new index where all indices are for a given pub
for (i in 1:length(df[, 1])) {
    if (i %in% new) {
        newindex <- newindex + 1
    }
    df$index[i] <- newindex
}

# Change bibtype to character, remove rows where bibtype is blank
df$bibtype <- as.character(df$bibtype)
df <- df[which(df$bibtype != "  "), ]

# Pivot the long table format to wide format
df.wide <- dcast(df, index ~ bibtype)
```

The next section specifies focal terms that were used in our analysis of WOS abstracts. We were interested in particular ecosystems where microplastic presence, abundance, and biological effects were studied.

```r
focal_samples <- c("fish", "mussel", "plant", "invertebrate", "clam", "plankton", "oyster")

systems <- c("marine", "ocean", "estuary", "gulf", "sea", "gyre", "freshwater", "river", "stream", "lake",
    "soil", "terrestrial", "forest")

marine <- c("marine", "ocean", "estuary", "gulf", "sea", "gyre")

freshwater <- c("freshwater", "river", "stream", "lake")

terrestrial <- c("soil", "terrestrial", "forest")
```

**Systems**

**Identify abstracts that contain the focal systems**

The remaining sections identify abstracts that contain system-specific focal terms and count them by year and group. Because abstracts may contain multiple focal systems, the sum of proportions across all focal systems for a year may sometimes exceed one.

**Iterate through abstracts for focal terms**

We use a `for loop` to iterate through each abstract and focal system. The resulting data frame contains a column `ABcontains` that identifies presence/absence of a given system.

```r
## Proportion of systems across all discplines . First copy the wide dataframe
df_system <- df.wide
# Create an empty character vector where we will put focal terms
df_system$term_system <- ""
# Create an empty numeric column to count number of times a term appears
df_system$ABcontains <- 0
# Convert Publication Year to a numeric
df_system$PY <- as.numeric(df_system$PY)
# Copy this dataframe to a 'final data frame version'
df_system_final <- df_system
# For loop to iterate through each focal system in character vector
for (i in 1:length(systems)) {
    # Assign temporary variable for a particular system
    termi <- systems[i]
    # Create a temporary dataframe
    dfi <- df_system
    # Search for instances of focal system in the abstract
    whichi <- grep(termi, dfi$AB, ignore.case = TRUE, fixed = TRUE)
    # Create a reference to which system is present within the abstract
    dfi$term <- termi
    # Assign a value of one to abstracts that contain a given system
    dfi$ABcontains[whichi] <- 1
    # Start the final dataframe if this is the first iteration through the for loop
    if (i == 1) {
        df_system_final <- dfi
    }
    # Combine the final data frame with the temporary after the first for loop iteration
    if (i > 1) {
        df_system_final <- rbind(df_system_final, dfi)
    }
}
# Set factor levels for the focal system
df_system_final$term <- factor(df_system_final$term, levels = systems)

# I added a step that makes sure ABcontains only has a value of 1 or 0.
df.system.binary <- df_system_final
# In most, if not all cases, this step is redundant. It is included as a fail-safe.
for (i in length(df.system.binary$ABcontains)) {
    if (df.system.binary$ABcontains[i] != 0) {
        df.system.binary$ABcontains[i] = 1
    }
}
```

**Add the system type column**

We can then build a system type column using serial mutate and ifelse statements. All of our successive analyses will use the system type column.

```r
df.system.binary$SYSTEM <- NA
df.system.binary <- df.system.binary %>% mutate(SYSTEM = ifelse(term %in% marine, "marine", NA), SYSTEM = ifelse(term %in%
    freshwater, "freshwater", SYSTEM), SYSTEM = ifelse(term %in% terrestrial, "terrestrial", SYSTEM))
```

**Enumeration by focal system**

Next, we calculate the number of abstracts in a given year and system type in two steps.

We need to flag an individual abstract as containing an instance of a given pharmceutical class. A given abstract is assigned a value of 1 if it mentions a pharmaceutical class.

```r
df.system.wo.na.part1 <- df.system.binary %>% # Group by abstract Year, then Title, then Pharmaceutical Class
group_by(PY, TI, SYSTEM) %>% # Sum the number of times a class was references per abstract
summarize(TOTAL = sum(ABcontains)) %>% # If greater than one, replace with one, so we have a presence/absence
mutate(TOTAL = ifelse(TOTAL > 1, 1, TOTAL))
factor(x$var1, levels = c("high", "med", "low"))

## Error in factor(x$var1, levels = c("high", "med", "low")): object 'x' not found
```

We sum the number of distinct abstracts that mention a given pharmaceutical class in a given year.

```r
df.system.wo.na.part2 <- df.system.wo.na.part1 %>% # Select studies that have at least one system referenced
filter(TOTAL == 1) %>% # Group by abstract year and system type
group_by(PY, SYSTEM) %>% # Count the number of titles that reference a given system type
summarize(COUNT.PUBS = n_distinct(TI))
```

We then calculate the number of abstracts that mentioned a particular system type at all in the abstract. This count excludes studies that did not contain any system type names in the abstract. For this reason, we only consider studies that mention a specific system in the abstract.

```r
DI.count.total <- df.system.wo.na.part1 %>%
  #Select all studies that reference at least one system type
  filter(TOTAL == 1) %>%
  #Group by abstract year
  group_by(PY) %>%
  #Sum the number of titles in a given year
  summarize(TOTAL.TI = n_distinct(TI))
```

Finally, we take the proportion of the total number of abstracts mentioning a particular system in a given year normalized by the total number of abstracts mentioning at least one type of system in a year.

```r
dataplot.system <- full_join(df.system.wo.na.part2, DI.count.total)
dataplot.system <- dataplot.system %>%
  #Group by abstract year and pharmaceutical class
  group_by(PY, SYSTEM) %>%
  #Calculate proportions for analysis
 summarize(PROP.COUNT = COUNT.PUBS/TOTAL.TI) %>%
  as.data.frame()
```

We can then produce a plot of proportions over time and by system type.

```r
dataplot.system <- dataplot.system %>% spread(SYSTEM, PROP.COUNT) %>% gather(SYSTEM, PROP.COUNT, -PY) %>%
    mutate(PROP.COUNT = ifelse(is.na(PROP.COUNT), 0, PROP.COUNT))
```

<table style="margin-left:auto;margin-right:auto;" class="table table-striped table-hover table-condensed table-responsive" >

<tr >

freshwater
marine
terrestrial
</tr>

<tbody >
<tr >

<td style="text-align:left;" >Min.
</td>

<td style="text-align:right;" >0.0000000
</td>

<td style="text-align:right;" >0.8000000
</td>

<td style="text-align:right;" >0.0000000
</td>
</tr>
<tr >

<td style="text-align:left;" >1st Qu.
</td>

<td style="text-align:right;" >0.2666667
</td>

<td style="text-align:right;" >0.8877551
</td>

<td style="text-align:right;" >0.0000000
</td>
</tr>
<tr >

<td style="text-align:left;" >Median
</td>

<td style="text-align:right;" >0.3000000
</td>

<td style="text-align:right;" >0.9444444
</td>

<td style="text-align:right;" >0.0454545
</td>
</tr>
<tr >

<td style="text-align:left;" >Mean
</td>

<td style="text-align:right;" >0.3319045
</td>

<td style="text-align:right;" >0.9258420
</td>

<td style="text-align:right;" >0.0502595
</td>
</tr>
<tr >

<td style="text-align:left;" >3rd Qu.
</td>

<td style="text-align:right;" >0.4062500
</td>

<td style="text-align:right;" >1.0000000
</td>

<td style="text-align:right;" >0.0888889
</td>
</tr>
<tr >

<td style="text-align:left;" >Max.
</td>

<td style="text-align:right;" >1.0000000
</td>

<td style="text-align:right;" >1.0000000
</td>

<td style="text-align:right;" >0.1530612
</td>
</tr>
</tbody>
</table>

```r
### The lines below build the final plot
dataplot.system$SYSTEM <- factor(dataplot.system$SYSTEM, levels = c("marine", "freshwater", "terrestrial"))

yearplot.systems <- ggplot(dataplot.system, aes(x = as.factor(PY), y = PROP.COUNT, group = SYSTEM)) +
    geom_point(size = 4, color = "grey60") + ylab("Proportion of Abstracts") + xlab("Publication Year") +
    theme_minimal() + facet_wrap(~SYSTEM, drop = FALSE) + # scale_x_continuous(limits = c(1997, 2017)) +
theme(legend.position = "none") + theme(plot.title = element_text(size = 20), strip.text.x = element_text(size = 20),
    strip.background = element_rect(fill = "white"), panel.background = element_rect(color = "black"),
    axis.title = element_text(size = 20), axis.text.x = element_text(size = 20), axis.text.y = element_text(size = 20),
    axis.title.y = element_text(margin = margin(0, 20, 0, 0)), axis.title.x = element_text(margin = margin(20,
        0, 0, 0)))
yearplot.systems
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-12-1.png)

**Multiple systems**

This next section tabulates how many systems are included in each abstract The structure is similar to that of the above code with the exception that we add the number of dataplot.system for a given abstract and year.

```r
richness.orig <- df.system.binary %>% # Group by abstract year, then title, then system type
group_by(PY, TI, SYSTEM) %>% # Sum the number of systems for a given system type
summarize(TOTAL = sum(ABcontains)) %>% # Replace summed values with a 1 so we have presence/absence data of the system type
mutate(TOTAL = ifelse(TOTAL > 1, 1, TOTAL)) %>% # Filter for studies that mention at least one system type
filter(TOTAL >= 1) %>% # Remove grouping
ungroup() %>% # Group by abstract year and title
group_by(PY, TI) %>% # Sum the number of system types for a given abstract
summarize(RICHNESS = sum(TOTAL)) %>% # Remove grouping
ungroup() %>% # Group by abstract year and RICHNESS
group_by(PY, RICHNESS) %>% # Sum the number of unique titles
mutate(UNIQUE_TI = n_distinct(TI))

system.div <- ggplot(richness.orig, aes(as.factor(PY), as.factor(RICHNESS), size = UNIQUE_TI)) + geom_point(shape = 21,
    colour = "grey40", fill = "grey80", stroke = 2) + scale_size("Number of Abstracts", range = c(10,
    35), breaks = c(25, 50, 75, 100, 125, 150, 175, 200)) + geom_text(aes(label = UNIQUE_TI), size = 6,
    color = "black") + ylab("Number of Systems in an Abstract") + xlab("Publication Year") + theme_minimal() +
    theme(legend.position = "none", panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(color = "black", size = 1), plot.title = element_text(size = 20),
        strip.text.x = element_text(size = 20), axis.title = element_text(size = 20), axis.text.x = element_text(size = 20,
            angle = 45, vjust = 0.5), axis.text.y = element_text(size = 20), axis.title.y = element_text(margin = margin(0,
            20, 0, 0)), axis.title.x = element_text(margin = margin(20, 0, 0, 0)))
system.div
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-13-1.png)

**Using Bibliometrix for text analysis**

```r
library(bibliometrix)

### The following lines replicate what we did above within base R. These data frames though are not
### necessarily reconcilable. We will bring in the full records with references for this example.
df.orig <- readFiles("savedrecs_withRefs_mfm_20181008.txt")
df.current <- convert2df(df.orig, dbsource = "isi", format = "plaintext")

##
## Converting your isi collection into a bibliographic dataframe
##
## Articles extracted   100
## Articles extracted   200
## Articles extracted   300
## Articles extracted   307
## Done!
##
##
## Generating affiliation field tag AU_UN from C1:  Done!

plot(x = results, k = 10, pause = FALSE)
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-1.png)![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-2.png)![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-3.png)![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-4.png)![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-5.png)

```r
### Bibliometrix can help us look at author collaboration networks. Just put in the Bibliometrix
### formatted dataframe... Then the type of analysis you want to perform... The network you are trying
### to build... And what the separator is in your dataframe.
NetMatrix <- biblioNetwork(df.current, analysis = "collaboration", network = "authors", sep = ";")

### Bibliometrix 2.0.0 offers more flexibility with respect to plotting and metrix.

net <- networkPlot(NetMatrix, normalize = "salton", weighted = NULL, n = 100, Title = "Authors' Coupling",
    type = "kamada", size = 5, size.cex = T, remove.multiple = TRUE, labelsize = 0.8, label.n = 10, label.cex = F)
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-6.png)

```r
### Similar formulas can be used to build co-citatin networks Two papers are considerd to be co-cited
### if a third paper cites both of them. Remember to change the network to the references.
NetMatrix <- biblioNetwork(df.current, analysis = "co-citation", network = "references", sep = ";")

net <- networkPlot(NetMatrix, normalize = "salton", weighted = NULL, n = 10, Title = "Co-citation network",
    type = "fruchterman", size = 5, size.cex = T, remove.multiple = TRUE, labelsize = 0.8, label.n = 10,
    label.cex = F)
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-7.png)

```r
### We can also look at a conceptual structure plot, where we are basically looking at associations
### between common terms.
CS <- conceptualStructure(df.current, field = "ID", method = "MCA", minDegree = 15, k.max = 8, stemming = FALSE,
    labelsize = 10, documents = 10)
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-8.png)![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-9.png)![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-10.png)

```r
### We can also look at the direct historical association with a given publication by creating a
### historical direct citation network.
histResults <- histNetwork(df.current, min.citations = 20, sep = ".  ")

## Articles analysed   88

net <- histPlot(histResults, n = 10, size = 10, labelsize = 5, size.cex = TRUE, arrowsize = 0.5, color = TRUE)
```

![](http://cougrstats.files.wordpress.com/2018/10/unnamed-chunk-14-11.png)

```r
##
##  Legend
##
##                                              Paper                             DOI Year LCS GCS
## 2008 - 1      BROWNE MA, 2008, ENVIRON SCI TECHNOL               10.1021/ES800249A 2008  75 393
## 2012 - 5     VON MOOS N, 2012, ENVIRON SCI TECHNOL               10.1021/ES302332W 2012  58 216
## 2013 - 7                BROWNE MA, 2013, CURR BIOL       10.1016/J.CUB.2013.10.012 2013  41 192
## 2013 - 10 VAN CAUWENBERGHE L, 2013, ENVIRON POLLUT    10.1016/J.ENVPOL.2013.08.013 2013  45 198
## 2013 - 14        COLE M, 2013, ENVIRON SCI TECHNOL               10.1021/ES400663F 2013  85 325
## 2014 - 24           FREE CM, 2014, MAR POLLUT BULL 10.1016/J.MARPOLBUL.2014.06.001 2014  46 153
## 2014 - 26          LECHNER A, 2014, ENVIRON POLLUT    10.1016/J.ENVPOL.2014.02.006 2014  35 124
## 2015 - 34        COLE M, 2015, ENVIRON SCI TECHNOL         10.1021/ACS.EST.5B04099 2015  41  49
## 2015 - 43       KLEIN S, 2015, ENVIRON SCI TECHNOL         10.1021/ACS.EST.5B00492 2015  32  93
## 2015 - 45            AVIO CG, 2015, ENVIRON POLLUT    10.1016/J.ENVPOL.2014.12.021 2015  33 124
```
