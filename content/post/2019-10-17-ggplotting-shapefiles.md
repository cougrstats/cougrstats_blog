---
title: ggplotting shapefiles
author: Carly Prior
date: '2019-10-17'
tags:
  - ggplot2
  - mapping
  - shapefiles
slug: ggplotting-shapefiles
---

_By Carly Prior_

### Load these libraries

```r
library(ggplot2)
library(maptools)
library(maps)
library(rgdal)
library(sp)
library(raster)
library(plyr)
library(dplyr)
library(knitr)
library(tidyverse)
```

## What is a shapefile?

A shapefile is a specific format for geospatial vector data describing points, lines or polygons. Shapefiles are most often used in GIS software like ArcGIS, but today we'll be using them in R as polygon layers on a ggplot map.

### Load the shapefile with raster::shapefile

This shapefile is for the Laurentide Ice Sheet, which covered large portions of North America 18 thousand years ago during the Last Glacial Maximum.

```r
# Note that while we are only loading the .shp file the .dbf, .shx, .sbn, .sbx, and .prj files all must be in the same folder as the .shp file to use the shapefile (more info in link below)
shapeLGM <- shapefile("LGM/ice18k_ICE.shp")

#Exploring the class of our shapefile (link below for further info)
class(shapeLGM)

## [1] "SpatialPolygonsDataFrame"
## attr(,"package")
## [1] "sp"

#Exploring the shapefile's coordinate reference system (crs)
crs(shapeLGM)

## CRS arguments:
##  +proj=lcc +lat_1=49 +lat_2=77 +lat_0=49 +lon_0=-95 +x_0=0 +y_0=0
## +ellps=clrk66 +units=m +no_defs
```

_Note that this initial shape file has the Lambert conformal conic (lcc) projection_

### Load some basic maps with ggplot2::map_data

```r
world <- map_data("world")
kable(head(world))
```

<table >

<tr >
long
lat
group
order
region
subregion
</tr>

<tbody >
<tr >

<td align="right" >-69.89912
</td>

<td align="right" >12.45200
</td>

<td align="right" >1
</td>

<td align="right" >1
</td>

<td align="left" >Aruba
</td>

<td align="left" >NA
</td>
</tr>
<tr >

<td align="right" >-69.89571
</td>

<td align="right" >12.42300
</td>

<td align="right" >1
</td>

<td align="right" >2
</td>

<td align="left" >Aruba
</td>

<td align="left" >NA
</td>
</tr>
<tr >

<td align="right" >-69.94219
</td>

<td align="right" >12.43853
</td>

<td align="right" >1
</td>

<td align="right" >3
</td>

<td align="left" >Aruba
</td>

<td align="left" >NA
</td>
</tr>
<tr >

<td align="right" >-70.00415
</td>

<td align="right" >12.50049
</td>

<td align="right" >1
</td>

<td align="right" >4
</td>

<td align="left" >Aruba
</td>

<td align="left" >NA
</td>
</tr>
<tr >

<td align="right" >-70.06612
</td>

<td align="right" >12.54697
</td>

<td align="right" >1
</td>

<td align="right" >5
</td>

<td align="left" >Aruba
</td>

<td align="left" >NA
</td>
</tr>
<tr >

<td align="right" >-70.05088
</td>

<td align="right" >12.59707
</td>

<td align="right" >1
</td>

<td align="right" >6
</td>

<td align="left" >Aruba
</td>

<td align="left" >NA
</td>
</tr>
</tbody>
</table>

```r
states <- map_data("state") # We'll use this one later

# Let's make a quick world map:
ggplot() +
  geom_polygon(data = world, aes(x = long, y = lat, group = group), fill = NA, color = "black", size = 0.25) +
  coord_fixed(1.3) +
  NULL
```

![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_1.png)

## Now let's prepare our shapefile and plot it on the map

```r
#Just for the example's sake we'll change the name of the file
testLGM <- shapeLGM

#explicitly set the id so that later we can collapse the SpatialPolygonsDataFrame into a regular DataFrame
testLGM@data$id <- rownames(testLGM@data)

#collapse to a regular DataFrame
testLGM.points <- fortify(testLGM, region = "id")

#Matches ids and joins the two dataframes in those spaces (explicit join)
testLGM.df <- join(testLGM.points, testLGM@data, by="id")

# Let's map it!
ggplot() +
   geom_polygon(data = testLGM.df, aes(x = long, y = lat, group = group), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```

