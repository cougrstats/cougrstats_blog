---
title: ggplot2 tutorial
author: cougrstats
date: '2020-10-16'
categories:
  - Package Introductions
tags:
  - ggplot2
slug: ggplot2-tutorial
---

_By Mikala Meize_

## Libraries used

```r
library(tidyverse)
library(ggthemes)
```

The ggplot() function, which is used in this tutorial is housed within the tidyverse library. The ggthemes library is something we'll use later on in the tutorial.

There are several ways to set up a plot using ggplot(). The first is to simply run:

```r
ggplot()
```

![1](https://cougrstats.files.wordpress.com/2020/10/1.png)

This tells R that you are prepping the plot space. You'll notice that the output is a blank space. This is because we have not specified an x or y axis, the variables we want to use, etc.

When building a plot with ggplot(), you add pieces of information in layers. These are separated by a plus sign (+). Whatever you include in the first layer, will be included in the following layers. For example, if we include a dataframe in the first layer:

```r
ggplot(data = mtcars)
```

![2](https://cougrstats.files.wordpress.com/2020/10/2.png)

Then each layer following will use that dataframe. Notice that even though we added a dataset, the output is still a blank space.

Something else to note about ggplot(), you can get the same plot using several different chunks of code. In the next example, I will plot the mpg variable from the mtcars dataset using two different sets of code. These both result in the same plot:

```r
ggplot(data = mtcars) +
  geom_boxplot(aes(x = mpg)) #specified the data in the first layer and the x variable in the second
```

![3](https://cougrstats.files.wordpress.com/2020/10/3.png)

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_boxplot() #specified both data and x variable in the first layer and the type of plot alone in the second
```

![4](https://cougrstats.files.wordpress.com/2020/10/4.png)

These plots are the same, but using the aes() code, the x variable was specified in different layers. The 'aes' is short for aesthetic.

There are different reasons to include the data, the x, or the y variables in the first layer. If you want to layer data from different dataframes together in a plot, you'll likely start with ggplot() alone in the first layer. If you want to layer multiple x variables from the same dataset, then you might specify the data in the first layer: ggplot(data = df). Then, if you want to keep the same x or y variable as you add layers, you can specify that as well: ggplot(data = df, aes(x = variable, y = variable)).

### Plotting variables together

Using the dataset mtcars, mpg (miles per gallon) will be on the x axis and hp (horsepower) will be on the y axis.

```r
ggplot(data = mtcars, aes(x = mpg, y = hp))
```

![5](https://cougrstats.files.wordpress.com/2020/10/5.png)

I have not clarified how I want these variables plotted (lines, points, etc.) so the x and y axes are labeled, but there is no data in the plot space. In the next layer, I specify that I want the data plotted as points.

```r
ggplot(data = mtcars, aes(x = mpg, y = hp)) +
  geom_point()
```

![6](https://cougrstats.files.wordpress.com/2020/10/6.png)

I am interested in the relationship between displacement and mpg too. By adding another layer, I can add a second y variable.

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_point(aes(y = hp)) +
  geom_point(aes(y = disp))
```

![7](https://cougrstats.files.wordpress.com/2020/10/7.png)

Because I have two y variables, I removed the y specification from the first layer and added the separate y variables in their own layers. To differentiate one set of points from another, I can request different shapes for the data points based on variable.

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_point(aes(y = hp, shape = 'Horsepower')) +
  geom_point(aes(y = disp, shape = 'Displacement'))
```

![8](https://cougrstats.files.wordpress.com/2020/10/8.png)

Now I can tell the difference between horsepower and displacement, and there is a legend off to the side explaining this. You can do the same thing with lines instead of points.

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_line(aes(y = hp)) +
  geom_line(aes(y = disp))
```

![9](https://cougrstats.files.wordpress.com/2020/10/9.png)

Instead of shape, use linetype to differentiate between variables.

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_line(aes(y = hp, linetype = 'Horsepower')) +
  geom_line(aes(y = disp, linetype = 'Displacement'))
```

![10](https://cougrstats.files.wordpress.com/2020/10/10.png)

You can change the color of each plotted variable too. If you add the label inside aes(), then R picks the line color for you.

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_line(aes(y = hp, color = 'Horsepower')) +
  geom_line(aes(y = disp, color = 'Displacement'))
```

![11](https://cougrstats.files.wordpress.com/2020/10/11.png)

You can specify the color of each line by include the color code outside the aes().

```r
ggplot(data = mtcars, aes(x = mpg)) +
  geom_line(aes(y = hp), color = 'blue') +
  geom_line(aes(y = disp), color = 'green')
```

![12](https://cougrstats.files.wordpress.com/2020/10/12.png)

### Publishable Plots

In the following example, I am using the economics dataset that comes loaded with R. I want to plot variables across time, so I'll use 'date' as the x axis.

```r
ggplot(data = economics, aes(x = date))
```

![13](https://cougrstats.files.wordpress.com/2020/10/13.png)

The first variable I'll plot is 'psavert' (Personal Savings Rate), and I'll plot it as a line.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert))
```

![14](https://cougrstats.files.wordpress.com/2020/10/14.png)

The second variable I'll plot is 'uempmed' (Duration of Unemployment measured in weeks).

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert)) +
  geom_line(aes(y = uempmed))
```

![15](https://cougrstats.files.wordpress.com/2020/10/15.png)

As before, the lines are indistinguishable. For this example, I want to make a black and white plot that I could publish with. So I'll let R choose the line type for these two variables.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)'))
```

![16](https://cougrstats.files.wordpress.com/2020/10/16.png)

I have no need for the grid in the background so I can use the theme() layer to change this. You can remove some of the grid lines, or all of the grid lines.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme(panel.grid.major = element_blank())
```

![17](https://cougrstats.files.wordpress.com/2020/10/17.png)

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())
```

![18](https://cougrstats.files.wordpress.com/2020/10/18.png)

If you want zero grid lines, you can skip a step and do this:

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme(panel.grid = element_blank())
```

![19](https://cougrstats.files.wordpress.com/2020/10/19.png)

I want to add axis lines for both x and y, and I want them to be black.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme(panel.grid = element_blank(),
        axis.line = element_line(color = 'black'))
```

![20](https://cougrstats.files.wordpress.com/2020/10/20.png)

We can also use preset themes. Most of these themes are in the tidyverse library, but some of the more unique themes are part of the ggthemes library.
I tend to use the theme_bw() or the theme_classic() when building my publishable plots.

_Note: the premade/preset theme must go before the theme() specifications you make._

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme_bw() +                                                                    #this theme adds a border around the plot
  theme(panel.grid = element_blank(),
        panel.border = element_blank(),                                           #this code removes the border
        axis.line = element_line(color = 'black'))
```

![21](https://cougrstats.files.wordpress.com/2020/10/21.png)

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme_classic()
```

![22](https://cougrstats.files.wordpress.com/2020/10/22.png)

```r
#theme_classic() does all of the things I did manually above, but in one line of code instead of several.
```

Currently the plot is very wide with the legend on the right, so I am going to move it to the bottom of the plot using the theme() options.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme_classic() +
  theme(legend.position = 'bottom')
```

![23](https://cougrstats.files.wordpress.com/2020/10/23.png)

This looks much better, but the axis titles and the legend title are still not publishable quality. I can fix the axis and plot titles using the labs() layer.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme_classic() +
  theme(legend.position = 'bottom') +
  labs(x = 'Date',
       y = NULL,
       title = 'Savings and Unemployment',
       subtitle = 'US Economic Data')
```

![24](https://cougrstats.files.wordpress.com/2020/10/24.png)

My plot now has no Y axis title, a grammatically correct x axis title, a plot title, and a subtitle. In this next step, I'll go back to the theme() options and center the plot title and get rid of the legend title.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme_classic() +
  theme(legend.position = 'bottom',
        plot.title = element_text(hjust = 0.5),        #Center the title
        plot.subtitle = element_text(hjust = 0.5),     #Center the subtitle
        legend.title = element_blank()) +              #Remove the legend title
  labs(x = 'Date',
       y = NULL,
       title = 'Savings and Unemployment',
       subtitle = 'US Economic Data')
```

![25](https://cougrstats.files.wordpress.com/2020/10/25.png)

Now I have a beautiful black and white plot, with no odd coding language. This can be exported from R as an image or as a PDF.

Sometimes a journal will want you to match the font of your plots to the font of your text. I've found a nice theme (from ggthemes library) I like to use for this.

```r
ggplot(data = economics, aes(x = date)) +
  geom_line(aes(y = psavert, linetype = 'Personal Savings Rate')) +
  geom_line(aes(y = uempmed, linetype = 'Duration of Unemployment (weeks)')) +
  theme_tufte() +
  theme(legend.position = 'bottom',
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        legend.title = element_blank(),
        axis.line = element_line(color = 'black')) +    #This theme removes all axis lines, I've added them back here.
  labs(x = 'Date',
       y = NULL,
       title = 'Savings and Unemployment',
       subtitle = 'US Economic Data')
```

![26](https://cougrstats.files.wordpress.com/2020/10/26.png)

There are so many more things you can do with ggplot, this is only a start to the possibilities. I highly recommend browing the ggplot website and their posted cheat sheets to learn more: <https://ggplot2.tidyverse.org/>
