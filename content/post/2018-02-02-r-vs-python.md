---
title: R "vs" Python
author: cougrstats
date: '2018-02-02'
tags:
  - guest speaker
  - Python
  - R/Python
slug: r-vs-python
---

_Author: A. Leah Zulas and Stephanie Labou_

Today's guest speaker was Dr. A. Leah Zulas. Dr. Zulas has a master's degree and a PhD in experimental psychology, as well as a master's degree in computer science. She walked us through similarities and differences in R and Python. You can view her presentation [here](https://prezi.com/view/D5cMP812Xi2Lpm8PqfSu/).

**Overview of Python and R**

First things first, let's start this recap on the right foot: this is _not_ a competition between R and Python. The two languages are, in fact, very complimentary! The issue at hand is strengths and weaknesses of each. Whereas Python is a high-level language designed to the "glue" between languages (i.e., letting other programs talk to one another), R is an ultra high-level language designed specifically for computation statistics.

_Python_

Python is an object-oriented, interactive, scripting language. While it is often used as an extension language for C/C++, it is not limited to being embedded in other code. Python has a rich set of libraries (analogous to R packages) available for other topics!

Python really excels when dealing with servers: creating a phone app, updating a user interface, or otherwise taking in a large amount of data from other programs speaking other computational languages. For example, Python would be the appropriate choice to create a script that "talks" to a cloud server and pulls some data.

Advantages of Python: Python tends to be faster when dealing with large amounts of data and/or databases. It is also more flexible, since it is meant to be a fully functional programming language, not only a scripting language.

_R_

R is built more for the layman, rather than the traditionally trained programmer. While it has basic programming capabilities like loops, functions, conditionals, etc., its real strength is its statistical capabilities. R also has an extensive collection of specialized packages (analogous to Python libraries).

Advantages of R: R shines when it comes to advanced statistics and interactive visualization (i.e., [ggplot2](http://ggplot2.tidyverse.org/reference/), [shiny](https://shiny.rstudio.com/)). R also has a strong community around data analysis – R packages are battle tested by users and multiple avenues exist for finding help.

**Using both in a workflow**

Python tends to outperform R in webscaping/crawling and database connections, whereas R outperforms Python in terms of statistical analysis and interactive graphics. You can see how the two can complement each other! For instance, a project might use Python to connect to an external database and import data, then use R for analysis and visualization.

When it comes to data wrangling – getting data in the right format for analysis – both R and Python have packages/libraries available for getting data into the "right" format for analysis (i.e., [tidyverse ](https://www.tidyverse.org/)packages for R and [pandas](https://pandas.pydata.org/)/[NumPy ](http://www.numpy.org/)for Python). The scripting language used for the data wrangling stage up to the user – both are good options!

_Moving between R and Python_

There is a Python library called [RPy2](https://rpy2.readthedocs.io/en/version_2.8.x/index.html) that lets the user use R within Python. For instance, you could use ggplot2 in Python: the _syntax_ would be Python, but the _terminology_ would be from R, and visualizations would look like they were from R.

The inverse is also possible. The R package [rPython ](https://cran.r-project.org/web/packages/rPython/rPython.pdf)lets the user call Python within R. For example, you could write Python code to pull data from a remote location, then use R to analyze and visualize it. All from within R!

**Conclusions**

R and Python can be used separately, but they are more powerful when used together to optimize each step of the workflow. We can see this reflected in most data science jobs, which require _both_ R and Python.

**Additional reading**

Dataquest set R and Python [head-to-head](https://www.dataquest.io/blog/python-vs-r/) in terms of lines of code and code complexity to perform the same task.

KDNuggets has an [overview](https://www.kdnuggets.com/2015/05/r-vs-python-data-science.html) of R vs. Python, in terms of data science.

Qz.com [says](https://qz.com/1063071/the-great-r-versus-python-for-data-science-debate/): "If all you're doing is data analysis, it doesn't really matter which one you use."