![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_2.png)

Well, that's not quite what we're looking for. This is because the shapefile has the lcc projection, and most of us are used to a rectangular projection, so let's change that and then use it as a layer over a map.

_Note, you could also make a map with this specific projection!_

```r
#explicitly set the id so that later we can collapse the SpatialPolygonsDataFrame into a regular DataFrame
shapeLGM@data$id <- rownames(shapeLGM@data)

#change the coordinate reference system to longlat projection using WGS84
shapeLGM.proj <- spTransform(shapeLGM, CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"))

#collapse to a regular DataFrame
lgmPoints <- fortify(shapeLGM.proj, region = "id")

#Matches ids and joins the two dataframes in those spaces (explicit join)
lgm.df <- merge(lgmPoints, shapeLGM@data, by = "id")

# Let's make a map!
ggplot() +
  geom_polygon(data = world, aes(x = long, y = lat, group = group), fill = NA, color = "black", size = 0.25) +
   geom_polygon(data = lgm.df, aes(x = long, y = lat, group = group), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```

![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_3.png)

Wow! What a map. But maybe we really care about the area specifically affected by this particular ice sheet.
```r
ggplot() +
  geom_polygon(data = subset(world, long > -180 & long  30), aes(x = long, y = lat, group = group), fill = NA, color = "black", size = 0.25) +
  geom_polygon(data = lgm.df, aes(x = long, y = lat, group = group), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```
![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_4.png)

Super cool! Now, I specifically learned these methods to produce maps that show how the ice sheet encroached on an eastern North American species' extant geographic range, implying a historical range contraction as the ice sheets expanded and subsequently a historical range expansion as the ice sheets shrank.

```r
#Let's look at the ice sheet over a very specific area in the United States
ggplot() +
  geom_polygon(data = subset(states, long > -100 & long < -75), aes(x = long, y = lat, group = group), fill = NA, color = "black", size = 0.25) +
   geom_polygon(data = lgm.df, aes(x = long, y = lat, group = group), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```

![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_5.png)

Yikes.

```r
# Let's try again and reduce the size of the shape file like we did with the states object
ggplot() +
  geom_polygon(data = subset(states, long > -100 & long  -100 & long < -75), aes(x = long, y = lat, group = group), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```

![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_6.png)

OK, still not great but let's subset on the latitude as well.

```r
ggplot() +
  geom_polygon(data = subset(states, long > -100 & long  -100 & long < -75 & lat < 50), aes(x = long, y = lat, group = group), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```

![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_7.png)

Much worse. Why?

Well our polygon has no defined edge at 50N, so there is no way to properly display what we asked for.

Let's fix that!
```r
# We can reduce the dataframe to just longitude and latitude
lgmpoly <- lgm.df[,2:3]

# Then subset that polygon to the desired area
lgmpoly.1  -100 & long < -75 & lat < 50)

# Finally, serially add points along the latitude = 50 line
for (i in -100:-75){
  lgmpoly.1[nrow(lgmpoly.1) + 1,]  -100 & long < -75), aes(x = long, y = lat, group = group), fill = NA, color = "black", size = 0.25) +
    geom_polygon(data = lgmpoly.1, aes(x = long, y = lat), fill = "deepskyblue2", alpha = 0.2) +
  coord_fixed(1.3) +
  NULL
```
![](https://cougrstats.files.wordpress.com/2019/10/shapefiles_8.png)

A thing of beauty! On top of this map you can easily apply other points, lines and polygons!

#### Below are links to several tutorials that I referenced when teaching myself this topic!
  * [Tutorial specific to ggplot](https://github.com/tidyverse/ggplot2/wiki/plotting-polygon-shapefiles)
  * [General map making tutorial](https://eriqande.github.io/rep-res-web/lectures/making-maps-with-R.html)
  * [Documentation for the maps::map function](https://www.rdocumentation.org/packages/maps/versions/2.0-10/topics/map)
  * [Documentation for SpatialPolygonsDataFrame](https://www.rdocumentation.org/packages/sp/versions/1.3-1/topics/SpatialPolygonsDataFrame-class)
  * [Documentation on shapefiles and their associated files](https://en.wikipedia.org/wiki/Shapefile)
