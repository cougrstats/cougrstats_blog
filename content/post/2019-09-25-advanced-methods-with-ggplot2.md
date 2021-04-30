---
title: Advanced methods with ggplot2
author: cougrstats
date: '2019-09-25'
categories:
  - Package Introductions
tags:
  - cowplot
  - ggplot2
  - ggpubr
  - ggrepel
  - tidyverse
slug: advanced-methods-with-ggplot2
---

_By Matt Brousil_

This walkthrough will cover some advanced ways of working with `ggplot2`. There are a lot of functions and plotting options available in `ggplot2`, but here I'll be showing a couple of examples of ways to extend your `ggplot2` usage with additional packages. This post is less about mind-blowing images as it is useful ways to produce and modify figures for your research.

## Overview

This post is going to cover a couple of main points for working with `ggplot2`. They include:

  * Changing up color themes with `viridis` and labeling points with `ggrepel`

  * Generating multiple plots without copying and pasting code

  * Arranging multiple plots into one figure with a shared legend using `ggpubr`

  * Creating insets in a plot

**Quick notes**:

  * I'll be using pipes (`%>%`) in this post. You can find more info on their usage [here](https://uc-r.github.io/pipe) if you haven't encountered them before

  * I assume you have some prior `ggplot2` experience! Alli Cramer's [Introduction to R](https://cougrstats.wordpress.com/2018/01/25/introduction-to-r-a-roadmap/) post discusses some basic `ggplot2` commands if you need them

## The walkthrough

First off, we'll load the following packages:

```r
library(tidyverse)
library(ggpubr)
library(ggrepel)
library(lubridate)
library(tigris)
library(sf)
library(cowplot)
```

Next, we'll load in data exported from the [iNaturalist](https://www.inaturalist.org/home) website. The data are observations of animals, plants, fungi, and other forms of life from Whitman County, WA. You can download the file [here](https://drive.google.com/drive/folders/1D57KUyAjU9eLClktBdjAwuGpWh_kEdnF?usp=sharing).

```r
whitman_nature <- read.csv(file = "whitman_inaturalist.csv",
                           stringsAsFactors = FALSE)
```

Most of the variables in this dataset are related to the taxonomic IDs of its observations.

```r
str(whitman_nature)

## 'data.frame':    3306 obs. of  32 variables:
##  $ observed_on           : chr  "2012-06-07" "2012-08-13" "2012-08-13" "2007-08-31" ...
##  $ quality_grade         : chr  "research" "research" "research" "research" ...
##  $ latitude              : num  46.7 46.7 46.7 47 46.7 ...
##  $ longitude             : num  -117 -117 -117 -117 -117 ...
##  $ coordinates_obscured  : chr  "false" "false" "false" "false" ...
##  $ species_guess         : chr  "Black-billed Magpie" "Gray Hairstreak" "Great Mullein" "Rock Wren" ...
##  $ scientific_name       : chr  "Pica hudsonia" "Strymon melinus" "Verbascum thapsus" "Salpinctes obsoletus" ...
##  $ common_name           : chr  "Black-billed Magpie" "Gray Hairstreak" "great mullein" "Rock Wren" ...
##  $ iconic_taxon_name     : chr  "Aves" "Insecta" "Plantae" "Aves" ...
##  $ taxon_id              : int  143853 50931 59029 7486 143853 9744 14823 2969 1409 13858 ...
##  $ taxon_kingdom_name    : chr  "Animalia" "Animalia" "Plantae" "Animalia" ...
##  $ taxon_phylum_name     : chr  "Chordata" "Arthropoda" "Tracheophyta" "Chordata" ...
##  $ taxon_subphylum_name  : chr  "Vertebrata" "Hexapoda" "Angiospermae" "Vertebrata" ...
##  $ taxon_superclass_name : chr  "" "" "" "" ...
##  $ taxon_class_name      : chr  "Aves" "Insecta" "Magnoliopsida" "Aves" ...
##  $ taxon_subclass_name   : chr  "" "Pterygota" "" "" ...
##  $ taxon_superorder_name : chr  "" "" "" "" ...
##  $ taxon_order_name      : chr  "Passeriformes" "Lepidoptera" "Lamiales" "Passeriformes" ...
##  $ taxon_suborder_name   : chr  "" "" "" "" ...
##  $ taxon_superfamily_name: chr  "" "Papilionoidea" "" "" ...
##  $ taxon_family_name     : chr  "Corvidae" "Lycaenidae" "Scrophulariaceae" "Troglodytidae" ...
##  $ taxon_subfamily_name  : chr  "" "Theclinae" "" "" ...
##  $ taxon_supertribe_name : chr  "" "" "" "" ...
##  $ taxon_tribe_name      : chr  "" "Eumaeini" "" "" ...
##  $ taxon_subtribe_name   : chr  "" "Eumaeina" "" "" ...
##  $ taxon_genus_name      : chr  "Pica" "Strymon" "Verbascum" "Salpinctes" ...
##  $ taxon_genushybrid_name: logi  NA NA NA NA NA NA ...
##  $ taxon_species_name    : chr  "Pica hudsonia" "Strymon melinus" "Verbascum thapsus" "Salpinctes obsoletus" ...
##  $ taxon_hybrid_name     : chr  "" "" "" "" ...
##  $ taxon_subspecies_name : chr  "" "" "" "" ...
##  $ taxon_variety_name    : chr  "" "" "" "" ...
##  $ taxon_form_name       : chr  "" "" "" "" ...
```

