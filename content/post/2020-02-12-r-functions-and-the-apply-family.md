---
title: R functions and the Apply family
author: cougrstats
date: '2020-02-12'
categories:
  - Introduction to R
tags:
  - apply
  - functions
  - lapply
slug: r-functions-and-the-apply-family
---

_By Vera Pfeiffer_

## Data for today

```r
BadFungi<-read.csv("BadFun.csv", row.names=1)
head(BadFungi)

##               Botrytis Cladosporium  Monilinia
## X10orgedge  0.02131367   0.15160858 0.04504021
## X10orgint   0.02654155   0.09718499 0.03900804
## X11convedge 0.04959786   0.24664879 0.02560322
## X11convint  0.03391421   0.32600536 0.04571046
## X15softedge 0.10442359   0.17694370 0.05201072
## X15softint  0.09195710   0.21796247 0.01300268
##             Mycosphaerella Penicillium
## X10orgedge       0.3230563           0
## X10orgint        0.1786863           0
## X11convedge      0.6823056           0
## X11convint       0.5143432           0
## X15softedge      0.3900804           0
## X15softint       0.4044236           0

Envi<-read.csv("FunEnvi.csv", row.names=1)
head(Envi)

##                   PCNM1       PCNM2 Precip MinT VPDmin
## X10orgedge  -0.11090592 -0.01442449   2.31 37.0   1.15
## X10orgint   -0.11092923 -0.01445247   2.31 37.0   1.15
## X11convedge -0.11065756 -0.01294471   2.31 37.0   1.15
## X11convint  -0.08651768  0.69306694   2.31 37.0   1.15
## X15softedge -0.11087064 -0.03984493   2.18 37.9   1.27
## X15softint  -0.11088600 -0.04012614   2.18 37.9   1.27
##             VPDmax  PropPear PropFruit   PropFor soft org
## X10orgedge   10.20  7.219268 0.1145916 5.7295780    0   1
## X10orgint    10.20  7.219268 0.1145916 5.7295780    0   1
## X11convedge  10.20 66.119330 1.6042818 0.3437747    0   0
## X11convint   10.20 66.119330 1.6042818 0.3437747    0   0
## X15softedge  11.28 14.782311 1.4896903 0.0000000    1   0
## X15softint   11.28 14.782311 1.4896903 0.0000000    1   0
```

## R packages for today

install.packages("CCA"),
install.packages("vegan")

## R functions

Everything that exists in R is an object, and everything that is done (data transformations, plotting, operations) in R is a function.

There are many functions supplied by the base R software package, as well as libraries of code accessible through open access packages available at R Cran repositories.

You can also write your own functions, and activate them by running them in your script. Or alternatively, you can to use source() to load them from a separate file in your working directory.

## Writing functions

Abstracting your code into many small functions is a great way to improve your
organization, comfort, and efficiency in R. You can store your functions in .R
documents and source them from a script if they are long and obscure the flow of your working version of code. Try to avoid making very long or complex functions that do too much at once.

FUNCTION.NAME = function(PARAMETER.LIST) {

BODY

}

A function call proceeds as follows:

  * Execution jumps to the first line of the function upon seeing the call FUNCTION.NAME(ARGUMENT.LIST)

  * Function's PARAMETER.LIST is copied from caller's ARGUMENT.LIST by name or position, and from defaults specified as PARAMETER.NAME=DEFAULT in PARAMETER.LIST

  * Assignment to function parameters and local variables doesn't affect caller's variables

  * Code in function is executed until return(EXPRESSION), or until function's closing }

  * Execution returns to caller; if caller assigned a variable to function it gets EXPRESSION from function's return() or last expression

```r
a=4
b=5
square.a <- function(a = 1, b = 2) {
  b=100
  c=a*a
  return(c)
}
square.a

## function(a = 1, b = 2) {
##   b=100
##   c=a*a
##   return(c)
## }

square.a()

## [1] 1

square.a(a=3)

## [1] 9

square.a(3)

## [1] 9

square.a(3,7)

## [1] 9

a

## [1] 4

b

## [1] 5
```

You don't have to use a return statement...

