---
title: Webscraping in R
author: cougrstats
date: '2018-10-12'
slug: webscraping-in-r
categories:
  - Package Introductions
tags:
  - webscraping
  - rvest
---

# Things to Look for as a Beginner

These are the three functions that are used during this presentation for webscraping. These are the only functions that are used from the "rvest" package. Everything else in this presentation is base R.

  * read_html()
  * html_nodes()
  * html_table()

# What is Web Scraping?

Web scraping is the process of automatically collecting data from web pages without visiting them using a browser. This can be useful for collecting information from a multitude of sites very quickly. Also, because the scraper searches for the location of the information within the webpage it is possible to scrape pages that change daily to get the updated information.

# Scraping in R using rvest

We will focus on scraping without any manipulation of the webpages that we visit. Webpage manipulation while scraping is possible, but it can not be done exclusively in R which is why we will be ignoring it for this lesson.

# What is HTML?

HTML stands for HyperText Markup Language. All HTML pages are built using the same format. A very generalized version of this is that a page should always have a header, a body, and a footnote. This isn't always the case though and is up to the developer.

# The HTML Tree

![](https://cougrstats.files.wordpress.com/2018/10/flowchat.png)

# Information to Gather

Let's collect some environmental data. I want to know what the weather station on the roof is reporting right now.
The url for the PACCAR Weather Station is

<http://micromet.paccar.wsu.edu/roof/>

# Install rvest

This is a package for R that should download the webpage as html for further manipulation.

```r
# Load the library
if(!require(rvest)){
    install.packages("rvest")
    library(rvest)
}
```

# Download the HTML

First we need to tell R to navigate to the site and save the current html of the page.

```r
# Save the url as a variable
weather.station <- read_html('http://micromet.paccar.wsu.edu/roof/')
```

# Extract Values From Table

Next we specify the html nodes that we are interested in. In this case these are all referred to with the label "font" which allows us to specify that we want all values from the page that are labeled "font".

```r
# Extract the table values from the HTML
table.values <- html_nodes(weather.station, xpath = '//font/text()')
```

# Visualize the Table

```r
head(table.values, 13)

## {xml_nodeset (13)}
##  [1]
##  [2]  Latest time
##  [3]   2018-10-08 09:10:00
##  [4] Net Radiation
##  [5]   106.7  Wm
##  [6] Temperature
##  [7]    8  &amp;deg C ( 46.4 &amp;deg F )
##  [8] Humidity
##  [9]    76.8 %
## [10] Pressure
## [11]    923.4 mbar
## [12]  Wind speed
## [13]    2.7 m/s (6 mph)
```

# Save the Values as Individual Variables

We're going to save the values that we want from the previous list as individual variables

```r
# Time
scraped.datetime <- as.character(table.values[3])
# Radiation
radiation <- as.character(table.values[5])
# Temperature
temperature <- as.character(table.values[7])
# Humidity
humidity <- as.character(table.values[9])
# Pressure
pressure <- as.character(table.values[11])
# Wind Speed
wind.speed <- as.character(table.values[13])
# Rain
rain <- as.character(table.values[17])
```

# View the Variables to Check Formatting

Let's view one of our variables to see how it is formatted now.

```r
# Print the variable to the console
scraped.datetime

## [1] "  2018-10-08 09:10:00 "
```

# Split the Datetime into Date and Time

```r
# Use strsplit to separate into a list
datetime <- strsplit(scraped.datetime, " ")
# View the list after the split
datetime

## [[1]]
## [1] ""           ""           "2018-10-08" "09:10:00"

# Select and save the scraped date
scraped.date <- datetime[[1]][3]
# Select and save the scraped time
scraped.time <- datetime[[1]][4]
# Print the time
scraped.time

## [1] "09:10:00"
```

# Create a Function to Scrape Radiation

```r
# This is our radiation scraping function
scrape.raditation <- function(){
  # Download the html
  weather.station <- read_html('http://micromet.paccar.wsu.edu/roof/')
  # Extract the table values
  table.values <- html_nodes(weather.station, xpath = '//font/text()')
  # Save the radiation value
  radiation <- as.character(table.values[5])
  # Split the string
  radiation.temp <- strsplit(radiation, " ")
  # Return only the numerical value
  return(radiation.temp[[1]][3])
}
```

# Let's Try Our Radiation Function

```r
# Execute the function
scrape.raditation()

## [1] "106.7"
```

# Web Scraping Tables

```r
# Function to scrape votesmart.org
voting.record <- function(candidate, pages){
  # Create an empty data frame
  df <- NULL
  # Collect all data from the table on each page
  for (page in 1:pages){
    # Paste the URLs together
    candidate.page <- paste(candidate, "/?p=", page, sep = "")
    # Download the html for the page
    candidate.url <- read_html(candidate.page)
    # Save the record as a table
    candidate.record <- as.data.frame(html_table(candidate.url)[2])
    # Row bind the current table to the rest
    df <- rbind(df, candidate.record)
  }
  return(df)
}
```

# Run the Function

```r
# Website for Cathy McMorris Rogers' voting rcord
cathy <- "https://votesmart.org/candidate/key-votes/3217/cathy-mcmorris-rodgers"
# Website for Lisa Brown's voting record
lisa <- "https://votesmart.org/candidate/key-votes/3180/lisa-brown"

# Scrape Cathy's voting record
cathy.df <- voting.record(cathy, 21)
# Scrape Lisa's voting record
lisa.df <- voting.record(lisa, 2)
```

# View Some Lines from Cathy's Record

```r
##             Date Bill.No.
## 1 Sept. 28, 2018  HR 6760
## 2 Sept. 26, 2018  HR 6157
## 3 Sept. 13, 2018  HR 1911
##                                                                                           Bill.Title
## 1                                          Protecting Family and Small Business Tax Cuts Act of 2018
## 2 Department of Defense and Labor, Health and Human Services, and Education Appropriations Act, 2019
## 3                                      Special Envoy to Monitor and Combat Anti-Semitism Act of 2018
##                          Outcome Vote
## 1 Bill Passed - House(220 - 191)  Yea
## 2                House(361 - 61)  Yea
## 3                 House(393 - 2)  Yea
```

# View Some Lines from Lisa's Record

```r
##             Date Bill.No.
## 1 April 11, 2012  HB 2565
## 2 April 11, 2012  SB 5940
## 3 April 10, 2012  SB 6378
##                                           Bill.Title
## 1           Roll-Your-Own Cigarette Tax Requirements
## 2 Amends Public School Employees Retirement Benefits
## 3               Amends State Employee Pension System
##                         Outcome Vote
## 1 Bill Passed - Senate(27 - 19)  Yea
## 2 Bill Passed - Senate(25 - 20)  Nay
## 3 Bill Passed - Senate(27 - 22)  Nay
```

# View Cathy's Voting Distribution

![](https://cougrstats.files.wordpress.com/2018/10/graph1.png)

# View Lisa's Voting Distribution

![](https://cougrstats.files.wordpress.com/2018/10/graph2.png)

There is so much more that can be done with webscraping, but this code should be enough to get you up and running using rvest to scrape.
