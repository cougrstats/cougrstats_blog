---
title: Mapping in R
author: cougrstats
date: '2018-04-30'
categories:
  - Package Introductions
tags:
  - cowplot
  - grid
  - mapping
  - mapview
  - sf
  - spatial data
  - spData
  - spDataLarge
  - tidyverse
  - tmap
slug: mapping-in-r
---

_Post by Dominik Schneider_

A couple things to note. Spatial/gis functions in R are undergoing a massive change right now. The old stalwart `sp` has been succeeded by `sf` (simple features), which is compatible with the open geospatial consortium standards. When you are looking for solutions online, make sure you know which data type is being used- they are not interchangeable. You can convert from `sf` to `sp` with `as(x,'Spatial')` and vice versa with `st_as_sf()`. Stick with `sf` whenever possible, it is the future. `sf` is designed to be more consistent in syntax, tidy, and feature rich (it does everything `rgdal`, `rgeos`, and `sp` do/did).

`sf` is specific to vector data (points, lines, polygons). Gridded raster data is still served by `raster`. Unfortunately, thye are not really compatible so if you need to mix them, you will need to convert your `sf` objects to `sp` objects. This should mostly only be the case for analysis because there are mapping packages that handle both. Keep your eye on `star` as an upcoming successor of the `raster` package.

If you do need to mix vector and raster data, I think it's still worth doing any vector operations with `sf` and then convert to `sp` at the end. I believe many of the `sf` tools are written in c++ to be as efficient as possible. For polygon/raster conversions, check out [fasterize](https://cran.r-project.org/web/packages/fasterize/) and [spex](https://mdsumner.github.io/spex/index.html) for more efficient implementations that work with `sf`. I often just convert my raster and vector data to tibbles and use the tidyverse tools to do the processing.

If there is one resource you should read, it's the new [Geocomputation with R](https://geocompr.robinlovelace.net) book that is being written. Basic spatial methods are described in part 1 and I will assume some knowledge of that material. I am going to cover mapping from [part 2](https://geocompr.robinlovelace.net/adv-map.html).

They recommend `tmap` because it can handle `sp`, `sf`, and `raster` objects. You will see it's quite powerful. I encourage you to read the vignettes.

# load libraries

```r
# these packages can be installed from cran
require(sf) # the spatial workhorse

## Loading required package: sf

## Warning: package 'sf' was built under R version 3.4.4

## Linking to GEOS 3.6.1, GDAL 2.2.3, proj.4 4.9.3

library(spData) #example spatial data

## Warning: package 'spData' was built under R version 3.4.4

library(tidyverse) # for general data wrangling

## -- Attaching packages ---------------------------------- tidyverse 1.2.1 --

## v ggplot2 2.2.1.9000     v purrr   0.2.4
## v tibble  1.4.2          v dplyr   0.7.4
## v tidyr   0.8.0          v stringr 1.3.0
## v readr   1.1.1          v forcats 0.3.0

## Warning: package 'tidyr' was built under R version 3.4.4

## Warning: package 'stringr' was built under R version 3.4.4

## Warning: package 'forcats' was built under R version 3.4.4

## -- Conflicts ------------------------------------- tidyverse_conflicts() --
## x dplyr::filter() masks stats::filter()
## x dplyr::lag()    masks stats::lag()

library(tmap)    # for static and interactive maps
library(mapview) # for interactive maps

## Warning: package 'mapview' was built under R version 3.4.4

library(grid) # for putting multiple plot on top of each other
library(cowplot) # for arranging multiple ggplots

##
## Attaching package: 'cowplot'

## The following object is masked from 'package:ggplot2':
##
##     ggsave

# install with install.packages("spDataLarge", repos = "https://nowosad.github.io/drat/", type = "source")
library(spDataLarge) # more example spatial data
```

# the data

I will use the new zealand example dataset from `spData`, but if you need to read in your own GIS data you can use the built in functions from `sf::read_sf()` for vector data and `raster::raster()` for raster data.

If you have a csv file with coordinates for points try this general approach:

    csvdata <- readr::read_csv(file=<your_filename>)
    sfdata <- sf::st_as_sf(csvdata,
                           coords = c('xcoords','ycoords'),
                           crs = <a_proj4_projection_string>)

Example datasets in spData include `nz`. It is a multipolygon simple feature collection of New Zealand.