```r
sum.of.squares <- function(x,y) {
  x^2 +y^2
}

sum.of.squares(5,6)

## [1] 61

x<-c(2:11)
y<-c(3:12)
sum.of.squares(x,y)

##  [1]  13  25  41  61  85 113 145 181 221 265
```

Function goals:

  * short

  * performs one opperation

  * intuitive name

Functions should primarily help you improve the readability of your code, and secondarily improve your efficiency and organization. It also helps you maintain your code by storing it in separate easily accessible files, rather than in super, super, long whole-project document.

Bigger function example

```r
badfungiCC<-CCorA(Envi,BadFungi, stand.X=TRUE,stand.Y=TRUE)
summary(badfungiCC)

##              Length Class  Mode
## Pillai         1    -none- numeric
## Eigenvalues    5    -none- numeric
## CanCorr        5    -none- numeric
## Mat.ranks      2    -none- numeric
## RDA.Rsquares   2    -none- numeric
## RDA.adj.Rsq    2    -none- numeric
## nperm          1    -none- numeric
## p.Pillai       1    -none- numeric
## p.perm         1    -none- logical
## Cy           150    -none- numeric
## Cx           150    -none- numeric
## corr.Y.Cy     55    -none- numeric
## corr.X.Cx     25    -none- numeric
## corr.Y.Cx     55    -none- numeric
## corr.X.Cy     25    -none- numeric
## control       12    how    list
## call           5    -none- call

badfungiCC$CanCorr

## [1] 0.8717640 0.8035587 0.6797292 0.5107511 0.4393814

#0.87 0.80
#Eigenvalues are canonical correlations squared
#Pillai's trace is the sum of squared Canonical correlations
print(sum(badfungiCC$CanCorr^2))

## [1] 2.321634

print(sum(badfungiCC$Eigenvalues))

## [1] 2.321634

print(badfungiCC$Pillai)

## [1] 2.321634

#RDA R squares
print(badfungiCC$RDA.Rsquares)

## [1] 0.1611034 0.4759253

# ...tell you how much variance in the *dependent* variables is explained by the independent *canonical variate* (and vice versa)
# i.e. X|Y = variance in X variables explained by the Y canonical variate
# i.e. Y|X = variance in Y variables explained by the X canonical variate

# IMPORTANT
# corr.Y.Cy = Correlation of each variable in Y with its Canonical variate (similarly, corr.X.Cx)
# Also called Canonical loadings or canonical structure correlations, interpreted as factor loadings
# ...tells you how much do individual variables contribute to their own canonical variates
badfungiCC$corr.Y.Cy

##              CanAxis1    CanAxis2    CanAxis3    CanAxis4
## PCNM1     -0.32081197 -0.33933054 -0.21230081 -0.27697487
## PCNM2      0.20369029  0.14892281 -0.22857132  0.48254574
## Precip    -0.18490434 -0.22563958 -0.08315862 -0.23894850
## MinT       0.03450369  0.15228199  0.23966211  0.26635597
## VPDmin    -0.13952698 -0.21987239  0.03910030  0.14645347
## VPDmax    -0.12043970  0.25484033 -0.05257090 -0.13428438
## PropPear   0.45021330  0.69746308 -0.10002690  0.25950088
## PropFruit  0.20965421  0.37011541  0.14175772  0.33301858
## PropFor   -0.20070175 -0.34619064 -0.19023253 -0.33176122
## soft       0.32626004  0.05835548  0.07913943 -0.59234743
## org       -0.21437285 -0.34322738 -0.06779914 -0.01384469
##              CanAxis5
## PCNM1      0.16866057
## PCNM2      0.12143280
## Precip     0.26614803
## MinT      -0.23270298
## VPDmin     0.13155815
## VPDmax    -0.41006701
## PropPear  -0.05107942
## PropFruit -0.07686641
## PropFor    0.26656009
## soft      -0.28857927
## org        0.15500380

badfungiCC$corr.X.Cx

##                   CanAxis1   CanAxis2    CanAxis3
## Botrytis       -0.58500580 0.49284541 -0.40984921
## Cladosporium   -0.04194937 0.70546350 -0.46226576
## Monilinia       0.66393123 0.18551419  0.44195394
## Mycosphaerella -0.28847351 0.81947263  0.09200482
## Penicillium     0.26637032 0.09997318 -0.14498754
##                  CanAxis4    CanAxis5
## Botrytis       -0.4107330  0.27963134
## Cladosporium    0.4506787  0.28941422
## Monilinia      -0.4621564  0.34039386
## Mycosphaerella  0.4837810  0.05233234
## Penicillium    -0.2441335 -0.91565805

# So the Canonical axis 1 correlation is driven by the high influence of the first spatial distance vector and the proportion of pear in the surrounding area - on Botrytis and Monilinia

# The second Canonical axis 2 correlation shows an even stronger influence of the proportion of pear, as well as more distributed effects of the proportion of fruit, the first spatial vector, organic management and precipitation on Cladosporium and Mycosphaerella

# ...NOT THAT INFORMATIVE
# corr.Y.Cx = Correlation of each variable in Y with each Canonical variate in X (similarly corr.X.Cy)
# Also called canonical cross-loading. Correlation of each variabel with the opposite canonical variate
# ...tells you how strongly are individual variables correlated with the canonical variates of the dependent/independent set

badfungiCC$corr.Y.Cx

##              CanAxis1    CanAxis2    CanAxis3     CanAxis4
## PCNM1     -0.27967234 -0.27267200 -0.14430705 -0.141465227
## PCNM2      0.17756987  0.11966822 -0.15536659  0.246460778
## Precip    -0.16119295 -0.18131464 -0.05652534 -0.122043214
## MinT       0.03007908  0.12236752  0.16290533  0.136041613
## VPDmin    -0.12163460 -0.17668037  0.02657761  0.074801276
## VPDmax    -0.10499500  0.20477916 -0.03573398 -0.068585896
## PropPear   0.39247977  0.56045251 -0.06799120  0.132540364
## PropFruit  0.18276900  0.29740945  0.09635686  0.170089613
## PropFor   -0.17496457 -0.27818449 -0.12930660 -0.169447413
## soft       0.28442177  0.04689206  0.05379338 -0.302542112
## org       -0.18688254 -0.27580334 -0.04608505 -0.007071191
##              CanAxis5
## PCNM1      0.07410631
## PCNM2      0.05335531
## Precip     0.11694049
## MinT      -0.10224536
## VPDmin     0.05780420
## VPDmax    -0.18017580
## PropPear  -0.02244335
## PropFruit -0.03377367
## PropFor    0.11712154
## soft      -0.12679636
## org        0.06810578

badfungiCC$corr.X.Cy

##                   CanAxis1   CanAxis2    CanAxis3
## Botrytis       -0.50998702 0.39603021 -0.27858646
## Cladosporium   -0.03656995 0.56688132 -0.31421552
## Monilinia       0.57879137 0.14907154  0.30040898
## Mycosphaerella -0.25148083 0.65849435  0.06253836
## Penicillium     0.23221207 0.08033432 -0.09855226
##                  CanAxis4    CanAxis5
## Botrytis       -0.2097823  0.12286480
## Cladosporium    0.2301846  0.12716321
## Monilinia      -0.2360469  0.14956272
## Mycosphaerella  0.2470917  0.02299386
## Penicillium    -0.1246915 -0.40232309

biplot(badfungiCC)
```

