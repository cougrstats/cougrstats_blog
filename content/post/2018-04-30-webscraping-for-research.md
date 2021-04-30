---
title: Webscraping for Research
author: cougrstats
date: '2018-04-30'
categories:
  - Research Profiles
tags:
  - html
  - rvest
  - webscraping
slug: webscraping-for-research
---

_Author: Brad Luff_

# What is Web Scraping?

Web scraping is the process of automatically collecting data from web pages without visiting them using a browser. This can be useful for collecting information from a multitude of sites very quickly. Also, because the scraper searches for the location of the information within the webpage it is possible to scrape pages that change daily to get the updated information. We will focus on scraping without any manipulation of the webpages that we visit. Webpage manipulation while scraping is possible, but it can not be done exclusively in R which is why we will be ignoring it for this lesson.

# What is HTML?

HTML stands for HyperText Markup Language. All HTML pages are built using the same format. A very generalized version of this is that a page should always have a header, a body, and a footnote. This isn't alwasy the case though and is up to the developer.

Let's view the webpage we will use as an example...

<https://www.stevenspass.com/site/mountain/reports/snow-and-weather-report/@@snow-and-weather-report>

### Try rvest

This is a package for R that should download the webpage as html for further manipulation.

    # Load the library
    if(!require(rvest)){
        install.packages("rvest")
        library(rvest)
    }

    ## Loading required package: rvest

    ## Warning: package 'rvest' was built under R version 3.4.4

    ## Loading required package: xml2

    # get the webpage
    stevens <- read_html('https://www.stevenspass.com/site/mountain/reports/snow-and-weather-report/@@snow-and-weather-report')

    # Get the current header information
    temperature <- html_nodes(stevens, xpath = '//div/header/div/div/div/div/a/span/span[@class="header-stats-value"]/text()')
    # Select only the temperature
    temperature <- as.character(temperature[1])
    # Strip the temperature down to the numeric digits
    temperature <- gsub(" ", "", temperature)
    temperature <- gsub("\n", "", temperature)
    temperature <- gsub("Â°", "", temperature)

    # Get the amount of snow that fell in the last 24 hours
    snow24 = as.character(html_nodes(stevens, xpath = '//div/div/div/div/div/main/div/div[3]/div[2]/div/div/div[1]/text()'))
    # Strip the inches symbol from the snowfall value
    snow24 <- gsub("â<u>³", "", snow24)

    # Print the report we just scraped
    cat("The temperature at Stevens Pass is",temperature, "F and in the last 24 hours there has been", snow24, "inches of snow!")
    </u>

    ## The temperature at Stevens Pass is 45° F and in the last 24 hours there has been 2<U+2033> inches of snow!