### 1. Some tweaks to a basic plot

Let's explore the dataset. For example, we might be interested in getting a sense of how common each group of organisms (plants, insects, mammals, etc.) is throughout the year. But before plotting we should prep the dataset a bit:

    whitman_interest %
      # Remove missing dates
      filter(observed_on != "",
             # Focus on just groups with a lot of observations
             iconic_taxon_name %in% c("Insecta", "Plantae", "Mammalia",
                                      "Fungi", "Reptilia", "Amphibia")) %>%
      # Extract month and year data from the observed_on date
      mutate(month_obs = month(observed_on, label = TRUE),
             year_obs = year(observed_on)) %>%
      # Count the number of observations by year, month, and taxonomic group
      count(year_obs, month_obs, iconic_taxon_name) %>%
      # Divide up the data by deciles so we can pick out times with peak sighting counts
      mutate(n_tile = ntile(x = n, n = 10),
             # Create a label denoting the data in the top decile of values
             label = if_else(condition = n_tile == 10,
                             true = as.character(year_obs), false = ""))

    head(whitman_interest)

    ## # A tibble: 6 x 6
    ##   year_obs month_obs iconic_taxon_name     n n_tile label
    ##
    ## 1     1993 Jun       Plantae              10      8 ""
    ## 2     1993 Jul       Plantae               1      1 ""
    ## 3     1997 Jun       Plantae               1      1 ""
    ## 4     1998 Mar       Mammalia              1      1 ""
    ## 5     2006 Jun       Plantae               1      1 ""
    ## 6     2006 Sep       Mammalia              1      1 ""

Now we'll plot what we've created above. Here's a basic start:

```r
ggplot(data = whitman_interest, aes(x = month_obs, y = n)) +
  geom_point(aes(color = iconic_taxon_name)) +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45)) +
  ylab(label = "Count") +
  xlab(label = "Month observed")
```