Effect sizes and significant canonical variates for **Bad Fungi**

```r
badfungiCCA<-cc(Envi,BadFungi)
#Effect sizes
badfungiCCA$ycoef

##                      [,1]      [,2]       [,3]      [,4]
## Botrytis       -22.438664 11.750585  -8.474913 32.178310
## Cladosporium    12.718896  2.526191 -17.735366 -6.120606
## Monilinia        2.291911  1.647968   1.267286  1.787275
## Mycosphaerella  -3.954103  4.631983   7.749042 -1.847856
## Penicillium      1.862247  2.207945  -1.680171  1.763883
##                     [,5]
## Botrytis        4.676756
## Cladosporium    5.152196
## Monilinia       1.122518
## Mycosphaerella -2.364223
## Penicillium    -5.048976

badfungiCCA$xcoef

##                   [,1]         [,2]         [,3]
## PCNM1      20.20318698 -30.87925582  -3.54177300
## PCNM2       1.22514085  -0.68045395  -2.74271617
## Precip    -30.26201821  40.71110573  24.93730815
## MinT        1.26711128  -2.85800379   4.65692142
## VPDmin    -25.44970665  30.85066149 -11.54735182
## VPDmax     -5.64031688   6.12719196  -1.63367262
## PropPear   -0.01383938   0.07172806  -0.02568558
## PropFruit   0.87891684  -0.85420311   0.48111233
## PropFor     0.02406463  -0.04232783  -0.05020187
## soft        2.06630668  -0.45726184   0.57663036
## org         0.56344937   0.21743181   0.63884373
##                    [,4]         [,5]
## PCNM1     -16.952541694 -53.60023442
## PCNM2      -1.837648383   2.73584459
## Precip     19.380736253  38.64802445
## MinT       -3.515535279  -9.39025411
## VPDmin     18.076110329  38.23013274
## VPDmax      3.280948570   6.08024432
## PropPear    0.001137222  -0.06726919
## PropFruit   0.006018099   0.43610758
## PropFor     0.005374205   0.12673231
## soft        1.806271076  -1.39622883
## org         0.126172135  -2.55539272
```

