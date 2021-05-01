---
title: Clustering in R
author: Enrique Jimenez
date: '2019-10-02'
categories:
  - Research Profiles
tags:
  - clustering
slug: clustering-in-r
---

_By Enrique Jimenez_

```r
library(ggplot2)

## Warning: package 'ggplot2' was built under R version 3.5.3

library(ggpubr)

## Warning: package 'ggpubr' was built under R version 3.5.3

library(cluster)

## Warning: package 'cluster' was built under R version 3.5.3

library(factoextra)

## Warning: package 'factoextra' was built under R version 3.5.3

library(NbClust)

## Warning: package 'NbClust' was built under R version 3.5.2

library(tidyLPA)

## Warning: package 'tidyLPA' was built under R version 3.5.3
```

## What is clustering?

**Clustering** or **cluster analysis** is the task of dividing a data set into groups of similar individuals. When clustering we generally want our groups to be similar within (individuals within a group are as similar as possible) and different between (the individuals from different groups are as different as possible).

## k-means Clustering

_k_-means clustering is one of the simplest and most commonly used clustering algorithms. It works by iteratively assigning individuals to one of _k_ centroids (means) and recalibrating the locations of the menas based on the groups created.

### k-means example

We will use the classic Fisher's iris dataset mostly because Fisher was cool. However, for simplicity, we will use only the petal measurements.

```r
  data("iris")
  petals_kmeans<-iris[,3:5]
  head(petals_kmeans)

##   Petal.Length Petal.Width Species
## 1          1.4         0.2  setosa
## 2          1.4         0.2  setosa
## 3          1.3         0.2  setosa
## 4          1.5         0.2  setosa
## 5          1.4         0.2  setosa
## 6          1.7         0.4  setosa

  set.seed(23)
  petals_kmeans_3<-kmeans(iris[,3:4], centers = 3)
  petals_kmeans$k3<-petals_kmeans_3$cluster
  head(petals_kmeans)

##   Petal.Length Petal.Width Species k3
## 1          1.4         0.2  setosa  3
## 2          1.4         0.2  setosa  3
## 3          1.3         0.2  setosa  3
## 4          1.5         0.2  setosa  3
## 5          1.4         0.2  setosa  3
## 6          1.7         0.4  setosa  3

  iris_plot_k3<-ggplot(petals_kmeans) +
  geom_point(aes(x=Petal.Length, y=Petal.Width, colour=as.factor(k3)), data=petals_kmeans) +
  theme_bw() +
  theme(panel.grid = element_blank()) +
  scale_color_viridis_d() +
  ggtitle("Iris petal data k=3") +
  labs(colour="Cluster")

  iris_plot_k3
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_1.png)

```r
  set.seed(23)
  petals_kmeans_4<-kmeans(iris[,3:4], centers = 4)
  petals_kmeans$k4<-petals_kmeans_4$cluster

  iris_plot_k4<-ggplot(petals_kmeans) +
  geom_point(aes(x=Petal.Length, y=Petal.Width, colour=as.factor(k4)), data=petals_kmeans) +
  theme_bw() +
  theme(panel.grid = element_blank()) +
  scale_color_viridis_d() +
  ggtitle("Iris petal data k=4") +
  labs(colour = "Cluster")

  iris_plot_k4
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_2.png)

```r
  iris_plot_species<-ggplot(petals_kmeans) +
  geom_point(aes(x=Petal.Length, y=Petal.Width, colour=as.factor(Species)), data=petals_kmeans) +
  theme_bw() +
  theme(panel.grid = element_blank()) +
  scale_color_viridis_d() +
  ggtitle("Iris petal data colored by species") +
  labs(colour = "Species")

  iris_plot_species
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_3.png)

```r
  final_figure <- ggarrange(plotlist = list(iris_plot_k3, iris_plot_k4, iris_plot_species),
          common.legend = TRUE,
          legend = "right")
  final_figure
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_4.png)

## Other simple clustering algorithms
  * **K-medoids algorithm** or **PAM**
  * **Heirarchical clustering**

## Model evaluation

One of the difficulties in using k-means clustering and other similar clustering algorithms is selecting the number of clusters.

### Determining the number of clusters

There are a large number of measurements that help determine the ideal number of clusters into which a set of data should be split. `NbClust` provides a function to leverage this field of indices.