![basic_plot](https://cougrstats.files.wordpress.com/2019/09/basic_plot.png)

This plot is fine, but there's more we can do with it. I've made a few changes below:

  * We use `geom_text_repel()` from `ggrepel` to place labels that don't overlap one another

  * We use `scale_color_viridis_d()` from `ggplot2` to use a colorblind-friendly color palette

  * `geom_jitter()` adds some random variation to the point placement so that we don't have points overlapping one another

The [viridis](https://ggplot2.tidyverse.org/reference/scale_viridis.html) scale provides a colorblind-friendly palette to the `color` aesthetic we're using. Use `scale_color_viridis_d()` for discrete variables and `scale_color_viridis_c()` for continuous.

```r
ggplot(data = whitman_interest, aes(x = month_obs, y = n)) +
  geom_jitter(aes(color = iconic_taxon_name)) +
  geom_text_repel(aes(label = label)) +
  scale_color_viridis_d(name = "Taxon name") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45)) +
  ylab(label = "Count") +
  xlab(label = "Month observed")
```

![repel_plot](https://cougrstats.files.wordpress.com/2019/09/repel_plot.png)

This plot now shows the counts of each taxonomic group during every month of the year in Whitman County. We can see that people generally report more observations during the middle of the year, but also more recent years have higher counts than earlier years (based on the labels). A label is placed for the month-species combinations that have counts in the highest 10%.

Note that if we want, we can change the `viridis` color palette and add line segments to the labels from `ggrepel`. As an example, we can change the color [palette](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html) to "plasma" and add thin grey line segments. Here I also change `geom_jitter()` to `geom_point()` because the jitter doesn't line up with the `geom_text_repel()` segments well.

```r
ggplot(data = whitman_interest, aes(x = month_obs, y = n)) +
  geom_point(aes(color = iconic_taxon_name)) +
  geom_text_repel(aes(label = label),
                  segment.size = 0.2, # Line width
                  min.segment.length = 0, # All labels have lines
                  nudge_x = 0.9, # Nudge x starting point of labels
                  segment.color = "gray") + # Line color
  scale_color_viridis_d(name = "Taxon name", option = "plasma") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45)) +
  ylab(label = "Count") +
  xlab(label = "Month observed")
```

![segment_repel_plot](https://cougrstats.files.wordpress.com/2019/09/segment_repel_plot.png)

### 2. What if we wanted to generate a plot for each group?

The plot above is generally informative, but what if you wanted to break it out so that you had a separate plot for each taxonomic group (i.e., insects, plants, etc.)?

It might look like this:

```r
ggplot(data = whitman_interest %>%
         filter(iconic_taxon_name == "Plantae"),
       aes(x = month_obs, y = n)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(aes(color = factor(year_obs))) +
  scale_color_viridis_d(name = "Year") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45)) +
  ggtitle(label = "Plantae") +
  ylab(label = "Count") +
  xlab(label = "Month observed")
```

![taxa_template_plot](https://cougrstats.files.wordpress.com/2019/09/taxa_template_plot.png)

This gives us a plants plot, but none of the other taxonomic groups. If you're like me, you've got a few scripts lying around where you just copied and pasted the same code a bunch of times to make multiple figures. Luckily there's a simpler, more reliable way for us to produce plots for each taxonomic group in this case.

Recall that we have the column `iconic_taxon_name` with the values **Plantae, Mammalia, Insecta, Fungi, Reptilia, Amphibia**.

Using the function `map()` from the package `purrr`, we can produce a new plot for each value in a vector that we specify. In this case, we'll supply a vector of the unique values of `iconic_taxon_name` and tell R to use each value (e.g. "Plantae") to filter the dataset and create a plot title:

##### The basic structure of `purrr::map()`:

    map(.x = , # Here we supply the vector of values (in this case taxa names)
        .f = ~ ) # Here we supply the function we want to feed those values into

We'll want to provide a function that can use any of the inputs in our taxa vector. Instead of writing the taxa name (e.g. "Plantae") in our function, we'll replace it with `.x`, which is the name of the first argument in the `map()` function:

```r
whitman_interest %>%
              filter(iconic_taxon_name == .x) %>%
              ggplot(aes(x = month_obs, y = n)) +
              geom_boxplot(outlier.shape = NA) +
              geom_jitter(aes(color = factor(year_obs))) +
              scale_color_viridis_d(name = "Year") +
              scale_x_discrete(drop = FALSE) + # Include months with no data
              theme_bw() +
              theme(axis.text.x = element_text(angle = 45)) +
              ggtitle(label = .x) +
              ylab(label = "Count") +
              xlab(label = "Month observed")
```

Now if we combine our vector of taxa names and this function, we get a full `map()` call. Note the use of the `~` before the function call:

    figs %
                  filter(iconic_taxon_name == .x) %>%
                  ggplot(aes(x = month_obs, y = n)) +
                  geom_boxplot(outlier.shape = NA) +
                  geom_jitter(aes(color = factor(year_obs))) +
                  scale_color_viridis_d(name = "Year", drop = FALSE) +
                  scale_x_discrete(drop = FALSE) +
                  theme_bw() +
                  theme(axis.text.x = element_text(angle = 45)) +
                  ggtitle(label = .x) +
                  ylab(label = "Count") +
                  xlab(label = "Month observed"))

The `figs` object is now a list of figures for all six of our taxa!

```r
typeof(figs)

## [1] "list"

figs
```

[gallery ids="331,330,328,325,333,322" columns="2"]

#### 3. Combining figures into one plot

Now that we have all six figures we want, we might want to combine them into a single plot. This is possible using `ggarrange()` from `ggpubr`. We just need to supply it our plot list (`figs`). We can even have it use create one legend for all six plots!

```r
ggarrange(plotlist = figs, # List of our plots to arrange
          common.legend = TRUE, # One legend for all plots (only if it makes sense!)
          legend = "right") # Place legend on right side of figure
```

![ggarange_plot](https://cougrstats.files.wordpress.com/2019/09/ggarange_plot.png)

There are ways that you can use this method to have single x- or y-axis labels, too, but I won't cover that here in detail. Essentially, you leave the axis titles of the individual plots blank and then use the `ggpubr` `annotate_figure()` function to create new axis labels for the entire figure.

#### 4. Insets

Mapping in `ggplot2` deserves its own separate treatment so I won't cover the backround right now, but creating maps provides great context for plot insets. A plot inset is a smaller plot or image included within a larger one. For example, you may want to include a zoomed out map for spatial context alongside your regular map.

We can continue using the iNaturalist data and `ggplot2` for this. Let's plot the locations where people have made observations.

First get the Whitman county shapefile. `st_as_sf()` comes from the `sf` package, while `counties()` comes from `tigris`.

    whitman_co % filter(NAME == "Whitman")

    ## Using FIPS code '53' for state 'Washington'

Then make a basic map with observation points.

    whitman_map_data % filter(coordinates_obscured == "false")

    whitman_point <- ggplot() +
      geom_sf(data = whitman_co, fill = NA) +
      geom_point(data = whitman_map_data,
                 aes(x = longitude, y = latitude)) +
      scale_fill_viridis_c() +
      theme(panel.grid = element_blank())

    whitman_point

![basic_map](https://cougrstats.files.wordpress.com/2019/09/basic_map.png)

We go about creating the inset map much like the regular one. I add a filled black polygon for Whitman County over the Washington polygon and simplified the style of the map compared with the larger focal map.

    washington_st % filter(NAME == "Washington")

    inset_map <- ggplot() +
      geom_sf(data = washington_st,
              fill = NA) +
      geom_sf(data = whitman_co,
              fill = "black") +
      theme_bw() +
      xlab("") +
      ylab("") +
      theme(axis.title.x = element_blank(),
            axis.title.y = element_blank(),
            panel.grid = element_blank(),
            axis.text = element_blank(),
            axis.ticks = element_blank(),
            plot.background = element_blank())

We can now place the inset using `ggdraw()` and `draw_plot()` from `cowplot`.

```r
ggdraw() +
  draw_plot(whitman_point) +
  draw_plot(plot = inset_map,
            x = 0.085, # x location of inset placement
            y = 0.04, # y location of inset placement
            width = .455, # Inset width
            height = .26, # Inset height
            scale = .58) # Inset scale
```

![inset_map](https://cougrstats.files.wordpress.com/2019/09/inset_map.png)

There's some overplotting of points on our map. One way we can deal with this and spice the map up a bit would be to replace the point layer with a heatmap hex layer (`geom_hex()`). Also, the plot inset moves if we use the same xy location as in the previous plot so I've changed the xy info.

```r
whitman_hex <- ggplot() +
  geom_sf(data = whitman_co, fill = NA) +
  geom_hex(data = whitman_map_data,
           aes(x = longitude, y = latitude),
           alpha = 0.8) + # Partial transparency
  scale_fill_viridis_c() +
  theme(panel.grid = element_blank())

ggdraw() +
  draw_plot(whitman_hex) +
  draw_plot(plot = inset_map,
            x = 0.03,
            y = 0.04,
            width = .455,
            height = .26,
            scale = .58)
```

![hex_inset_map](https://cougrstats.files.wordpress.com/2019/09/hex_inset_map.png)

# References

  * iNaturalist. Available from <https://www.inaturalist.org>. Accessed 2019-09-12.

  * https://twitter.com/slowkow/status/1029737128014606336?s=20

  * https://cran.r-project.org/web/packages/ggrepel/vignettes/ggrepel.html

  * https://cran.r-project.org/web/packages/ggpubr/ggpubr.pdf

  * https://stackoverflow.com/questions/5219671/it-is-possible-to-create-inset-graphs

  * https://jennybc.github.io/purrr-tutorial/index.html

  * https://walkerke.github.io/2017/05/tigris-metros/
