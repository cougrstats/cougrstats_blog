---
title: Raster analyses in R
author: Alli Cramer
date: '2019-01-30'
categories:
  - Research Profiles
tags:
  - gis
  - mapping
  - ncdf
  - raster
slug: raster-analyses-in-r
---

_By Alli Cramer_

## Spatial analysis in R

For one of my primary experiences of spatial analysis in R, we used a number of existing data bases to determine the average yearly temperature and precipitation for over _1.3 million_ lakes. One of my duties in this project was to combine multiple raster layers from a reanalysis of satellite data (From MERRA2, for all you climate nerds) to determine the average values. We then re-sampled the grids to match the spatial resolution of some lake data.

The data is WAY to big to use in this example, so we will first be generating some ncdf files which we will use. Then we will be doing some calculations between the rasters, and mapping them.

If you you like to learn more about spatial calculations in R in general, I recommend this website: https://rspatial.org/spatial/rst/sphere/sphere/index.html

If you would like to learn more specifics about mapping, we have a great mapping tutorial on this blog here: https://cougrstats.netlify.app/post/mapping-in-r/

## Libraries you will need

```r
library(ncdf4)
library(raster)
library(rasterVis)
library(maptools)
library(maps)
library(gridExtra)
```

## Our For Fun data

_This section is long, just scroll past it if you want to get to the "how" and not the "fake data" bit._

