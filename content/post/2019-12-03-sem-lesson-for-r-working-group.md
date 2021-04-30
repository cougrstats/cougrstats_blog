---
title: SEM Lesson for R Working Group
author: cougrstats
date: '2019-12-03'
categories:
  - Package Introductions
tags:
  - Structural Equation Modeling
slug: sem-lesson-for-r-working-group
---

_By Ben Lee_

_Data for this walkthrough are available [here](https://drive.google.com/file/d/1FF6YBoudCzsil6viaKhPJp_37lRv75Ds/view?usp=sharing)._

#### Why Use an SEM?

Autocorrelation is everywhere in Ecological data, and fundamentally violates the assumptions of univariate linear models. Path analysis allows us to partition the variance of responses through a **series** of linear models.

In our example, we'll be looking at how insect predators affect the populations and movement of aphids, which vector a plant virus. This experiment manipulated lady beetles by gluing their mouthparts shut such that some predators were "risk" only, while unmanipulated predators were considered "lethal".

Confirmatory path analysis using piecewise SEM will allow us to determine just how predators affect aphid populations and behavior in ways that affect the number of plants that get infected in a field mesocosm. Our goal is to incorporate all significant predictors in our path model, and to calculate the relative contribution of each predictor to its response variable.

#### Packages Needed

```r
library("lme4")
library("car")
library("multcomp")
library("ggplot2")
library("grid")
library("gridExtra")
library("emmeans")
library("piecewiseSEM")
```

#### Set WD, load data, check headers

```r
setwd("C:/Users/bwl42/Desktop/sem")

## Error in setwd("C:/Users/bwl42/Desktop/sem"): cannot change working directory

sem <- read.csv("sem_data.csv", sep = ",", header=TRUE)
str(sem)
```

### Create a full hypothetical model prior to any further path analysis

Before creating the linear models that will form the SEM, we need to determine what interactions to include by doing a bit of preliminary analysis. This is a combination of background knowledge of the system and some initial looks at the data. We'll first take a peek at some simple models of our data

#### How do Predator treatments affect aphids?

```r
ggplot(sem, aes(x=Treat, y = totad)) + geom_boxplot() ->p1
ggplot(sem, aes(x=Treat, y = totnym)) + geom_boxplot() ->p2
ggplot(sem, aes(x=Treat, y = addist)) + geom_boxplot() ->p3
ggplot(sem, aes(x=Treat, y = inf.ratio)) + geom_boxplot() ->p4
grid.arrange(p1,p2,p3,p4, ncol=2)
```

![sem1](https://cougrstats.files.wordpress.com/2019/12/sem1.png)

Looking at these boxplots, its pretty clear that lethal predators reduce the populations of aphid adults and nymphs, as expected. It also looks like both predator treatments increase the movement of aphid adults, **and** increase the proportion of plants infected in the mesocosm! But we know that the predators can't transmit the virus themselves, so this has to be an indirect effect mediated by **something** that they're doing to the aphids.

The reason we're using a piecewise SEM is to tell us which aphid response this might be, and how significantly it's contributing to these observed effects on infection.

#### How do aphid responses affect the number of plants infected?

```r
ggplot(sem,aes(x = totnym, y = inf.ratio)) + geom_smooth(method='lm') -> a1
ggplot(sem,aes(x = totad, y = inf.ratio)) + geom_smooth(method='lm') -> a2
ggplot(sem,aes(x = addist, y = inf.ratio)) + geom_smooth(method='lm') -> a3
grid.arrange(a1,a2,a3, ncol = 2)
```

![sem_fig2](https://cougrstats.files.wordpress.com/2019/12/sem_fig2.png)

Looking at these simple models, it seems likely that aphid populaton or movement are influential on virus prevalence in this system.

Using our predictions and the direction of effects from these outputs, lets throw together our a priori network model.

#### Our A priori model

![](PIC/apriori.png)![apriori](https://cougrstats.files.wordpress.com/2019/12/apriori.png)

This network model shows what component linear models we're going to include in our initial analysis; predators affect aphid population and movement, and population and movement affect the ratio of plants infected with the virus. The whole point of running the path analysis is to determine which of these predictors are significant, so this is subject to change as we refine the model.

Notice the double-ended arrow between Adult pop and Nym Pop. This is a correlated error, which we will specify later in the model. We know that Adult and Nymph populations are going to be significantly linked but since we aren't interested in that relationship, specifying it as a correlated error will tell the path analysis that we expect this correlation and don't need to include one of them as a predictor.

### Run Primary GLMs for each hypothesized path

With our a priori model created, we can begin creating the linear models that serve as our paths. Here I'm using generalized linear models, but the piecewisesem package supports lm, glm, gls, pgls, sarlm, lme, glmmPQL, lmerMod, merModLmerTest, and glmerMod.

```r
 ad.pop1 <- glm(totad ~ lethal, data = sem)
 nym.pop1 <- glm(totnym ~ lethal, data = sem)
 ad.dist1 <- glm(addist ~ lethal + risk, data = sem)
 inf.rat1 <- glm(inf.ratio ~ totad + totnym + addist, family="binomial", weights= inf.weight, dat=sem)
```

These models represent each of our proposed paths. The inf.rat1 model uses a binomial distribution weighted to 25 (the total possible number of plants infected).

#### Pop our glms into the SEM

The psem() function unites our models into a single structural equation model.

```r
 sem.1 <- psem(ad.pop1, nym.pop1, ad.dist1, inf.rat1)
```

Now let's see what how our a priori model performed! The summary function will provide us with all sorts of information.

Disclaimer: Since the piecewisesem summary output has a lot of additional garbage that mess with the Rmarkdown, these are screenshots of the output.

###SEM 1
summary(sem.1, standardize = "none", conserve = TRUE)
![](PIC/sem1.jpg)
![sem1](https://cougrstats.files.wordpress.com/2019/12/sem1.jpg)

There's a ton of information here so let's go through it step-by-step.

The "Call" lists out the paths we included in this initial model. Below that we have our AIC of 57.566, which we'll use to compare the performance of this model to others when we add or remove paths.

The tests of directed separation let us know what interactions were significant and should have been included in the model. The model as it stands was not accepted (p < .05). It appears we ignored a significant **direct** effect of lethal predators on infected plants, so we will include that in our next model. We also didn't include our correlated error between totnym ~ totad, which we add to model next

Our coefficients show that most of the paths we included appear to be significant predictors. However, the values of these will change as we add significant paths or remove others.

#### Add our correlated error

Here we specify our correlated error, which we'll include for all the remaining SEM summary outputs.

summary(update(sem.1, totad %~~% totnym), standardize="none")

![](PIC/sem1update.jpg)
![sem1update](https://cougrstats.files.wordpress.com/2019/12/sem1update.jpg)

While our AIC improved significantly, this model still has room to improve, so lets modify our paths.

#### Can we refine this model to strengthen our case?

In the tests of directed separation, it still appears that lethal has a significant **direct** effect on inf.ratio that we didn't include, so lets add a direct effect of "lethal" to our inf.rat model.

```r
 inf.rat2 <- glm(inf.ratio ~ totad + totnym + addist + lethal, family="binomial", weights= inf.weight, dat=sem)
```

#### SEM 2

Update the model with the newly modified inf.rat2 and let's see how the model improved.

sem.2 <- psem(ad.pop1, nym.pop1, ad.dist1, inf.rat2)
summary(update(sem.2, totad %~~% totnym), standardize= "none")

![](PIC/sem2.jpg)
![sem2](https://cougrstats.files.wordpress.com/2019/12/sem2.jpg)

The AIC has improved slightly, and our new paths show that we may want to include the effect of "Risk" predators on nymph populations and the inf.ratio. Lets add those to our model.

```r
 nym.pop2 <- glm(totnym ~ lethal + risk, data = sem)
 inf.rat3 <- glm(inf.ratio ~ totad + totnym + addist + lethal + risk, family="binomial", weights= inf.weight, dat=sem)
```

#### SEM 3

sem.3 <- psem(ad.pop1, nym.pop2, ad.dist1, inf.rat3)
summary(update(sem.3, totad %~~% totnym), standardize= "none")

![](PIC/sem3nostandard.jpg)
![sem3nostandard](https://cougrstats.files.wordpress.com/2019/12/sem3nostandard.jpg)

The model appears to fit rather well, with our AIC at 38.8, all significant paths included, and most of the variation explained.

#### Scale Coefficients

So we've got our path analysis finished up, but there's still a need to calculate the relative effect of each predictor. Standardizing using "scale" scales the estimate to the standard deviation, but honestly I don't know just how the math plays out there.

summary(update(sem.3, totad %~~% totnym), standardize= "scale")

![](PIC/sem3.jpg)
![sem3](https://cougrstats.files.wordpress.com/2019/12/sem3.jpg)

Now we've got our completed path analysis, R2 values for each outcome, and standardized effect sizes of each predictor. Our finalized model therefore looks something like this

![](PIC/finalmodel.png)![finalmodel](https://cougrstats.files.wordpress.com/2019/12/finalmodel.png)

This model tells a very different story from what our initial univariate models suggested. Here we found that despite a significant effect of predators on aphid populations and movement on the number of plants infected, there appears to be some unincluded way that predators influenced infection. Later experiments found this was likely due to predators moving aphids higher up on plants, where new tissue was more susceptible to virus transmission. However, since this was not included in our model, that hidden effect was highlighted by the direct effect of predators on infection revealed by our SEM.