```r
spData::nz

## Simple feature collection with 16 features and 6 fields
## geometry type:  MULTIPOLYGON
## dimension:      XY
## bbox:           xmin: 1090144 ymin: 4748537 xmax: 2089533 ymax: 6191874
## epsg (SRID):    2193
## proj4string:    +proj=tmerc +lat_0=0 +lon_0=173 +k=0.9996 +x_0=1600000 +y_0=10000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
## First 10 features:
##    REGC2017            REGC2017_NAME AREA_SQ_KM LAND_AREA_SQ_KM
## 1        01         Northland Region  12512.749       12500.320
## 2        02          Auckland Region   4942.693        4941.622
## 3        03           Waikato Region  24578.246       23899.899
## 4        04     Bay of Plenty Region  12280.444       12070.497
## 5        05          Gisborne Region   8385.816        8385.816
## 6        06       Hawke's Bay Region  14191.302       14137.210
## 7        07          Taranaki Region   7254.357        7254.357
## 8        08 Manawatu-Wanganui Region  22220.590       22220.590
## 9        09        Wellington Region   8119.553        8048.661
## 10       12        West Coast Region  23319.648       23243.812
##    Shape_Length  Shape_Area                       geometry
## 1     3321236.6 12512734660 MULTIPOLYGON (((1745493 600...
## 2     2878758.5  4942685973 MULTIPOLYGON (((1793982 593...
## 3     2177078.9 24578239227 MULTIPOLYGON (((1860345 585...
## 4     1400381.0 12280442951 MULTIPOLYGON (((2049387 583...
## 5      689546.8  8385816413 MULTIPOLYGON (((2024489 567...
## 6      948804.8 14191296978 MULTIPOLYGON (((2024489 567...
## 7      533923.9  7254385835 MULTIPOLYGON (((1740438 571...
## 8     1118235.5 22220599731 MULTIPOLYGON (((1866732 566...
## 9      679244.2  8119550321 MULTIPOLYGON (((1881590 548...
## 10    1723903.1 23319649647 MULTIPOLYGON (((1557042 531...
```

# simple examples

The basic `tmap` syntax includes a spatial object in `tm_shape` plus a layer that you choose based on the geometry you are trying to plot. You can add multiple layers for a given object.

```r
tm_shape(nz) + tm_fill()
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-4-13.png)

```r
# Add border layer to nz shape
tm_shape(nz) + tm_borders()
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-4-23.png)

```r
# Add fill and border layers to nz shape
tm_shape(nz) + tm_fill() + tm_borders()
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-4-33.png)

`tmap` uses the "grammar of graphics" similar to `ggplot`. You can create maps by adding layers on top of each other.

```r
map_nz = tm_shape(nz) + tm_polygons() #tm_polygons is the equivalent to tm_fill+tm_borders

map_nz + # note that you can store maps as objects
  tm_shape(nz_elev) + tm_raster(alpha = 0.7)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-5-12.png)

# Data-defined plotting

It's also simple to color your features by a variable.

```r
tm_shape(nz)+tm_fill(col='REGC2017_NAME')
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-6-13.png)

Want to change the colors? check out the nifty `tmaptools::palette_explorer()`

```r
tm_shape(nz)+tm_fill(col='REGC2017_NAME', palette='Set1')
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-8-13.png)

You can use `tm_layout` to adjust layout options, like margins. Here is an example where I made more space for the legend.

```r
tm_shape(nz)+
  tm_fill(col='REGC2017_NAME',
          palette='Set1',
          title='Regions of New Zealand')+
  tm_layout(frame.lwd = 5,
            legend.just = c(0,1),
            legend.position = c(0.01,1),
            inner.margins = c(.02,.15,0.02,.1),
            legend.width = 0.5)+
  tm_style_beaver()
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-9-13.png)

# Facetting based on data categories

If you have data, for example for different months or years, you could plot them simulataneously with a shared legend.

```r
# make a random category
nz$let=sample(letters[1:2],nrow(nz),replace=T)

# here is a silly map based on randomly assigned 'a' or 'b'
tm_shape(nz)+
  tm_fill(col='REGC2017_NAME', palette='Set1')+
  tm_facets(by='let')
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-10-13.png)

# Arrange different types of plots next to each other