Our for fun data are NetCDF files. NetCDFs are very compact, easily machine read file formats that are frequently used to store large data sets. Most of the climate, oceanographic, or population spatial data from governmental sources are in this format, so it is useful to be exposed to it. They are, however, a bit difficult to read for humans. One way to easily view a netCDF file, and all of the subsequent layers and metadata, is with [Panoply](https://www.giss.nasa.gov/tools/panoply/), a free viewer from NOAA.

We will not be discussing the format of netCDF files, we will just be making two small ones to play with. A good discussion of netCDFs in R can be found at this University of Oregon [site](http://geog.uoregon.edu/GeogR/topics/netcdf-to-raster.html).

```r
library(ncdf4)
#code modified from http://geog.uoregon.edu/GeogR/topics/netcdf-to-raster.html

# create a small netCDF file, save, and read back in using raster and rasterVis
# generate lons and lats
nlon <- 24; nlat <- 9
dlon <- 360.0/nlon; dlat <- 180.0/nlat
lon <- seq(-180.0+(dlon/2),+180.0-(dlon/2),by=dlon)
lat <- seq(-90.0+(dlat/2),+90.0-(dlat/2),by=dlat)

# generate the first temperature data
set.seed(10) # for reproducibility
tmp1 <- rnorm(nlon*nlat)
tmat <- array(tmp1, dim = c(nlon, nlat))

# define dimensions
londim <- ncdim_def("lon", "degrees_east", as.double(lon))
latdim <- ncdim_def("lat", "degrees_north", as.double(lat))

# define variables
varname="tmp"
units="z-scores"
dlname <- "test variable -- original"
fillvalue <- 1e20
tmp.def <- ncvar_def(varname, units,
                    list(londim, latdim),
                    fillvalue,  dlname,
                    prec = "single")

# create a netCDF file
ncfname <- "test-netCDF-file_tmp1.nc"
ncout <- nc_create(ncfname, list(tmp.def), force_v4 = TRUE)

# put the array
ncvar_put(ncout, tmp.def, tmat)

# put additional attributes into dimension and data variables
ncatt_put(ncout, "lon", "axis", "X")
ncatt_put(ncout, "lat", "axis", "Y")

# add global attributes
title <- "small example netCDF file"
ncatt_put(ncout, 0, "title", title)

# close the file, writing data to disk
nc_close(ncout)

# generate the second temperature data
set.seed(12) # for reproducibility
tmp2 <- rnorm(nlon*nlat)
tmat <- array(tmp2, dim = c(nlon, nlat))

# define dimensions
londim <- ncdim_def("lon", "degrees_east", as.double(lon))
latdim <- ncdim_def("lat", "degrees_north", as.double(lat))

# define variables
varname="tmp"
units="z-scores"
dlname <- "test variable -- original"
fillvalue <- 1e20
tmp.def <- ncvar_def(varname, units,
                    list(londim, latdim),
                    fillvalue,  dlname,
                    prec = "single")

# create a netCDF file
ncfname <- "test-netCDF-file_tmp2.nc"
ncout <- nc_create(ncfname, list(tmp.def), force_v4 = TRUE)

# put the array
ncvar_put(ncout, tmp.def, tmat)

# put additional attributes into dimension and data variables
ncatt_put(ncout, "lon", "axis", "X")
ncatt_put(ncout, "lat", "axis", "Y")

# add global attributes
title <- "small example netCDF file"
ncatt_put(ncout, 0, "title", title)

# close the file, writing data to disk
nc_close(ncout)
```

# Rasters

First, what is a raster?

A raster is a type of data structure which exists in an array. Rasters are analogous to digital photos - every grid cell, or pixel, has a value. In a photo that value is a color. For rasters, that value can be a variety of things - temperature, population, etc.

Rasters are useful when doing spatial analyses because programs that understand rasters can perform calculations on the same grid cell by default - aka when using a raster programs "know" that you want calculations performed on a cell by cell basis. Otherwise, we have to write loops etc. to explicitly tell the computer that "hey, I want cell b5 to be subtracted from b5, and cell b6 to be subtracted from b6,..." and so on. If you do NOT want this type of cell to cell math, then a raster might not be for you. But if you DO, they can be a life saver.

## Raster calculations

One of the primary uses for rasters is to compare one set of spatial data to another. For example, we can compare temperature vs precipitation, or the elevation of an area vs it's slope. You may have used GIS to do this before, and the benefit of the GIS framework is that it double checks many of your steps. It is, however, slow.

**When using rasters in R make sure to double check your**

  * projection
  * dimensions
  * expected values

**Before doing any calculations**

## Our for fun data

Our for fun data is ncdf data. Ncdf files are different file formats from raster, but they can be READ as rasters by the raster package in R. Lets explore our ncdf and one of our raster files.

```r
#reading in the raster
library(raster)
library(rasterVis)
library(maptools)
library(maps)

T1.nc <- nc_open("test-netCDF-file_tmp1.nc")
T1.nc

## File test-netCDF-file_tmp1.nc (NC_FORMAT_NETCDF4):
##
##      1 variables (excluding dimension variables):
##         float tmp[lon,lat]   (Contiguous storage)
##             units: z-scores
##             _FillValue: 1.00000002004088e+20
##             long_name: test variable -- original
##
##      2 dimensions:
##         lon  Size:24
##             units: degrees_east
##             long_name: lon
##             axis: X
##         lat  Size:9
##             units: degrees_north
##             long_name: lat
##             axis: Y
##
##     1 global attributes:
##         title: small example netCDF file

nc_close(T1.nc)

T1 <- raster("test-netCDF-file_tmp1.nc")
T2<- raster("test-netCDF-file_tmp2.nc")  # we aren't going to look at this, but lets bring it in to save for later
T1

## class       : RasterLayer
## dimensions  : 9, 24, 216  (nrow, ncol, ncell)
## resolution  : 15, 20  (x, y)
## extent      : -180, 180, -90, 90  (xmin, xmax, ymin, ymax)
## coord. ref. : +proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0
## data source : C:\Users\allison.cramer\OneDrive\Teaching\R Working Group\WriteUps\test-netCDF-file_tmp1.nc
## names       : test.variable....original
## zvar        : tmp

print(T1)

## File C:\Users\allison.cramer\OneDrive\Teaching\R Working Group\WriteUps\test-netCDF-file_tmp1.nc (NC_FORMAT_NETCDF4):
##
##      1 variables (excluding dimension variables):
##         float tmp[lon,lat]   (Contiguous storage)
##             units: z-scores
##             _FillValue: 1.00000002004088e+20
##             long_name: test variable -- original
##
##      2 dimensions:
##         lon  Size:24
##             units: degrees_east
##             long_name: lon
##             axis: X
##         lat  Size:9
##             units: degrees_north
##             long_name: lat
##             axis: Y
##
##     1 global attributes:
##         title: small example netCDF file
```

As you can see, the data is stored differently between the ncdf and the raster. However, by comparing the two files you can see that the raster package, with the raster() function, opened the ncdf correctly and interpreted it right. We can now move on to mapping our raster file.

```r
# map the data
world.outlines <- map("world", plot=FALSE)
world.outlines.sp <- map2SpatialLines(world.outlines, proj4string = CRS("+proj=longlat"))

mapTheme <- rasterTheme(region = rev(brewer.pal(10, "RdBu")))
cutpts <- c(-2.5, -2.0, -1.5, -1, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5)
plt <- levelplot(T1, margin = F, at=cutpts, cuts=11, pretty=TRUE, par.settings = mapTheme,
  main="temperature variable -- as raster layer")
plt + layer(sp.lines(world.outlines.sp, col = "black", lwd = 0.5))
```

![](http://cougrstats.files.wordpress.com/2019/01/unnamed-chunk-37-1.png)

## Raster Brick and Raster Stack

Often, rasters have multiple layers, or "bands". To open a multi-band raster we use the brick() function from the raster package.

But what if we want to open multiple rasters and then do some calculations? Say ... average temperature?

For this, we use the stack() function. A raster stack is less efficient than a brick, so if doing large computations it can be efficient to use stack to then create bricks, and then do calculations. Lets try getting average temperature from our two ncdf files.

```r
#look for the .nc files in the directory
ncs <- list.files(getwd(), pattern = "*.nc$")

#create a raster stack from the files
stacked <- raster::stack(ncs)

#lets do some math!

#calculate mean temperature for every grid cell in the raster, between the two layers
Tmean <- mean(stacked)

#Lets check it
Tmean

## class       : RasterLayer
## dimensions  : 9, 24, 216  (nrow, ncol, ncell)
## resolution  : 15, 20  (x, y)
## extent      : -180, 180, -90, 90  (xmin, xmax, ymin, ymax)
## coord. ref. : +proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0
## data source : in memory
## names       : layer
## values      : -1.427061, 2.079051  (min, max)

#save this new calculated raster as a GeoTiff
writeRaster(Tmean, filename = "test-GTiff-file_TmpMean.tif", format="GTiff", overwrite = TRUE)
```

## Comparing the Data

```r
T1

## class       : RasterLayer
## dimensions  : 9, 24, 216  (nrow, ncol, ncell)
## resolution  : 15, 20  (x, y)
## extent      : -180, 180, -90, 90  (xmin, xmax, ymin, ymax)
## coord. ref. : +proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0
## data source : C:\Users\allison.cramer\OneDrive\Teaching\R Working Group\WriteUps\test-netCDF-file_tmp1.nc
## names       : test.variable....original
## zvar        : tmp

T2

## class       : RasterLayer
## dimensions  : 9, 24, 216  (nrow, ncol, ncell)
## resolution  : 15, 20  (x, y)
## extent      : -180, 180, -90, 90  (xmin, xmax, ymin, ymax)
## coord. ref. : +proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0
## data source : C:\Users\allison.cramer\OneDrive\Teaching\R Working Group\WriteUps\test-netCDF-file_tmp2.nc
## names       : test.variable....original
## zvar        : tmp

Tmean

## class       : RasterLayer
## dimensions  : 9, 24, 216  (nrow, ncol, ncell)
## resolution  : 15, 20  (x, y)
## extent      : -180, 180, -90, 90  (xmin, xmax, ymin, ymax)
## coord. ref. : +proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0
## data source : in memory
## names       : layer
## values      : -1.427061, 2.079051  (min, max)

# Setting up the maps
world.outlines <- map("world", plot=FALSE)
world.outlines.sp <- map2SpatialLines(world.outlines, proj4string = CRS("+proj=longlat"))

mapTheme <- rasterTheme(region = rev(brewer.pal(10, "RdBu")))
cutpts <- c(-2.5, -2.0, -1.5, -1, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5)

#T1 plot
plt_1 <- levelplot(T1, margin = F, at=cutpts, cuts=11, pretty=TRUE, par.settings = mapTheme,
  main="T1 -- as raster layer")

#T2 plot
plt_2 <- levelplot(T2, margin = F, at=cutpts, cuts=11, pretty=TRUE, par.settings = mapTheme,
  main="T2 -- as raster layer")

#Tmean plot
plt_m <- levelplot(Tmean, margin = F, at=cutpts, cuts=11, pretty=TRUE, par.settings = mapTheme,
  main="Tmean -- as raster layer")

#Actual plots
library(gridExtra) #to put our plots all next to each other all fancy

p1 <- plt_1 + layer(sp.lines(world.outlines.sp, col = "black", lwd = 0.5))
p2 <- plt_2 + layer(sp.lines(world.outlines.sp, col = "black", lwd = 0.5))
pm <- plt_m + layer(sp.lines(world.outlines.sp, col = "black", lwd = 0.5))

grid.arrange(
  arrangeGrob(p1, p2, ncol = 2),  #put plots p1 & p2 next to each other on the same row, in 2 columns (ncol=columns)
  pm, nrow = 2, #put pm on the next row, out of two rows (nrow=rows)
  heights = c(1,1.5)) #make the second row larger (here it is 1.5)
```

![](http://cougrstats.files.wordpress.com/2019/01/unnamed-chunk-39-1.png)
