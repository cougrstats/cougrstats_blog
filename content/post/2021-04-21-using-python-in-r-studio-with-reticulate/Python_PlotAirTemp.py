import xarray as xr
import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs


def PlotAirTemp(usertime):
    """ Plot air temperature
    
    Args:
        username (str): "yyyy-mm-dd hh:mm:ss" 
                (for example '2013-04-14 00:00:00')
    """
    
    air_temperature = xr.tutorial.open_dataset("air_temperature.nc")
    
    fig = plt.figure(figsize = (15,5))
    ax = plt.axes(projection = ccrs.PlateCarree())
    ax.set_extent([-125, -66.5, 20, 50])
    ax.coastlines()
    ax.gridlines(draw_labels=True)
    plot = air_temperature.air.sel(time=usertime).plot(ax = ax, transform = ccrs.PlateCarree())
    ax.set_title('Air Temperature\n' + usertime)
    ax.add_feature(cartopy.feature.STATES)
    plt.show()
