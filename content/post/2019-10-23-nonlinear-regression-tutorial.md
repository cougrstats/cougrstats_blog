---
title: Nonlinear regression tutorial
author: Abby Hudak
date: '2019-10-23'
categories:
  - Research Profiles
tags:
  - nonlinear regression
  - regression
slug: nonlinear-regression-tutorial
---

_By Abby Hudak_

When relationships between variables is not linear you can try:
1) transforming data to linearize the relationship
2) fit non-linear functions to data (use nls example)
3) fit polynomial or spline models to data (use growthrates package example)

**linear regression:** dependent variable = constant + parameter x indepenent variable + p x IV +....

y = B0 + B1X1 + B2X2 + ...

This doesn't mean you can't fit a curve! What makes it linear is that _parameters_ are linear. You may have nonlinear independent variables ex) y = B0 +B1X1 +B2X(2)1. Instead of exponentially changing the independent variable, you could have log or inverse terms, etc.

**nonlinear regression:** Anything else. Can be crazy stuff like: B1 x cos(X+B4) + B2 x cos(2*X+B4)+B3. This makes it important that you do research to understand what functional form your data may take.

**Nonlinear least squares approach**

Nonlinear least squares is a good way to estimate parameters to fit nonlinear data. Uses a linear function to estimate a nonlinear one and iteratively works to find best parameter values.

```r
#simulate some data
#set random number generator
set.seed(2019)
x<-seq(0,50,1)
y<-((runif(1,10,20)*x)/(runif(1,0,10)+x))+rnorm(51,0,1)
#for simple models nls find good starting values for the parameters even if it throws a warning

#Michaelis-Menten equation
m<-nls(y~a*x/(b+x))

## Warning in nls(y ~ a * x/(b + x)): No starting values specified for some parameters.
## Initializing 'a', 'b' to '1.'.
## Consider specifying 'start' or using a selfStart model

m

## Nonlinear regression model
##   model: y ~ a * x/(b + x)
##    data: parent.frame()
##      a      b
## 17.908  7.645
##  residual sum-of-squares: 51.78
##
## Number of iterations to convergence: 6
## Achieved convergence tolerance: 1.077e-06

#will throw warning, but should work
#get some estimation of goodness of fit
cor(y,predict(m))

## [1] 0.9658715

#plot
plot(x,y)
lines(x,predict(m),col="red",lwd=3)
```

