---
title: Introduction to Time Series in R
author: cougrstats
date: '2018-10-24'
categories:
  - Package Introductions
tags:
  - acf
  - arima
  - astsa
  - forcasting
  - pacf
  - time series
slug: introduction-to-time-series-in-r
---

_By Alli Cramer_

```r
library(astsa)
```

# Lynx Data set

For this example, we will be using a Lynx population dataset. You can find the dataset here: the "Annual Number of Lynx Trapped on the Mackenzie River from 1821-1934.

From: <https://datamarket.com/data/set/22vj/annual-number-of-lynx-trapped-mackenzie-river-1821-1934#!ds=22vj&display=line>

##Plot the series and examine the main features of the graph, checking in particular whether there is:

(a) a trend,

(b) a seasonal component,

© any apparent sharp changes in behavior, (d) any outlying observations. Explain in detail.

```r
lynx = read.csv("C:/Users/allison.cramer/OneDrive/Teaching/R Working Group/ExampleData/TimeSeries/annual-number-of-lynx-trapped-ma.CSV", header = T)
head(lynx)

##   Year Lynx.trapped
## 1 1821          269
## 2 1822          321
## 3 1823          585
## 4 1824          871
## 5 1825         1475
## 6 1826         2821

plot(lynx, type= "l", main = "Figure 1 - Annual Number of Lynx Trapped on the Mackenzie River from 1821-1934")
```

