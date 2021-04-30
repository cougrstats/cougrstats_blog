---
title: Introduction to Shiny
author: cougrstats
date: '2018-03-30'
categories:
  - Package Introductions
tags:
  - collaboration
  - html
  - Rstudio
  - shiny
slug: introduction-to-shiny
---

_Author: Alli N. Cramer_

Shiny is an R package that allows you to create interactive data visualizations. Shiny can create HTML pages which can allow users to generate graphs, maps, etc. based on underlying data and predetermined functions.

If you use R Studio, Shiny comes pre-installed and can be accessed by clicking File -> New File -> Shiny Web App. If you use native R you will need to make sure you have the shiny package.

For cool examples of shiny, and for more help, see the shiny page, <https://shiny.rstudio.com/>.

## Shiny File Format

When you open a new Shiny file, called a shiny "app", there are two possible ways to do it. One is as a single app script, the other is as two scripts, a ui.R and a server.R script, which work together to make a functioning app script.

In this example we will use a single app script. As will become apparent, the two-script version is suitable for more complicated shiny files, but relies on the same format as the basic app script.

## Shiny Component Parts

The two essential parts of shiny are the ui and the server parts. When you open a brand new shiny app you will get a preformatted shiny app which includes these two parts. Format wise, the ui and the server look like, and function similarly to, functions in R. In the example page below the ui specifies the layout of the html page and where a user can add inputs (changing the number of bins in a histogram). The server specifies the data source for the histogram (the built in dataset **faithful**), the plot format itself (_hist()_), and where user input is incorporated (the _input$bins_ call).

```r
#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(

   # Application title
   titlePanel("Old Faithful Geyser Data"),

   # Sidebar with a slider input for number of bins
   sidebarLayout(
      sidebarPanel(
         sliderInput("bins",
                     "Number of bins:",
                     min = 1,
                     max = 50,
                     value = 30)
      ),

      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("distPlot")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

   output$distPlot <- renderPlot({
      # generate bins based on input$bins from ui.R
      x    <- faithful[, 2]
      bins <- seq(min(x), max(x), length.out = input$bins + 1)

      # draw the histogram with the specified number of bins
      hist(x, breaks = bins, col = 'darkgray', border = 'white')
   })
}

# Run the application
shinyApp(ui = ui, server = server)
```

## More Complicated Inputs

The base example above is effective but we can easily do more complicated apps. For example, what if we wanted to change the source data being plotted based on user inputs?

To do this we need to use what are called "reactives". We need to specify the user input in the ui, and then call it in the server function, but in a way that lets Shiny know that the input will require the dataset and graph to be re-run. We can do this two ways, by specifying the user input with a _get()_ command (good for simple changes) or by explicitly telling the server the data is reactive.

In the example below we have plotted the built in **iris** dataset. In this example we use radio buttons to select the response variable in the ui. The data is then integrated into the plot using the _get()_ command.

We alter what subset of the data is being plotted by creating a reactive dataset. In the ui we have chosen to select species data from a drop down menu, _selectInput()_, however the ui component could be radio buttons, or a slider, etc. The server component specifies the data is reactive before developing the plot:

```r
dat <- reactive({
    df <- subset(iris, Species == input$species)
    return(df)})
```

Here we have explicitly told the server that the dat object called in a later plot is a reactive object which changes based on the user input for Species. When we format data this way we need to be careful to call the dat object with open parentheses, "data = dat()" in this case, because the object is not static. See example below.

```r
library(shiny)

# Define UI for application that draws a plot with a linear model
ui <- fluidPage(

   # Application title
   titlePanel("Iris Data Plot"),

   # Sidebar with a slider input for number of bins
   sidebarLayout(
      sidebarPanel(
         selectInput("species",
                     "which species",
                     choices = c("setosa", "versicolor", "virginica")
                       )
         ),
         radioButtons("var",
                      "response variable",
                      c("Sepal Width" = "Sepal.Width",
                        "Petal Length" = "Petal.Length",
                        "Petal Width" = "Petal.Width"))
      ),

      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("modplot")
      )
   )

# Define server logic required to draw a plot
server <- function(input, output) {
  dat <- reactive({
    df <- subset(iris, Species == input$species)
    return(df)})

  output$speciesname <- renderText(get(input$species))

  output$modplot <- renderPlot({
      # generate models based on input$variable from ui.R

     mod <- lm(get(input$var) ~ Sepal.Length, data = dat())

      # plot based on selected variables and add model on top
      plot(get(input$var) ~ Sepal.Length, data = dat())
      abline(mod)
   })
}

# Run the application
shinyApp(ui = ui, server = server)
```
