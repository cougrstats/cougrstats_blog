---
title: 'Research Profile: Predicting antibacterial efficacy using snake venom data'
author: Michael Meyer
date: '2018-02-14'
categories:
  - Research Profiles
tags:
  - discriminant analysis
  - glmulti
  - model selection
  - proc
  - venom
slug: research-profile-model-selection
---

_Author: Michael Meyer_

_You can download a subset of the data used in this document [here](https://drive.google.com/open?id=1DovC79-WEoIspyZ40LvVRbEO6FS3h8CU), and an .Rmd version of this analysis [here](https://drive.google.com/file/d/12GygmFD3Oi-wDgO3ltTrN5ckTvAYAdbl/view?usp=sharing). To watch our guest speaker Michael talk about this analysis, check out the recording of his research profile talk on [YouTube](https://www.youtube.com/watch?v=b9RwZlIuJEo&feature=youtu.be)!_

## For the Reader

This is a tutorial of model selection techniques in R, presented for one of the Research Profile sessions for the R Working Group at Washington State University. Accompanying data were compiled from a meta-analysis of snake venom data and their associated antibiotic properties.

Data collection was conducted by Justin L. Rheubert (University of Findlay, Findlay, OH 45840). Statistical analyses in this manual were conducted by Michael F. Meyer (Washington State University, Pullman, WA 99164).

This work can be cited as:

Rheubert, J.L., Meyer, M.F., Strobel, R.M., Pasternak, M.A., & R.A. Charvat. 2018. The use of multivariate predictive modeling to uncover the complexities of antibacterial properties in snake venom. In prep.

For more information regarding this project or its citation, please contact either Justin L. Rheubert (rheubert@findlay.edu) or Michael F. Meyer (michael.f.meyer@wsu.edu).

## Background

Given the growing need for new antibiotics, snake venom has garnered significant attention due to its frequently high levels of cellular toxicity. Both crude venom and its independent protein components have repeatedly demonstrated antibacterial effectiveness against numerous bacterial cultures. Chavrat et al. (_In Review_) details over 500 studies that focus on antibacterial properties of snake venom, with over 58% of studies demonstrating antibacterial effectiveness.

Despite the number of studies detailing antibacterial effectiveness of snake venom, no studies have attempted to synthesize exsiting proteomic and antibacterial data with the intent of creating a relationship between venom composition and efficacy.

## Objectives, Research Questions, and Hypotheses

The **objective** of this study is to accurately predict antibacterial efficacy of snake venom, given a proteomic composition of a snake's venom.

The **main questions** involved in this study are three-fold:

  1. Is there a clear relationship between snake venom proteomic composition and the potential for that venom to have antibiotic properties?
  2. What is the best statistical model to predict antibiotic efficacy?
  3. Can we use the "best model" to predict antibiotic efficacy for snakes that have unkown efficacy data?

We **hypothesized** that L-Amino-Acid Oxidases and Phospholipase A2 concentrations are more associated with antibiotic properties of snake venom, based on literature review (Charvat et al., _In Review_).

## Packages Required

The following packages are required:

  1. Data Manipluation: tidyr, dplyr, stringr
  2. Model Selection and Statistical Operations: car, MASS, glmulti, pROC

```r
library(tidyr)
library(dplyr)
library(stringr)
library(car)
library(MASS)
library(glmulti)
library(pROC)
library(kableExtra)
library(knitr)
panel.cor <- function(x, y, digits = 2, cex.cor, ...)
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  # correlation coefficient
  r <- cor(x, y)
  txt <- format(c(r, 0.123456789), digits = digits)[1]
  txt <- paste("r= ", txt, sep = "")
  text(0.5, 0.6, txt)

  # p-value calculation
  p <- cor.test(x, y)$p.value
  txt2 <- format(c(p, 0.123456789), digits = digits)[1]
  txt2 <- paste("p= ", txt2, sep = "")
  if(p<0.01) txt2 <- paste("p= ", "<0.01", sep = "")
  text(0.5, 0.4, txt2)
}
```

## Data Import and Description

First, we will need to import the data. The data have already be pre-cleaned and organized for convenience. The various columns detail various data and metadata for the subset. All protein concentrations have been arcsine transformed. Below is a brief description of each column in the dataset. Note that this data subset is specifically composed of Elapidae species that were tested against gram negative, facultative anaerobic, bacillus bacteria.

```r
elap.gramneg.fac.bacillus <- read.csv("elap.gramneg.fac.bacillus.csv", header=TRUE)
```

  * **Snake.species** and **Family**: Genus and Species of snake, as well as Family of Snake (All should be Elapidae)
  * **Three.finger.toxins, Phospholipase.A2, Metalloproteinases, Serine.proteinases, Disintegrins, C.type.lectins, peptides, Vespryn.ohanin, Exonuclease.PDE.5..nuclotidases, Waglerins, Cysteine.rich.secretory.proteins, Snake.venom.growth.factors, L.amino.acid.oxidase, Waprin.Kunitz.BPTI, Hyaluronidase, Bradykinin.potentiating.peptides.and.natriuretic.peptides**: Arcsine transformed protein proportions.
  * **Toxin**: Type of toxin considered from original study (Should be Crude_Venom)
  * **bacteria**: Bacterial species considered in the study
  * **effectiveness**: Whether or not crude venom was effective as an antibiotic. Binary responses coded as 0 for ineffective and 1 as effective.
  * **Respiration**, **Morphology**, and **Gram.Stain**: Metadata on the bacteria of study. (Should be Facultative anaerobic, bacillus, and gram negative respectively)

## Summary Statistics

This step is essential for model selection. Essentially, we want to select for proteins that vary greatly, such that we can soak up the greatest variance in our final model. If a protein's concentration is relatively constant throughout all snake species, then there is effectively no reason to assume that a constant protein would be important in determining antibacterial effectiveness. Additionally, because the protein concentration would be relatively constant, the uncertainty attributed by that relatively constant protein would be absorbed in whatever constant the final model may produce. This will become more clear when we discuss model selection and logistic regression below.

For now, we are just going to look at Mean, Variance, and the Ratio of Variance to Mean. We will use these statistics to determine which proteins should go into our final model selection code. We set the following guidelines for whether a protein should be considered for model selection incoporation:

  1. Variance needs to be greater than 0.01.
  2. Variance to Mean Ratio needs to be greater than or equal to 0.05, meaning that the variance is at least 5% of the mean.

```r
mean <- as.vector(sapply(elap.gramneg.fac.bacillus[,3:18], mean))
var <- as.vector(sapply(elap.gramneg.fac.bacillus[,3:18], var))
mean.var.elap <- data.frame(cbind(mean[1:16], var[1:16]))
colnames(mean.var.elap)[colnames(mean.var.elap) == "X1"] <- "Mean"
colnames(mean.var.elap)[colnames(mean.var.elap) == "X2"] <- "Variance"
mean.var.elap <- dplyr::mutate(mean.var.elap, Var.Mean.RATIO = Variance/Mean)
row.names(mean.var.elap) <- colnames(elap.gramneg.fac.bacillus[,3:18])
mean.var.elap[order(-mean.var.elap$Variance),]
```

<table class="table table-striped table-hover" >

<tr >

Mean
Variance
Var.Mean.RATIO
</tr>

<tbody >
<tr >

<td >Three.finger.toxins
</td>

<td >0.8113154
</td>

<td >0.1029969
</td>

<td >0.1269505
</td>
</tr>
<tr >

<td >Phospholipase.A2
</td>

<td >0.3975931
</td>

<td >0.0646446
</td>

<td >0.1625899
</td>
</tr>
<tr >

<td >Metalloproteinases
</td>

<td >0.2654288
</td>

<td >0.0498894
</td>

<td >0.1879579
</td>
</tr>
<tr >

<td >Waprin.Kunitz.BPTI
</td>

<td >0.1096811
</td>

<td >0.0138297
</td>

<td >0.1260897
</td>
</tr>
<tr >

<td >L.amino.acid.oxidase
</td>

<td >0.1439121
</td>

<td >0.0133742
</td>

<td >0.0929328
</td>
</tr>
<tr >

<td >Cysteine.rich.secretory.proteins
</td>

<td >0.0656119
</td>

<td >0.0030976
</td>

<td >0.0472111
</td>
</tr>
<tr >

<td >Serine.proteinases
</td>

<td >0.0242164
</td>

<td >0.0029264
</td>

<td >0.1208433
</td>
</tr>
<tr >

<td >Vespryn.ohanin
</td>

<td >0.0319233
</td>

<td >0.0029112
</td>

<td >0.0911924
</td>
</tr>
<tr >

<td >Snake.venom.growth.factors
</td>

<td >0.0802526
</td>

<td >0.0028766
</td>

<td >0.0358440
</td>
</tr>
<tr >

<td >Exonuclease.PDE.5..nuclotidases
</td>

<td >0.0279614
</td>

<td >0.0022487
</td>

<td >0.0804231
</td>
</tr>
<tr >

<td >Bradykinin.potentiating.peptides.and.natriuretic.peptides
</td>

<td >0.0102775
</td>

<td >0.0009697
</td>

<td >0.0943556
</td>
</tr>
<tr >

<td >C.type.lectins
</td>

<td >0.0076465
</td>

<td >0.0003691
</td>

<td >0.0482759
</td>
</tr>
<tr >

<td >peptides
</td>

<td >0.0011394
</td>

<td >0.0000272
</td>

<td >0.0239141
</td>
</tr>
<tr >

<td >Disintegrins
</td>

<td >0.0000000
</td>

<td >0.0000000
</td>

<td >NaN
</td>
</tr>
<tr >

<td >Waglerins
</td>

<td >0.0000000
</td>

<td >0.0000000
</td>

<td >NaN
</td>
</tr>
<tr >

<td >Hyaluronidase
</td>

<td >0.0000000
</td>

<td >0.0000000
</td>

<td >NaN
</td>
</tr>
</tbody>
</table>

Now we see some interesting information. First, Disintegrins, Waglerins, and Hyaluronidases are completely absent from these snakes.

Secondly, we see that Three-Finger toxins, Phospholipase A2, Metalloproteinases, Waprin-Kunitz,and L-Amino-Acid Oxidases vary most intensively. These are the proteins that we will use for predictive measures. However, we should probably see if any of them are strongly correlated first. Our cut-off for strong-correlation is p-value < 0.01.

![](http://cougrstats.files.wordpress.com/2018/02/unnamed-chunk-4-1.png)

Here we see that including Three Finger Toxins and L-Amino-Acid-Oxidases may introduce some redundancies within our data, so we are going to eliminate those. We will now double check those correlations for the three final candidate proteins.

![](http://cougrstats.files.wordpress.com/2018/02/unnamed-chunk-5-1.png)

## Model Selection and Model Cross Validation General Process

Our approach to model selection can be summarized briefly as an exhaustive model selection approach, using AIC as the primary cross-model comparison technique, and then validation through a non-parametric, permutation of AUC values for the best perfomring model. This overarching method though has a lot of jargon packed into it, so I will walk through a high-level description of the process and then work through the code for an in-depth example.

In order to discriminate between effective and non-effective protein compositions, we will employ a multiple logistic regression. This technique is similar to the univariate logistic regression; however, it occurs in multi-dimensional space. Like the univariate case, we are still trying to predict the probability of an event using continous predictor variables. In the case of multiple logistic regression though we can have have interaction terms, where the interaction of two proteins imparts non-additive effects on the probability of predicting effectiveness of a given snake venom. The problem we face though is: what is the appropriate logistic regression model we need to best describe the data? To answer, this question, we will perform an exhaustive approach to model selection, where we will iterate through each possible model that could be created with the data that we have. Each model will be created, and then AIC will be used to assess the "fit" of the model. AIC is a relatively standard metric used in model selection, where the fitness of a model is penalized by the number of predictors a model incorporates. A "better" AIC is closer to zero, whereas a "worse" AIC is much greater than zero. By using AIC as our primary selection criterion, we avoid overfitting the model by including too many parameters.

Once we identify the best performing models, we need to show that those models truly describe the data in a way that efficacy can be predicted consistently. To do this, we will use Receiver-Operator Characteristics (ROCs) which were pioneered in the telecommunications fields to assess loss of response for a given input. Essentially, an ROC compares specificity and sensitivity. ROCs following a 1:1 line indicate randomness. We can evaluate ROCs by calculating the area under the curve (AUC), where AUC = 0.5 indicates randomness and 1.0 indicates perfect model performance. However, it is possible that the AUC we received is due by chance, especially when working with smaller datasets. To test the significance of our AUC values we will use a permutation technique, where effectiveness data are assigned randomnly to a given protein composition, and AUC is recalculated. After repeating this procedures thousands of times, we will create a distribution of AUCs and compare our original AUC to this distribution. The beauty in this technique is that the p-value of our AUC is defined as the probability of finding an AUC higher than our original AUC, meaining we take the number of AUCs greater than our original value divided by the total number of AUCs. Assuming this value is significant, we can test our final model for accuracy of discrimination, defined as the sum of True Positives and True Negatives divided by the total number of samples.

## Exhaustive Model Selection Using glmulti

```r
elap.gramneg.fac.bacillus.model <-
  glmulti(effectiveness ~  Phospholipase.A2 + Metalloproteinases + Waprin.Kunitz.BPTI,
          data = elap.gramneg.fac.bacillus,
          level = 2,               #interactions not considered
          method = "h",            #Exhaustive approach
          crit = "aic",            #AIC as criteria
          confsetsize = 100,       # Keep 100 best models
          plotty = T, report =T,   #plot or interim reports
          fitfunction = "glm",
          family = binomial)

## Initialization...
## TASK: Exhaustive screening of candidate set.
## Fitting...
##
## After 50 models:
## Best model: effectiveness~1+Metalloproteinases+Waprin.Kunitz.BPTI:Phospholipase.A2+Waprin.Kunitz.BPTI:Metalloproteinases
## Crit= 44.9888030323714
## Mean crit= 54.7067328978274
```

![](http://cougrstats.files.wordpress.com/2018/02/unnamed-chunk-6-1.png)

```r
## Completed.

###Now we will show the top 5 formulas...
elap.gramneg.fac.bacillus.model@formulas[1:5]

## [[1]]
## effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI:Phospholipase.A2 +
##     Waprin.Kunitz.BPTI:Metalloproteinases
## <environment: 0x0000000026657fe8>
##
## [[2]]
## effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI +
##     Metalloproteinases:Phospholipase.A2 + Waprin.Kunitz.BPTI:Phospholipase.A2 +
##     Waprin.Kunitz.BPTI:Metalloproteinases
## <environment: 0x0000000026657fe8>
##
## [[3]]
## effectiveness ~ 1 + Metalloproteinases + Metalloproteinases:Phospholipase.A2 +
##     Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
## <environment: 0x0000000026657fe8>
##
## [[4]]
## effectiveness ~ 1 + Phospholipase.A2 + Metalloproteinases + Waprin.Kunitz.BPTI:Phospholipase.A2 +
##     Waprin.Kunitz.BPTI:Metalloproteinases
## <environment: 0x0000000026657fe8>
##
## [[5]]
## effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI +
##     Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
## <environment: 0x0000000026657fe8>
```

Our next step is to get some summary statistics of the other models, so that we know how they are all performing other than AIC. We will use pseudo-Rsquared and AUC to assess model performance. While there are many definition of pseudo-Rsquared, I am using the McFadden definition of pseudo-Rsquared, defined as (R^2 = 1 - \frac{Null Deviance}{Residual Deviance}). We will also calculate AUC for each model.

## Calculation of Pseudo-Rsquared and AUC for Cross Model Comparison

```r
AIC <- rep(0, length(elap.gramneg.fac.bacillus.model@formulas))
MODEL <- rep(NA, length(elap.gramneg.fac.bacillus.model@formulas))
AUC <- rep(0, length(elap.gramneg.fac.bacillus.model@formulas))
RSQUARED <- rep(0, length(elap.gramneg.fac.bacillus.model@formulas))
for(i in 1:length(elap.gramneg.fac.bacillus.model@formulas)){
  fit <- glm(paste(as.character(elap.gramneg.fac.bacillus.model@formulas[i])), data = elap.gramneg.fac.bacillus, family = binomial)
  MODEL[i] <- paste(as.character(elap.gramneg.fac.bacillus.model@formulas[i]))
  AIC[i] <- fit$aic
  predictpr <- predict(fit, type = "response")
  ROC <- pROC::roc(elap.gramneg.fac.bacillus$effectiveness ~ predictpr)
  AUC[i] <- pROC::auc(ROC)
  RSQUARED[i] <- 1 - (fit$deviance/fit$null.deviance)
}
INDEX <- seq(1:length(elap.gramneg.fac.bacillus.model@formulas))
elap.gramneg.fac.bacillus.fits <- data.frame(INDEX, MODEL, AIC, RSQUARED, AUC)
elap.gramneg.fac.bacillus.fits$MODEL <- as.character(elap.gramneg.fac.bacillus.fits$MODEL)
elap.gramneg.fac.bacillus.fits$AIC <- as.numeric(elap.gramneg.fac.bacillus.fits$AIC)
elap.gramneg.fac.bacillus.fits$RSQUARED <- as.numeric(elap.gramneg.fac.bacillus.fits$RSQUARED)
elap.gramneg.fac.bacillus.fits$AUC <- as.numeric(elap.gramneg.fac.bacillus.fits$AUC)
```

<table style="margin-left:auto;margin-right:auto;" class="table table-striped table-hover" >

<tr >
INDEX
MODEL
AIC
RSQUARED
AUC
</tr>

<tbody >
<tr >

<td style="text-align:right;" >1
</td>

<td style="text-align:left;" >effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
</td>

<td style="text-align:right;" >44.98880
</td>

<td style="text-align:right;" >0.3733679
</td>

<td style="text-align:right;" >0.8596491
</td>
</tr>
<tr >

<td style="text-align:right;" >2
</td>

<td style="text-align:left;" >effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI + Metalloproteinases:Phospholipase.A2 + Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
</td>

<td style="text-align:right;" >45.91485
</td>

<td style="text-align:right;" >0.4254442
</td>

<td style="text-align:right;" >0.8706140
</td>
</tr>
<tr >

<td style="text-align:right;" >3
</td>

<td style="text-align:left;" >effectiveness ~ 1 + Metalloproteinases + Metalloproteinases:Phospholipase.A2 + Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
</td>

<td style="text-align:right;" >46.29477
</td>

<td style="text-align:right;" >0.3851257
</td>

<td style="text-align:right;" >0.8574561
</td>
</tr>
<tr >

<td style="text-align:right;" >4
</td>

<td style="text-align:left;" >effectiveness ~ 1 + Phospholipase.A2 + Metalloproteinases + Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
</td>

<td style="text-align:right;" >46.97107
</td>

<td style="text-align:right;" >0.3736684
</td>

<td style="text-align:right;" >0.8596491
</td>
</tr>
<tr >

<td style="text-align:right;" >5
</td>

<td style="text-align:left;" >effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI + Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases
</td>

<td style="text-align:right;" >46.98622
</td>

<td style="text-align:right;" >0.3734117
</td>

<td style="text-align:right;" >0.8530702
</td>
</tr>
<tr >

<td style="text-align:right;" >6
</td>

<td style="text-align:left;" >effectiveness ~ 1 + Phospholipase.A2 + Metalloproteinases + Waprin.Kunitz.BPTI + Waprin.Kunitz.BPTI:Metalloproteinases
</td>

<td style="text-align:right;" >47.17980
</td>

<td style="text-align:right;" >0.3701322
</td>

<td style="text-align:right;" >0.8508772
</td>
</tr>
</tbody>
</table>

For this model selection round, our best model was effectiveness ~ 1 + Metalloproteinases + Waprin.Kunitz.BPTI + Metalloproteinases:Phospholipase.A2 + Waprin.Kunitz.BPTI:Phospholipase.A2 + Waprin.Kunitz.BPTI:Metalloproteinases, which is indexed as Model 2. Although Model 1 has a better performing AIC, Model 2 has a better R-squared and AUC.

Now that we say Model 2 is our best model, we can evaluate this model by itself, as opposed to the previous step, which compared it to all other models. Essentially, we want to see how well model performs in general. To do this, we will calculate the ROC curve, confusion matrix, and accuracy for the best performing model. Then, we will examine the False Positives and False Negatives that were returned.

## Model Performance Using Confusion Matrix and Accuracy

```r
fit <- glm(paste(as.character(elap.gramneg.fac.bacillus.model@formulas[2])), data = elap.gramneg.fac.bacillus, family = binomial)
predictpr <- predict(fit, type = "response")
elap.gramneg.fac.bacillus$PREDICTION <- predictpr
elap.gramneg.fac.bacillus <- data.frame(elap.gramneg.fac.bacillus)
plot(pROC::roc(elap.gramneg.fac.bacillus$effectiveness ~ elap.gramneg.fac.bacillus$PREDICTION), main = "ROC for best model")
```

![](http://cougrstats.files.wordpress.com/2018/02/unnamed-chunk-8-1.png)

```r
elap.gramneg.fac.bacillus <- elap.gramneg.fac.bacillus %>%
  dplyr::mutate(PREDICTION = ifelse(as.numeric(PREDICTION) < 0.5, 0, 1))
table <- table(Reality = elap.gramneg.fac.bacillus$effectiveness, Prediction = elap.gramneg.fac.bacillus$PREDICTION)
table

##        Prediction
## Reality  0  1
##       0 13  6
##       1  4 20

accuracy <- (table[1,1]+table[2+2])/sum(table)
paste("The accuracy of this model is: ", accuracy*100, "%")

## [1] "The accuracy of this model is:  76.7441860465116 %"

#False Positives
FP <- elap.gramneg.fac.bacillus %>%
  filter(effectiveness == 0 & PREDICTION == 1)%>%
  dplyr::select(Snake.species, Phospholipase.A2, Metalloproteinases, Waprin.Kunitz.BPTI)
#False Negatives
FN <- elap.gramneg.fac.bacillus %>%
  filter(effectiveness == 1 & PREDICTION == 0)%>%
  dplyr::select(Snake.species, Phospholipase.A2, Metalloproteinases, Waprin.Kunitz.BPTI)
```

**False Postives**

<table style="margin-left:auto;margin-right:auto;" class="table table-striped table-hover" >

<tr >
Snake.species
Phospholipase.A2
Metalloproteinases
Waprin.Kunitz.BPTI
</tr>

<tbody >
<tr >

<td style="text-align:left;" >Naja melanoleuca
</td>

<td style="text-align:right;" >0.4455223
</td>

<td style="text-align:right;" >0.2796752
</td>

<td style="text-align:right;" >0.1993068
</td>
</tr>
<tr >

<td style="text-align:left;" >Naja melanoleuca
</td>

<td style="text-align:right;" >0.4455223
</td>

<td style="text-align:right;" >0.2796752
</td>

<td style="text-align:right;" >0.1993068
</td>
</tr>
<tr >

<td style="text-align:left;" >Naja naja
</td>

<td style="text-align:right;" >0.4058956
</td>

<td style="text-align:right;" >0.0950112
</td>

<td style="text-align:right;" >0.0360633
</td>
</tr>
<tr >

<td style="text-align:left;" >Naja naja
</td>

<td style="text-align:right;" >0.4058956
</td>

<td style="text-align:right;" >0.0950112
</td>

<td style="text-align:right;" >0.0360633
</td>
</tr>
<tr >

<td style="text-align:left;" >Naja naja
</td>

<td style="text-align:right;" >0.4058956
</td>

<td style="text-align:right;" >0.0950112
</td>

<td style="text-align:right;" >0.0360633
</td>
</tr>
<tr >

<td style="text-align:left;" >Naja nigricollis
</td>

<td style="text-align:right;" >0.5066873
</td>

<td style="text-align:right;" >0.1908939
</td>

<td style="text-align:right;" >0.0000000
</td>
</tr>
</tbody>
</table>

**False Negatives**

<table style="margin-left:auto;margin-right:auto;" class="table table-striped table-hover" >

<tr >
Snake.species
Phospholipase.A2
Metalloproteinases
Waprin.Kunitz.BPTI
</tr>

<tbody >
<tr >

<td style="text-align:left;" >Naja haje
</td>

<td style="text-align:right;" >0.1390113
</td>

<td style="text-align:right;" >0.306783
</td>

<td style="text-align:right;" >0.1198695
</td>
</tr>
<tr >

<td style="text-align:left;" >Naja haje
</td>

<td style="text-align:right;" >0.1390113
</td>

<td style="text-align:right;" >0.306783
</td>

<td style="text-align:right;" >0.1198695
</td>
</tr>
<tr >

<td style="text-align:left;" >Ophiophagus hannah
</td>

<td style="text-align:right;" >0.1854521
</td>

<td style="text-align:right;" >0.440098
</td>

<td style="text-align:right;" >0.1471594
</td>
</tr>
<tr >

<td style="text-align:left;" >Ophiophagus hannah
</td>

<td style="text-align:right;" >0.1854521
</td>

<td style="text-align:right;" >0.440098
</td>

<td style="text-align:right;" >0.1471594
</td>
</tr>
</tbody>
</table>

Our model looks like it is performing pretty well. However, we want to see whether or not the model is "significant". That is to say – how well does it perform in comparison to a random assignment of efficacy. To do this, we will bring in the permutation technique below.

## Permutation to Assess Model Significance

```r
i <- 1
nreps <- 1000
AUC.repo <- rep(0, nreps)
elap.gramneg.fac.bacillus.permute <- elap.gramneg.fac.bacillus
for(i in 1:nreps) {
  elap.gramneg.fac.bacillus.permute$effectiveness <- sample(elap.gramneg.fac.bacillus.permute$effectiveness,
                    size = length(elap.gramneg.fac.bacillus.permute$effectiveness),
                    replace = FALSE)
  fit <- glm(paste(as.character(elap.gramneg.fac.bacillus.model@formulas[2])), data = elap.gramneg.fac.bacillus, family = binomial)
  predictpr <- predict(fit, type = "response")
  ROC <- pROC::roc(elap.gramneg.fac.bacillus.permute$effectiveness ~ predictpr)
  AUC.repo[i] <- pROC::auc(ROC)
}
hist(AUC.repo, xlim = c(0,1), main = "Histogram of Permuted AUCs")
abline(v = elap.gramneg.fac.bacillus.fits$AUC[2], col = "red")
```

![](http://cougrstats.files.wordpress.com/2018/02/unnamed-chunk-9-1.png)

```r
prop.above <- length(AUC.repo[AUC.repo > elap.gramneg.fac.bacillus.fits$AUC[1]])/length(AUC.repo)
paste("The p-value for this model is: ", prop.above)

## [1] "The p-value for this model is:  0"
```

We have no models with a higher AUC, meaning that our model is probably not the product of a random assignment of AUC values! We can be confident that our model is the best performing model, and the parameters are likely not due to chance.