FIND WHICH CANONICAL DIMENSIONS ARE SIGNIFICANT

```r
ev=(1 - badfungiCCA$cor^2)
n=dim(Envi)[1]
p=length(Envi)
q=length(BadFungi)
k=min(p, q)
m=n - 3/2 - (p + q)/2
w=rev(cumprod(rev(ev)))
# initialize
d1=d2=f=vector("numeric", k)
for (i in 1:k) {
  s=sqrt((p^2 * q^2 - 4)/(p^2 + q^2 - 5))
  si=1/s
  d1[i]=p * q
  d2[i]=m * s - p * q/2 + 1
  r=(1 - w[i]^si)/w[i]^si
  f[i]=r * d2[i]/d1[i]
  p=p - 1
  q=q - 1
}
pv=pf(f, d1, d2, lower.tail = FALSE)
dmat=cbind(WilksL = w, F = f, df1 = d1, df2 = d2, p = pv)

print(dmat)

##          WilksL         F df1      df2          p
## [1,] 0.02728644 1.4637894  55 68.38983 0.06724978
## [2,] 0.11368049 1.1369873  40 58.73361 0.32254775
## [3,] 0.32086535 0.8348354  27 47.37057 0.68786933
## [4,] 0.59643919 0.6265401  16 34.00000 0.83991561
## [5,] 0.80694401 0.6151972   7 18.00000 0.73655072
```

As a function...

```r
TestSignificance <- function(veganCCA,x,y) {

ev=(1 - veganCCA$cor^2)
n=dim(x)[1]
p=length(x)
q=length(y)
k=min(p, q)
m=n - 3/2 - (p + q)/2
w=rev(cumprod(rev(ev)))
# initialize
d1=d2=f=vector("numeric", k)
for (i in 1:k) {
  s=sqrt((p^2 * q^2 - 4)/(p^2 + q^2 - 5))
  si=1/s
  d1[i]=p * q
  d2[i]=m * s - p * q/2 + 1
  r=(1 - w[i]^si)/w[i]^si
  f[i]=r * d2[i]/d1[i]
  p=p - 1
  q=q - 1
}
pv=pf(f, d1, d2, lower.tail = FALSE)
dmat=cbind(WilksL = w, F = f, df1 = d1, df2 = d2, p = pv)

print(dmat)

}

TestSignificance(badfungiCCA, Envi, BadFungi)

##          WilksL         F df1      df2          p
## [1,] 0.02728644 1.4637894  55 68.38983 0.06724978
## [2,] 0.11368049 1.1369873  40 58.73361 0.32254775
## [3,] 0.32086535 0.8348354  27 47.37057 0.68786933
## [4,] 0.59643919 0.6265401  16 34.00000 0.83991561
## [5,] 0.80694401 0.6151972   7 18.00000 0.73655072
```

