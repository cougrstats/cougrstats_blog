---
title: Best practices in R version control
author: Nicholas Potter
date: '2019-01-30'
slug: best-practices-in-r-version-control
---

#### By Nicholas Potter

#### Resources:

  * [A list of best practices](https://www.r-statistics.com/2010/09/managing-a-statistical-analysis-project-guidelines-and-best-practices/)

  * [Ropensci's rrrpkg suggestions](https://github.com/ropensci/rrrpkg)

  * [An official using GIT with Rstudio](https://support.rstudio.com/hc/en-us/articles/200532077?version=1.1.453&mode=desktop)

  * [A better GIT and Rstudio article](https://r-bio.github.io/intro-git-rstudio/)

## Why R projects?

Because `setwd()` is evil (source).

  * [here](https://github.com/jennybc/here_here): an `R` packages to manage the working directory and file locations

## A scenario: A new project on water resources

You are wrapping up a project before you meet with your advisor, and you need to update figure 1 in your paper. You open the project directory to see a list of files like this:

<table >

<tr >
Filename
Modified
</tr>

<tbody >
<tr >

<td >create_fig1.R
</td>

<td >June 1, 2017
</td>
</tr>
<tr >

<td >create_fig1_v2.R
</td>

<td >August 23, 2018
</td>
</tr>
<tr >

<td >20181022_create_fig1_v4.R
</td>

<td >November 2, 2018
</td>
</tr>
<tr >

<td >fig1.jpg
</td>

<td >August 23, 2018
</td>
</tr>
<tr >

<td >fig1_v3.jpg
</td>

<td >October 31, 2018
</td>
</tr>
<tr >

<td >etc...
</td>

<td >etc...
</td>
</tr>
</tbody>
</table>

What are the pitfalls here?

  1. fig1.jpg looks like it was created by `create_fig1.R`, but the modified date suggests it was actually created by `create_fig1_v2.R`. Did you forget to change the filename when you created the second script?

  2. There's no version 2 or 4 of `fig1.jpg`. Did you move those or delete them by accident? On purpose?

  3. `20181022_create_fig1_v4.R` was modified later than the date indicated in the filename. And also `fig1_v3.jpg` was modified just a few days before. Did you create a v4 of the figure and misplace it? Or did you forget to change the name again? And where is the version 3 file?

You pour through your scripts and manage to finally find the code that recreates the latest figure. Making the changes quickly, you rename the new script to `create_fig1_v5_FINAL.R`, but forget to change the name of the image, so it outputs `fig1_v3.jpg` again, overwriting your previous image. But you're out of time so you add it to your paper and email it right before your meeting, promising yourself you'll learn about this version control thing you keep hearing about...

At your meeting, you discuss another project with your advisor about water resources, and your advisor suggests you look into the colorado water rights database and a paper by [Leonard and Libecap (2016)](https://www.nber.org/papers/w22185). You decide you want to have an organized project this time, so you decide to research git and R projects a little bit. And the rest, _as they say, is history_...

### What are RStudio projects?

  * R Projects are a directory that include all the files for a given context

  * When you open an R project, RStudio does several things: (1) read .RData, .Rprofile, and .Rhistory; (2) change the working directory to the project home

### What is Git?

Git is really about taking _snapshots_ of your project and being able to go back to those changes at any time. I can't explain git nearly as well as [The Git Parable](http://tom.preston-werner.com/2009/05/19/the-git-parable.html).

### How do Rstudio Projects and Git work together?

Within a project, Rstudio integrates git into a special tab that allows you to do all of the git work without leaving Rstudio.

### In short

  * Don't try to do everything right right now. Focus on one change to your workflow per month

  * Don't modify raw data

  * Use version control to avoid file multiplication and naming hell

  * Have a standard project folder organization

  * Commit early and often