If you have two (or more) maps you would like side by side that you can't split based on an attribute you might find it useful to use `tmap_arrange`. You can also easily add a north arrow and scalebar.

```r
tmap_arrange(map_nz + tm_compass() + tm_scale_bar() ,
             tm_shape(nz_elev) + tm_raster(alpha = 0.7),
             ncol=2)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-11-12.png)

# inset maps

```r
# compute the bounding box for the auckland region
auckland_box <- st_bbox(nz %>% filter(REGC2017_NAME=='Auckland Region')) %>%
  st_as_sfc()

## Warning: package 'bindrcpp' was built under R version 3.4.4

# create a map of elevation for the subset we want to blow up
auckland_elev <-
  tm_shape(spDataLarge::nz_elev,
           ylim=c(5871375, 6007878),
           xlim=c(1704673,1828993))+
  tm_raster(style = "cont", palette='-YlOrBr',#minus sign for the palette reverses the colors
            auto.palette.mapping = FALSE, legend.show = TRUE)+
  tm_legend(legend.just=c(0,0),
            legend.position=c(0,0))
auckland_elev
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-12-13.png)

```r
# make the overview map tha tincludes a box outlining our subset we are highlighting
bigmap <- map_nz +
  tm_shape(auckland_box) +  #here we are adding the little inset box on the overview map
  tm_borders(lwd = 3)
bigmap
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-12-23.png)

```r
# make a viewport. think of this as a window in the bigmap through whcih we can see the elevation inset
auckland_vp <- grid::viewport(0.3, 0.7, width = 0.4, height = 0.4)

#make sure you run these next lines all at once to see the result!
bigmap
print(auckland_elev, vp = auckland_vp)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-12-32.png)

```r
# save your map using standard graphic functions - pdf()...dev.off() or save_tmap()
save_tmap(tm=bigmap,
          filename='test_map.png',
          insets_tm=auckland_elev,
          insets_vp=auckland_vp)

## Map saved to D:\Labou\Misc\R_working_group\test_map.png

## Resolution: 2100 by 2100 pixels

## Size: 6.999999 by 6.999999 inches (300 dpi)
```

# interactive maps!

See the [tmap vignette](https://cran.r-project.org/web/packages/tmap/vignettes/tmap-modes.html) or the [mapview vignettes](https://r-spatial.github.io/mapview/articles/index.html). mapview probably has more interactive features and supports more object types.

# for ggplot purists

If you don't know ggplot already, stick with `tmap` to begin with. if you are a ggplot enthusiast, you should know that the development version of ggplot has a new geom - `geom_sf` - that will make map making easier and more robust!

you can install the development ggplot with:

```r
# geom_sf still in ggplot dev. will need to install devtools from cran first
install.packages('devtools')
devtools::install_github("tidyverse/ggplot2")
library(ggplot2)
```

## simple example with geom_sf

```r
ggplot()+
  geom_sf(data=nz,aes(fill=REGC2017_NAME))+
  coord_sf() #handles projections!
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-14-1.png)

## the old way

what a mess, especially if you want the data and spatial info in your dataframe! for more, see the [CU Earth Lab tutorial](https://earthdatascience.org/courses/earth-analytics/spatial-data-r/make-maps-with-ggplot-in-R/)

```r
# polygons require a trip through 'sp', and then a join to get your data back
nz.sp <- as(nz,'Spatial')

nz.df <- broom::tidy(nz.sp,region='REGC2017') %>%
  full_join(nz.sp@data ,by=c('id'='REGC2017'))

## Warning: Column `id`/`REGC2017` joining character vector and factor,
## coercing into character vector

ggplot()+
  geom_polygon(data=nz.df,aes(x=long,y=lat,group=group,fill=REGC2017_NAME))+
  coord_fixed(ratio = 1) #you need to make sure things are in the right projection
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-15-1.png)