## Apply function family

Apply functions are implicit loops that iterate over the elements in an object like a dataframe, list, matrix, or array (3-d matrix) and execute some set of functions.

Apply functions are a more efficient way to write a loop - which can help to keep your code organized and efficient. They are also more computationally efficient.

Depending on your inputs and outputs - there is a whole family of apply functions. The first four apply a function over all the elements in a single object.

`lapply(X, FUN, ...)` list apply; returns a list of values obtatined by applying a function to a vector, list, or data frame.

```r
lapply(Envi$Precip, sqrt)

## [[1]]
## [1] 1.519868
##
## [[2]]
## [1] 1.519868
##
## [[3]]
## [1] 1.519868
##
## [[4]]
## [1] 1.519868
##
## [[5]]
## [1] 1.476482
##
## [[6]]
## [1] 1.476482
##
## [[7]]
## [1] 1.476482
##
## [[8]]
## [1] 1.476482
##
## [[9]]
## [1] 1.486607
##
## [[10]]
## [1] 1.486607
##
## [[11]]
## [1] 1.486607
##
## [[12]]
## [1] 1.486607
##
## [[13]]
## [1] 1.593738
##
## [[14]]
## [1] 1.593738
##
## [[15]]
## [1] 1.593738
##
## [[16]]
## [1] 1.593738
##
## [[17]]
## [1] 1.593738
##
## [[18]]
## [1] 1.593738
##
## [[19]]
## [1] 1.479865
##
## [[20]]
## [1] 1.479865
##
## [[21]]
## [1] 1.479865
##
## [[22]]
## [1] 1.479865
##
## [[23]]
## [1] 1.519868
##
## [[24]]
## [1] 1.519868
##
## [[25]]
## [1] 1.584298
##
## [[26]]
## [1] 1.584298
##
## [[27]]
## [1] 1.486607
##
## [[28]]
## [1] 1.486607
##
## [[29]]
## [1] 1.486607
##
## [[30]]
## [1] 1.486607
```

`sapply(X, FUN, ...)` Like lapply, but simplifies the output to the more simple data type... may return a vector instead of a list.

```r
sapply(Envi$Precip, sqrt)

##  [1] 1.519868 1.519868 1.519868 1.519868 1.476482 1.476482
##  [7] 1.476482 1.476482 1.486607 1.486607 1.486607 1.486607
## [13] 1.593738 1.593738 1.593738 1.593738 1.593738 1.593738
## [19] 1.479865 1.479865 1.479865 1.479865 1.519868 1.519868
## [25] 1.584298 1.584298 1.486607 1.486607 1.486607 1.486607
```

`apply(X, MARGIN, FUN, ...)` returns a vector or array or list of values obtatined by applying a function to margins (1 = rows, 2 = columns) of a data frame, matrix or array.

```r
apply(Envi, MARGIN=2, mean)

##         PCNM1         PCNM2        Precip          MinT
## -5.086263e-18 -6.604124e-17  2.309333e+00  3.710000e+01
##        VPDmin        VPDmax      PropPear     PropFruit
##  1.216000e+00  1.051000e+01  2.711236e+01  1.443854e+00
##       PropFor          soft           org
##  9.862514e+00  3.333333e-01  3.333333e-01
```

`tapply(X, INDEX, FUN = NULL)` Table apply, this apply statement requires an index values (object of the same length as X), and allows you to apply a function to a subset of your data.

```r
tapply(Envi$MinT, Envi$Precip, mean)

## 2.18 2.19 2.21 2.31 2.51 2.54
## 37.9 37.9 37.3 37.0 35.8 36.3
```

... and...

The multiple arguments apply function allows you to apply a function across multiple objects... takes several vectors, and applies the function to the first object of each, then the second object of each... can be different lengths

`mapply(FUN, ...)` returns a vector or array or list of values obtatined by applying a function to margins of a matrix or array.

```r
x= 1:4
y= 5:8
z= 9:12
mapply(sum, x, y, z)

## [1] 15 18 21 24
```

`MAP(FUN, ...)` is apparently similar and often preferable version, that does not simplify data structures or break lazy argument loading norms.