![plot of chunk looking at data](http://cougrstats.files.wordpress.com/2018/10/looking-at-data-1.png)

To the right is the plot of the raw Lynx data. From this initial observation it appears that there is a seasonal component to the data, but that there is a minimal trend and the variance is rather stable. There are a few observations that seem to be outliers - the three large spies around years 1829, 1865, and 1905 - however I am unconvinced that they are outliers as they appear evenly spaced apart and are all about the same height.

## Autocorellation

Lets look at the autocorellation function to see what patterns we observe in the data

```r
#getting rid of the time column (i.e. turning it into a ts dataset)
ts = ts(lynx, start = 1821, end = 1934)
dat= ts[,2]

acf(dat, 50, main = "Figure 2.1 - ACF of raw Lynx Data")
```

![plot of chunk turning to time series](http://cougrstats.files.wordpress.com/2018/10/turning-to-time-series-1.png)

```r
pacf(dat, 50, main = "Figure 2.2 - PACF of raw Lynx Data")
```

![plot of chunk turning to time series](http://cougrstats.files.wordpress.com/2018/10/turning-to-time-series-2.png)

To achieve stationary residuals the seasonality of the data was investigated. Examining the ACF seemed to indicate a 10 year seasonal trend (Fig 2), however differencing the data did not improve the oscillations present in the ACF. It seems that the peaks, despite their apparent periodicity, are not predictable. Because of this we will not make any models that had a seasonal component.

##looking at the variance
Lets look at the variance for the first half of the dataset, and the second half.

```r
data = dat
first = data[1:(length(data)/2)]
second = data[(length(data)/2+1): (length(data))]

var(first)

## [1] 2316637

mean(first)

## [1] 1458.158

var(second)

## [1] 2745091

mean(second)

## [1] 1617.877
```

The second half has slightly more variance.

##Lets transform the data to depress this variance.
We can log the data to depress the variance a bit

```r
d.log = log(dat)
plot(d.log)
```

![plot of chunk log transform](http://cougrstats.files.wordpress.com/2018/10/log-transform-1.png)

```r
data = d.log
first = data[1:(length(data)/2)]
second = data[(length(data)/2+1): (length(data))]

var(first)

## [1] 1.382848

mean(first)

## [1] 6.703306

var(second)

## [1] 1.952537

mean(second)

## [1] 6.66856

var(first) - var(second)

## [1] -0.569689

hist(dat, main = "Figure 3 - untransformed Lynx data")
```

![plot of chunk log transform](http://cougrstats.files.wordpress.com/2018/10/log-transform-2.png)

```r
hist(d.log, main = "Figure 4 - transformed Lynx data")
```

![plot of chunk log transform](http://cougrstats.files.wordpress.com/2018/10/log-transform-3.png)

The log transformed is MUCH better.

## Trying to "detrend"

```r
trend =
d.log.detrend <- resid(lm(d.log ~ time(d.log)))

plot(d.log.detrend, type = "l", main = "Figure 5 - detrended and log transformed Lynx data")
```

![plot of chunk detrending](http://cougrstats.files.wordpress.com/2018/10/detrending-1.png)

```r
hist(d.log.detrend)
```

![plot of chunk detrending](http://cougrstats.files.wordpress.com/2018/10/detrending-2.png)

```r
#this looks pretty good now.
```

We can also attempt to remove a seasonal component to the data. Below is the code for that, but we won't run it because it doesn't improve stationarity. So, despite what it appears to be, once log transformed and detrended the lynx data is already stationary!

##Removing seasonal trends - how you would do it, though it doesn't work for this dataset.

```r
#the pacf component appears to be an AR(2)
#attempt at removing a "seasonal" component - to no avail.
d.log
for(i in c(1:10)){
plot(diff(dat, lag = i))
}

#differencing makes almost no difference.
#none of the plots look improved.
#It seems that the peaks, despite their apparent periodicity, are not predictable.
```

## Choose a model to fit the residuals.

Lets test som models on this data. We are fitting "ARIMA" models, or Auto Regressive Integrated Moving Average models. These models have three components, p, d, and q.
The parameters of the ARIMA model are defined as follows:

p: The number of lag observations included in the model, also called the lag order.
d: The number of times that the raw observations are differenced, also called the degree of differencing.
q: The size of the moving average window, also called the order of moving average.

The syntax for ARIMA models is generally Arima(p,d,q). So in the example below, we are comparing a ARIMA(2,0,1) and an ARIMA(2,0,2).

```r
#lets test some models on this data.

acf.d = acf2(d.log.detrend, 50)
```

![plot of chunk model fitting](http://cougrstats.files.wordpress.com/2018/10/model-fitting-1.png)

```r
mod.1 = sarima(d.log.detrend, 2,0,1)

## initial  value 0.249436
## iter   2 value -0.309862
## iter   3 value -0.370696
## iter   4 value -0.477115
## iter   5 value -0.509287
## iter   6 value -0.534067
## iter   7 value -0.571560
## iter   8 value -0.595904
## iter   9 value -0.621684
## iter  10 value -0.651739
## iter  11 value -0.652590
## iter  12 value -0.657683
## iter  13 value -0.660312
## iter  14 value -0.661080
## iter  15 value -0.661131
## iter  16 value -0.661132
## iter  17 value -0.661132
## iter  17 value -0.661132
## iter  17 value -0.661132
## final  value -0.661132
## converged
## initial  value -0.655726
## iter   2 value -0.655820
## iter   3 value -0.655844
## iter   4 value -0.655875
## iter   5 value -0.655891
## iter   6 value -0.655894
## iter   7 value -0.655895
## iter   7 value -0.655895
## iter   7 value -0.655895
## final  value -0.655895
## converged
```

![plot of chunk model fitting](http://cougrstats.files.wordpress.com/2018/10/model-fitting-2.png)

```r
mod.2 = sarima(d.log.detrend, 2,0,2)

## initial  value 0.249436
## iter   2 value -0.320525
## iter   3 value -0.442471
## iter   4 value -0.498334
## iter   5 value -0.516408
## iter   6 value -0.526464
## iter   7 value -0.530492
## iter   8 value -0.536595
## iter   9 value -0.601440
## iter  10 value -0.609549
## iter  11 value -0.640524
## iter  12 value -0.652371
## iter  13 value -0.658401
## iter  14 value -0.658846
## iter  15 value -0.660549
## iter  16 value -0.664565
## iter  17 value -0.664603
## iter  18 value -0.664611
## iter  19 value -0.664614
## iter  20 value -0.664614
## iter  20 value -0.664614
## iter  20 value -0.664614
## final  value -0.664614
## converged
## initial  value -0.659301
## iter   2 value -0.659396
## iter   3 value -0.659422
## iter   4 value -0.659452
## iter   5 value -0.659462
## iter   6 value -0.659466
## iter   7 value -0.659467
## iter   8 value -0.659468
## iter   8 value -0.659468
## iter   8 value -0.659468
## final  value -0.659468
## converged
```

![plot of chunk model fitting](http://cougrstats.files.wordpress.com/2018/10/model-fitting-3.png)

```r
mod.1$AICc

## [1] -0.2421902

mod.2$AICc

## [1] -0.2299404
```

Based on the ACF and PACF of the now stationary series, the better model from our two models is an ARIMA(2,0,1) model (Fig. 6). From the ACF we see that it is most likely MA(1), though MA(2) is also a possibility. From the PACF we can see that it is AR(2) due to the two strong peaks.

###What is the model obtained by using AICC? Is it same as one of the models suggested by ACF/PACF?
We can compare a number of models this way. We will not run this code because it takes up lots of space, but feel free to run and observe on your own.

```r
#generating models with p and q values of either 0, 1, or 2.

P <-0
S <- 0
Q <- 0
bic.m <- matrix(c(rep(NA,9)),3,3)
aic.m <- matrix(c(rep(NA,9)),3,3)
logL.m <- matrix(c(rep(NA,9)),3,3)
for (p in c(0,1,2))
  for(q in c(0,1,2))
  {
    smod <- sarima(d.log.detrend, p, 0, q, 0, 0, 0, 0) # fit model
    bic.m[p+1,q+1] <- smod$BIC
    aic.m[p+1,q+1] <- smod$AICc
    logL.m[p+1,q+1] <- -smod$fit$loglik
  }

bic.m
aic.m
```

To examine other models besides the one selected based off of the ACF and PACF plots, models were generated used for-loops and then compared using BIC and AICc values (Tables 1, 2). The BIC matrix shows that the model supported by the BIC values (i.e. the lowest matrix value) is an ARMA(2, 0, 0) with a BIC value of -1.1857. This is almost indistinguishable from the next lowest model, an ARMA(2,0,1), which is the model supported by my model choice based off of the ACF and PACF, BIC value of -1.1686. When looking at the AICc values the lowest value is an ARMA(2,0,2) model, however the AICc values are all essentially the same. In fact, none of the values are far enough apart to merit real distinction between models.

##Estimate the parameters of the model and write down the model in algebraic form.

```r
#turning model into an arima() model to get the coef. and variance estimates

mod.1.1 = arima(d.log.detrend, c(2,0,1))

#The equation for this model is

mod.1.1$coef

##          ar1          ar2          ma1    intercept
##  1.475280551 -0.816861229 -0.233232740 -0.001533242

    #Xt = 1.47531*Xt-1 + -0.8169*Xt-2 + -0.2332*Wt-1 + Wt

#(d) What is the variance estimate?

var = mod.1.1$var.coef
var

##                     ar1           ar2           ma1     intercept
## ar1        4.760036e-03 -3.607999e-03 -0.0055806041 -6.405797e-05
## ar2       -3.607999e-03  3.689721e-03  0.0039856618  6.112233e-05
## ma1       -5.580604e-03  3.985662e-03  0.0150024841  1.373257e-04
## intercept -6.405797e-05  6.112233e-05  0.0001373257  1.179494e-02
```

Because the models are essentially identical, we'll am going with the initial model choice of an ARMA(2,0,1). This model can be written as

X_t=1.4753X_(t-1)+ -0.8169X_(t-2)+ -0.2332W_(t-1)

We estimated the parameters using the Maximum Likelihood Method (which is the default in both arima() and sarima()). We used this used that estimate method because the MLE method is preferred for ARMA(p,q) models and this model was an ARMA(2,1) (Shumway and Stoffer pg. 78) .

The variance in the estimates was produced using the arima() command as well, and can be seen above.

##Do the diagnostic checking, plot the residuals of the fitted model.

```r
#Plot the autocorrelations of the residuals. Are their any outliers?

resid = mod.1.1$residuals

plot(resid, main = "Figure 7 - Plot of Residuals")
```

![plot of chunk diagnostics](http://cougrstats.files.wordpress.com/2018/10/diagnostics-1.png)

```r
acf(resid, 1000)
```

![plot of chunk diagnostics](http://cougrstats.files.wordpress.com/2018/10/diagnostics-2.png)

```r
  #the plot of the residuals seems to show that, although very spiky, there are not any dramatic outliers.
  #the acf plot shows that this could be improved a bit, but we already knew that since the model is relatively poor. :/

#Perform tests (chi-squared, and so on) of randomness and obtain the p-values.

resid.nom = as.numeric(mod.1.1$residuals[1:114])
hist(resid.nom, main = "Figure 8 - Histogram of Residuals")
```

![plot of chunk diagnostics](http://cougrstats.files.wordpress.com/2018/10/diagnostics-3.png)

```r
#pretty dang normal

#to test for the randomness I am using a Kolmogorov-Smirnov test.
#This test is like the chi squared test in that it compares my distribution to an expected distributin (in this case rnorm)
#but this test can also take continuous vectors

randomness.test = ks.test(resid.nom, rnorm(
  n = length(resid.nom),
  mean = mean(resid.nom),
  sd = sd(resid.nom))
  )

randomness.test$p.value

## [1] 0.6634279

#the p-value shows that the residuals are essentially random
```

We ran model diagnostics by looking at a plot of the residuals, a histogram of the residuals, and performing a Kolmogorov-Smirnov test. The Kolmogorov-Smirnov test is like the Chi Squared test in that it compares the distribution to an expected distributing (in this case rnorm) but this test can also take continuous vectors. We also investigated the Ljung-Box plot provided by the sarima() function, and a long term ACF of the residuals.

From the residuals we can conclude that the model is satisfactory, though not optimum. By looking at the Ljung-Box values shows that at higher lags they are below the interval (i.e. not independent) yet looking at a long term ACF of the residuals shows that the longer lags are not having an impact. The plot of the residuals, although very spiky, showed no dramatic outliers and the histogram was relatively normal, Figures 7 and 8 respectively. The Kolmogrorov-Smirnov test showed that the residuals were essentially random (p-value = 0.7727)). Based on the Kolmogorov-Smirnov test, and the histogram of the residuals, the model is ok.

## Forecast the last 10 values based on our one chosen model.

```r
#Plot the original series and the forecasts for both of them.

short = d.log.detrend[1:(length(d.log.detrend)-10)]

forcasted = sarima.for(short, p = 2, d = 0, q = 1, n.ahead = 10)
```

![plot of chunk forcasting](http://cougrstats.files.wordpress.com/2018/10/forcasting-1.png)

```r
forcasted$pred

## Time Series:
## Start = 105
## End = 114
## Frequency = 1
##  [1]  1.25441563  1.03999995  0.50228428 -0.11783032 -0.59539761
##  [6] -0.79468001 -0.69886516 -0.39410970 -0.02162615  0.28014816

#Now lets calculate the 95% confidence intervals for the prediction values.

lower = forcasted$pred-1.96*forcasted$se
upper = forcasted$pred+1.96*forcasted$se

lower

## Time Series:
## Start = 105
## End = 114
## Frequency = 1
##  [1]  0.2150928 -0.6093246 -1.4499465 -2.1324971 -2.6135223 -2.8949890
##  [7] -2.9338470 -2.7229627 -2.3756480 -2.0740342

upper

## Time Series:
## Start = 105
## End = 114
## Frequency = 1
##  [1] 2.293738 2.689325 2.454515 1.896836 1.422727 1.305629 1.536117
##  [8] 1.934743 2.332396 2.634331

#Plotting it all together
plot(d.log.detrend, type = "l", main = "Figure 9 - Real Lynx data and Forecasted Values")

lines(forcasted$pred, type = "p", col = "red", lwd = 2)
#adding confidence intervals
lines(upper, type = "l", lty=2, lwd=1, col = "blue")
lines(lower, type = "l", lty=2, lwd=1, col = "blue")
```

![plot of chunk forcasting](http://cougrstats.files.wordpress.com/2018/10/forcasting-2.png)