```r
nz_elev_df <- raster::as.data.frame(nz_elev,xy=T)

ggplot()+
  geom_raster(data=nz_elev_df,aes(x=x,y=y,fill=elevation))+
  scale_fill_viridis_c()+
  geom_path(data=nz.df,aes(x=long,y=lat,group=group))+
  coord_fixed(ratio=1)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-16-13.png)

```r
# normally you can use ggsn package to add north arrow and scale bar but it's not working well right now, maybe because I'm using the dev ggplot
```

## inset maps and multiple plots side by side - cowplot

If you use ggplot, you need to learn [cowplot](https://cran.r-project.org/web/packages/cowplot/index.html). Your life will be exponentially improved.
We can use the cowplot package to place multiple ggplot figures next to each other or within each other.

Here is a basic example of cowplot's capabilities. Obviously the formatting and legend need some work, but hopefully you get the idea!

```r
# get some data from maps
usa <- st_as_sf(maps::map('state',plot=F, fill=T))
counties <- sf::st_as_sf(maps::map(database='county',regions='idaho',fill=TRUE,plot=F))

# plot the counties of Idaho
gidaho <-
  ggplot(counties)+
  geom_sf(aes(fill=ID),show.legend = F)
# gidaho

# create a ggplot of usa
overview <-
  ggplot(usa)+
  geom_sf(fill=NA)+
  geom_sf(data=counties,fill='grey20')+
  # blank()+
  theme(axis.line=element_blank(),
        plot.margin= unit(c(0,0,0,0),'npc'))
# overview

# combine the two ggplot objects, with the overview map of the usa as an inset
cowplot::ggdraw(gidaho)+
  cowplot::draw_plot(overview,0.5,0.5,.2,.2,scale=1)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-17-13.png)

```r
# combine the two ggplot objects by placing them side by side
cowplot::plot_grid(gidaho,overview)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-17-2.png)

# Miscellaneous

There are many other ways to create maps in R, but I recommend becoming proficient in 1 rather than jumping around.

The one other exciting tool is `ggmap` - which will download background maps from google maps, stamen, open street map. This does not work easily with `tmap`. Theoretically it works well with `ggplot` but there are still some issues to be worked out with the new dev version.

If you want to give `ggmap` a go with the pre-geom_sf ggplot (v2.2.1), check out this [tutorial](http://mazamascience.com/WorkingWithData/?p=1494).

`tmap` can currently only download background maps in interactive "view" mode (v2 will support basemaps in "plot" mode, which you can try out by installing the development version directly from github). `dismo::gmap` and `Rgooglmaps` may provide options for static plots on background maps.

If you are using interactive maps, check out these (background maps)[<https://leaflet-extras.github.io/leaflet-providers/preview/>] that you can use with tmap in view mode.

## quick example with `dismo::gmap` and `tmap`

```r
# dismo::gmap returns a raster with projection string so you can use it with tmap
library(dismo)

## Warning: package 'dismo' was built under R version 3.4.4

## Loading required package: raster

## Loading required package: sp

## Warning: package 'sp' was built under R version 3.4.4

##
## Attaching package: 'raster'

## The following object is masked from 'package:dplyr':
##
##     select

## The following object is masked from 'package:tidyr':
##
##     extract

## The following object is masked from 'package:ggplot2':
##
##     calc

id2 <- dismo::gmap('idaho',type='roadmap',lonlat = T)

# use the builtin maps package to download counties of Idaho
counties <- sf::st_as_sf(maps::map(database='county',regions='idaho',fill=TRUE,plot=F))

tmap_mode('plot')

## tmap mode set to plotting

tm_shape(id2,
         bbox = tmaptools::bb(counties))+
  tm_raster()+
  tm_shape(counties)+
  tm_borders(alpha=0.5)
```

![](http://cougrstats.files.wordpress.com/2018/04/unnamed-chunk-18-12.png)

# Additional Resources

<http://neondataskills.org/R/>

<http://science.nature.nps.gov/im/datamgmt/statistics/r/advanced/spatial.cfm>

<https://pakillo.github.io/R-GIS-tutorial/>

<http://stackoverflow.com/questions/20256538/plot-raster-with-discrete-colors-using-rastervis>

<http://www.nickeubank.com/gis-in-r/>

<http://moc.environmentalinformatics-marburg.de/doku.php?id=courses:msc:advanced-gis:description>

<https://ropensci.org/packages/>

<https://ropensci.org/tutorials/>

<https://geocompr.robinlovelace.net/>

<https://eriqande.github.io/rep-res-web/lectures/making-maps-with-R.html>

<https://ryanpeek.github.io/>

<https://earthdatascience.org/courses/earth-analytics/spatial-data-r/make-maps-with-ggplot-in-R/>

<http://mazamascience.com/WorkingWithData/?p=1494>
