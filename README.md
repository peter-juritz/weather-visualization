Intro
-----
After seeing [some great weather visualizations](https://www.reddit.com/r/dataisbeautiful/comments/41ooi6/the_daily_temperature_and_humidity_profiles_for/), I was curious to see how these would look for a few cities in South Africa. Decided to do this with python and matplotlib - as I’m more familiar with these tools.

Currently the code produces two types of graphs. The first one shows the average temperature each day for a number of years. The days progress downwards on the Y axis and years progress along the X axis. This gives a good overview of a city’s climate throughout the year.

![Temperature](https://raw.githubusercontent.com/peter-juritz/weather-visualization/master/images/year_temp.png)
The second type is a temperature humidity scatter plot. Each point is colored by it’s season and the mean values for each season are also shown. I found this visualization quite interesting due to the different types of geometries which the plot produces.

![Temperature-Humidity](https://raw.githubusercontent.com/peter-juritz/weather-visualization/master/images/temp_humid.png)

Usage
-----
To download weather data for cities:
```
python download_data.py datasource1 datasource2 ...
```
Datasource can be either an ICAO airport code or a WMO station id.
This data will then be saved as CSV files.
The csv files can then be plotted with:
```
python plot.py data1.csv data2.csv data3.csv
```


Some interesting things
----------------------
* Weather data was way harder to get hold of than I expected. I was hoping to get about a century worth of data. Some places offered this, but not for free. The data is often quite full of missing samples - as you can see in the graphs. In the end I got about 20 years of data at most for certain cities. Most data comes from airports with the remainder coming from WMO stations.
* I decided to not use the default colormap for my matplotlib version (1.3.1) and instead used the parula colormap from BIDS. They’ve done some interesting work on colormaps - one of which will be the new default version in matplotlib 2.0. More info [here](https://bids.github.io/colormap/).
* As the data downloaded had integer resolution for temperature, i had to jitter it slightly to remove the aliasing eggects - looked like a series of stripes in the scatterplot. Furthermore when I downloaded the data in celsius units there were some weird artefacts (far too few values reading 15 C) which disappeared when using farenheight. 