```r
nb<-NbClust(iris[3:4], distance = 'euclidean', min.nc = 2, max.nc = 9, method = "complete", index= "all",)

  fviz_nbclust(nb) + theme_minimal()

## Among all indices:
## ===================
## * 2 proposed  0 as the best number of clusters
## * 1 proposed  1 as the best number of clusters
## * 1 proposed  2 as the best number of clusters
## * 15 proposed  3 as the best number of clusters
## * 1 proposed  4 as the best number of clusters
## * 3 proposed  6 as the best number of clusters
## * 1 proposed  7 as the best number of clusters
## * 2 proposed  9 as the best number of clusters
##
## Conclusion
## =========================
## * According to the majority rule, the best number of clusters is  3 .
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_5.png)

### Silhouette Coefficient

The Silhouette Coefficient uses the distances between individuals in the same cluster and their average distance to every individual in the nearest class to evalueate a clustering run. The larger the number, the better the clustering.

```r
  sil_k3<-silhouette(petals_kmeans_3$cluster, dist(petals_kmeans[1:2]))
  sil_k4<-silhouette(petals_kmeans_4$cluster, dist(petals_kmeans[1:2]))
  sil_plot_k3<-fviz_silhouette(sil_k3, print.summary = FALSE) +
    scale_color_viridis_d()
  sil_plot_k4<-fviz_silhouette(sil_k4, print.summary = FALSE) +
    scale_color_viridis_d()
  ggarrange(plotlist = list(sil_plot_k3, sil_plot_k4),
          common.legend = FALSE,
          legend = FALSE)
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_6.png)

### Other clustering evaluation methods
  * **Calinski-Harabasz Index**
  * **Davies-Bouldin Index**
  * **Dunn Index**

## Model based clustering

An alternative to the traditional clustering methods is **model based clustering**, which allows for the use of likelihood-based evaluation of the models.

### Latent Profile Analysis

**Latent Profile Analysis** (LPA) is one version of what are called _latent variable models_. Broadly speaking latent variable models are ones where an unobserved (or latent) variable is modeled from observed or manifest variables. LPA is the latent variable model that plays the function of a cluster analysis. In the case of LPA, the latent variable is categorical, representing the classes or clusters in which the data is binned and the observed variables are continuous. Therefore, LPA acts as a clustering model for continuous observed variables. Within the framework of latent variable models there is also a clustering model for categorical observed variables: **Latent class analysis**.

Here we'll use `library(tidyLPA)` to run an LPA on the petal data.

```r
  LPA_1.5<-estimate_profiles(petals_kmeans[,1:2], 1:7)

## Warning:
## One or more analyses resulted in warnings! Examine these analyses carefully: model_1_class_7

  LPA_1.5

## tidyLPA analysis using mclust:
##
##  Model Classes AIC    BIC    Entropy prob_min prob_max n_min n_max BLRT_p
##  1     1       946.40 958.45 1.00    1.00     1.00     1.00  1.00
##  1     2       623.59 644.67 0.98    0.99     1.00     0.33  0.67  0.01
##  1     3       439.46 469.56 0.96    0.97     1.00     0.32  0.35  0.01
##  1     4       399.78 438.92 0.92    0.89     1.00     0.18  0.33  0.01
##  1     5       385.14 433.31 0.93    0.88     1.00     0.05  0.33  0.01
##  1     6       338.55 395.76 0.95    0.90     1.00     0.05  0.33  0.01
##  1     7       343.97 410.20 0.94    0.46     0.99     0.01  0.33  0.57

  ggplot(get_data(LPA_1.5)[which(get_data(LPA_1.5)$classes_number==3),]) +
    geom_point(aes(x = Petal.Length, y=Petal.Width, colour=as.factor(Class))) +
    theme_bw() +
    theme(panel.grid = element_blank()) +
    scale_color_viridis_d() +
    ggtitle("Iris petal data LPA 5") +
    labs(colour = "Class")
```

![](https://cougrstats.files.wordpress.com/2019/10/cluster_7.png)

One thing to keep in mind is that, as a model-based method, LPA is tied to a series of assumptions. One of these assumptions refers to the structure of the covariance matrix of the observed variables, which can drastically affect the fit of LPA models.