![](https://cougrstats.files.wordpress.com/2019/10/nonlinear1.png)

```r
#simulate some data, this without a priori knowledge of the parameter value
x<-seq(0,50,1)
y<-runif(1,5,15)*exp(-runif(1,0.01,0.05)*x)+rnorm(51,0,0.5)
#visually estimate some starting parameter values
plot(x,y)

#from this graph set approximate starting values
a_start<-8 #param a is the y value when x=0
b_start<-log(0.1)/(50*8) #b is the decay rate. k=log(A)/(A(intial)*t)

#model
m1<-nls(y~a*exp(-b*x),start=list(a=a_start,b=b_start))
m1

## Nonlinear regression model
##   model: y ~ a * exp(-b * x)
##    data: parent.frame()
##       a       b
## 8.59328 0.03544
##  residual sum-of-squares: 7.588
##
## Number of iterations to convergence: 6
## Achieved convergence tolerance: 7.615e-07

#get some estimation of goodness of fit (should be closer to 1)
cor(y,predict(m1))

## [1] 0.9833285

#plot the fit
lines(x,predict(m1),col="red",lty=2,lwd=3)
```

![](https://cougrstats.files.wordpress.com/2019/10/nonlinear2.png)

**using differential equations**

```r
library(deSolve) #this package is good for solving differential equations
#simulating some population growth from the logistic equation and estimating the parameters using nls

#defining a function
log_growth <- function(Time, State, Pars) {
  with(as.list(c(State, Pars)), {
    dN <- R*N*(1-N/K)
    return(list(c(dN)))
  })
}
#Time is the time intervals, States are the variable names, Pars and parameters

#pars, N_int, tmes are used to simulate data
pars  <- c(R=0.2,K=1000) #the parameters for the logisitc growth
N_ini <- c(N=1) #the initial numbers
times <- seq(0, 50, by = 1) #the time step to evaluate

#the ODE (ordinary differential equation)
out <- ode(N_ini, times, log_growth, pars)
plot(out)
```

![](https://cougrstats.files.wordpress.com/2019/10/nonlinear3.png)

```r
#add some random variation to it
N_obs<-out[,2]+rnorm(51,0,50)
#remove numbers less than 1
N_obs<-ifelse(N_obs<1,1,N_obs)
#plot
plot(times,N_obs)

#Not having starting values only works sometimes with simple data and functions like in the first example.
#notice how m3 WON'T work.Remember nls iteritavely runs to converge and this will not converge in under 30 iterations
#m3<-nls(N_obs~K*N0*exp(R*times)/(K+N0*(exp(R*times)-1)))

#getInitial gives guesses on parameter values based on data
#SSlogis is a selfStarting model
SS<-getInitial(N_obs~SSlogis(times,alpha,xmid,scale),data=data.frame(N_obs=N_obs,times=times))
#follows this equation: N(t)=alpha/(1+e+((xmid-t)/scale)
SS

##      alpha       xmid      scale
## 991.798725  34.112932   5.045119

#need to do some algebra to get parameterization right
#we used a different parametrization
K_start<-SS["alpha"]
R_start<-1/SS["scale"]
N0_start<-SS["alpha"]/(exp(SS["xmid"]/SS["scale"])+1)
#the formula (not set up as differential equation) for the model
log_formula<-formula(N_obs~K*N0*exp(R*times)/(K+N0*(exp(R*times)-1)))

#fit the model
m4<-nls(log_formula,start=list(K=K_start,R=R_start,N0=N0_start))

#estimated parameters
summary(m4)

##
## Formula: N_obs ~ K * N0 * exp(R * times)/(K + N0 * (exp(R * times) - 1))
##
## Parameters:
##           Estimate Std. Error t value Pr(>|t|)
## K.alpha  991.79872   29.86851  33.205   <2e-16 ***
## R.scale    0.19821    0.01338  14.817   <2e-16 ***
## N0.alpha   1.14659    0.47931   2.392   0.0207 *
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
##
## Residual standard error: 44.08 on 48 degrees of freedom
##
## Number of iterations to convergence: 0
## Achieved convergence tolerance: 4.177e-06

#get some estimation of goodness of fit (should be closer to 1)
cor(N_obs,predict(m4))

## [1] 0.9925536

#plot
lines(times,predict(m4),col="red",lty=2,lwd=3)
```

![](https://cougrstats.files.wordpress.com/2019/10/nonlinear4.png)

**Maximum likelihood approach** see nlme package. A bit more powerful and reliable method than nls.

**growthrates package**
Finding best fit was a bit annoying for fitting a somewhat simple function. Fit a spline! A spline doesn't just make a line through data, it actually goes through each data point and fits a cubic ploynomial between two points. So the spline is a piecewise snapshot of the best fit. Allows for good interpolation.

function **fit_spline** fits a spline to just one and solves the cubic system of equations.

These youtube videos explain the calculus and concepts well: <https://www.youtube.com/watch?v=BqZXS3n75l0>

```r
library(growthrates)

time<-rep(1:25, 8)
y<-grow_logistic(time, c(y0=0.2, mumax=0.3, K=4))[,"y"]
y<-jitter(y, factor=1, amount=0.3)
data<-data.frame(cbind(time,y))
data<-data[order(data$y),]
data$ID<-c(rep(1:10,20))
plot(time,y)
```

![](https://cougrstats.files.wordpress.com/2019/10/nonlinear5.png)

```r
splitted.data <- multisplit(data, c("ID"))

## show which experiments are in splitted.data
names(splitted.data)

##  [1] "1"  "2"  "3"  "4"  "5"  "6"  "7"  "8"  "9"  "10"

## get table from single individual.  Or could be an experiment, or batch, or block, etc.
dat <- splitted.data[["1"]]
dat[1, 2] = 0.03

fit0 <- fit_spline(dat$time, dat$y)
plot(fit0, col="green", lwd=3)
summary(fit0)

## Fitted smoothing spline:
## Call:
## smooth.spline(x = time, y = ylog)
##
## Smoothing Parameter  spar= 0.6721364  lambda= 0.006882113 (12 iterations)
## Equivalent Degrees of Freedom (Df): 3.685259
## Penalized Criterion (RSS): 2.029662
## GCV: 0.3015
##
## Parameter values of exponential growth curve:
## Maximum growth at x= 1.001382 , y= 0.1644875
## y0 = 0.1145593
## mumax = 0.3612431
##
## r2 of log transformed data= 0.8652797

#can get maximum growth rate from here.  Plot will show the exponetial curve (blue line) from max rate

## initial parameters
p <- c(coef(fit0), K = max(dat$y))

## avoid negative parameters
lower = c(y0 = 0, mumax = 0, K = 0)

fit3<-fit_growthmodel(grow_logistic, p=p, time=data$time, y=data$y)
lines(fit3, col="red", lwd=3)
```

![](https://cougrstats.files.wordpress.com/2019/10/nonlinear6.png)

```r
summary(fit3)

##
## Parameters:
##       Estimate Std. Error t value Pr(>|t|)
## y0    0.188670   0.012562   15.02   <2e-16 ***
## mumax 0.301080   0.007458   40.37   <2e-16 ***
## K     4.027982   0.029659  135.81   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
##
## Residual standard error: 0.1713 on 197 degrees of freedom
##
## Parameter correlation:
##            y0   mumax       K
## y0     1.0000 -0.9448  0.5116
## mumax -0.9448  1.0000 -0.6615
## K      0.5116 -0.6615  1.0000

#Get parameters for the entire population

fit4<-all_growthmodels(
          y ~ grow_logistic(time, parms) | ID,
          data = data, p = p, lower = lower) #gives parameters for each individual

results(fit4, extended=TRUE) #extended gives you time estimates of saturation values.

##    ID        y0     mumax        K turnpoint     sat1     sat2     sat3
## 1   1 0.1775788 0.3186817 3.922830  9.567004 13.69952 15.84286 18.80644
## 2   2 0.2131942 0.2973178 3.962413  9.643233 14.07267 16.37004 19.54655
## 3   3 0.1958260 0.2873056 4.118416 10.432393 15.01620 17.39362 20.68083
## 4   4 0.1639432 0.3095515 4.076656 10.248580 14.50299 16.70954 19.76054
## 5   5 0.1514473 0.3280776 3.963867  9.832374 13.84654 15.92849 18.80720
## 6   6 0.1988192 0.2916016 4.077459 10.188041 14.70430 17.04671 20.28550
## 7   7 0.2349602 0.2860918 4.040224  9.733663 14.33695 16.72443 20.02562
## 8   8 0.1929363 0.2827270 4.130590 10.667467 15.32552 17.74143 21.08189
## 9   9 0.1830012 0.3046824 4.035454 10.000489 14.32289 16.56470 19.66445
## 10 10 0.1680191 0.3139180 4.027611  9.984249 14.17949 16.35534 19.36390
##           r2
## 1  0.9896373
## 2  0.9803218
## 3  0.9865337
## 4  0.9893162
## 5  0.9840925
## 6  0.9897703
## 7  0.9846571
## 8  0.9887043
## 9  0.9836142
## 10 0.9825879
```

How ID is set right now, you will get parameter estimates for each individual. May change ID to treatment, experiment, block, etc. based on your data. If you replace it with treatment, you will get the parameters for each treatment. May include more by adding a plus sign between them.

Parameters: y0=initial y value; mumax=intrinsic growth rate; K=asymptotic size

Saturation times: turnpoint=time of turnpoint (50% saturation); sat1=time of minimum of 2nd derivative (minimum growth rate); sat2=time of intercept between steepest increase (tangent of mumax) and K; sat3=time when asymptotic size is reached

This showed how to fit logistic equations, but this package fits lots of different curves!

If you are more interested in defining more complex forumlas and defining their log-liklihood functions, I recommend the package **bblme** and use the function **mle2**
