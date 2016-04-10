# -*- coding: utf-8 -*-
from math import ceil
import sys
import matplotlib.pyplot as plt
from datetime import datetime

import numpy as np
import matplotlib.gridspec as gridspec
from colormap.parula import test_cm

# Some constants
GREEN = [0.06666666, 0.7333333,0.2666666]
YELLOW = [1.0, 0.733333333333, 0.0]
RED = [0.93333333, 0.26666, 0.26666]
BLUE = [0.26666666, 0.5333333, 1.0]

MIN_YEAR = 1997
MAX_YEAR=2015
SCALE_MAX=37
SCALE_MIN=0

def read_and_render(csv_filename, ax, ax2):
    data_file = open (csv_filename)

    season_means = ([0,0,0,RED], [0,0,0,BLUE], [0,0,0,GREEN], [0,0,0,YELLOW])
    grid=np.empty((367, MAX_YEAR-MIN_YEAR + 1))

    grid[:] = np.NaN
    temperatures=[]
    humidities=[]
    COLORS=[]

    for csv_line in data_file:
        if csv_line.strip() == "":
            continue
        sample = csv_line.strip("\n").split(",")
        if sample[2] == "":
            continue

        graph_title = csv_filename.strip(".csv").replace("_", " ")
        dint = map(int, sample[0].split("-")) # parse the date
        t = datetime(dint[0], dint[1], dint[2])
        day_of_year = t.timetuple().tm_yday

        temp_f = float(sample[2])
        temp_c = (temp_f - 32.0)*5.0/9.0
        temp=temp_c

        if dint[0] >= MIN_YEAR and dint[0] <= MAX_YEAR:
            grid[ day_of_year -1 ,  dint[0] - MIN_YEAR] = temp

        if sample[8] == "": # Temp data but not humidity
            continue

        humid = float(sample[8])
        temperatures.append(temp)
        humidities.append(humid)

        # Collect season data
        season_months = ([3,4,5], [6,7,8], [9,10,11],[12,1,2])
        season_colors = [RED, BLUE, GREEN, YELLOW] # autumn, winter, spring, summer
        for index, season_range in enumerate(season_months):
            if dint[1] in season_range:
                COLORS.append(season_colors[index])
                season_means[index][0]+=1
                season_means[index][1]+=temp
                season_means[index][2]+=humid

    if len(temperatures) == 0: # No data in the file
        return

    def rand_jitter(arr):
        stdev = .015*(max(arr) - min(arr))
        return arr + np.random.randn(len(arr)) * stdev

    # Jitter the data since we only have integer values - leads to aliasing
    temperatures_jitter = rand_jitter(temperatures)
    humidities_jitter = rand_jitter(humidities)

    # Render the images
    plt.figure("Temperature/Humidity")
    ax.grid(b=True, which="major", color="k", linestyle="-", alpha=0.3)
    ax.set_axis_bgcolor((0.95, 0.95, 0.95))
    ax.set_title(graph_title)

    ax.scatter(temperatures_jitter, humidities_jitter,color=COLORS, alpha=0.3, s =10, marker=".")
    ax.set_xlim(SCALE_MIN,SCALE_MAX)
    ax.set_ylim(0,100)

    season_plots = []
    for s in season_means: # Render the season mean points
        n, s_temp, s_humid, colour = s
        s_plot = ax.scatter([s_temp/n], [s_humid/n], s= 40, marker="o", facecolors=[colour], edgecolors="black", label="pppppppppp")
        season_plots.append(s_plot)

    H, xedges, yedges = np.histogram2d(humidities_jitter, temperatures_jitter)
    extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
    ax.contour(H,  origin="lower",colors=["black"],linewidths=[1.1],extent=extent, alpha=0.15)

    plt.figure("Temperature")
    ax2.set_title(graph_title)
    masked_array = np.ma.array (grid, mask=np.isnan(grid))
    test_cm.set_bad(color=(0.8,0.8,0.8))
    ticks = np.arange(MIN_YEAR, MAX_YEAR, 4)
    last_im = ax2.imshow(masked_array, extent=(MIN_YEAR, MAX_YEAR - 1, 12, 1),
            interpolation="nearest", cmap=test_cm, vmin=SCALE_MIN, vmax=SCALE_MAX )
    ax2.set_xticks(ticks)

    return last_im, season_plots # Need these for legends

def remove_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

def setup_labels_axes(fig1, fig2, im, season_plots):
    fig1.text(0.5, 0.02, u"Temperature °C", ha="center", va="center")
    fig1.text(0.02, 0.5, "Humidity %", ha="center", va="center", rotation="vertical")
    fig2.text(0.02, 0.5, "Month", ha="center", va="center", rotation="vertical")

    cbar_ax = fig2.add_axes([0.97, 0.35, 0.01, 0.4])
    fig2.colorbar(im, cax=cbar_ax,label=u"Temperature °C")
    fig1.legend(season_plots,   ["Autumn", "Winter", "Spring", "Summer"], "right" )


if __name__== "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [csv1] [csv2] [csv3] ..." % sys.argv[0]
        sys.exit(0)
    filenames = sys.argv[1:]

    N_COLUMNS = min(4, len(filenames))
    N_ROWS = int(ceil(len(filenames) / float(N_COLUMNS)))

    fig1 = plt.figure("Temperature/Humidity")
    fig2 = plt.figure("Temperature")

    fig1.patch.set_facecolor((0.9,0.9,0.9))
    fig2.patch.set_facecolor((0.9,0.9,0.9))

    gs1 = gridspec.GridSpec(N_ROWS, N_COLUMNS, wspace=0.05, hspace=0.25, left=0.05, bottom=0.07, right=0.90, top=0.95)
    gs2 = gridspec.GridSpec(N_ROWS, N_COLUMNS, wspace=0.05, hspace=0.25, left=0.05, bottom=0.05, right=0.96, top=0.95)

    for i,filename in enumerate(filenames):
        j,k = i/N_COLUMNS, i%N_COLUMNS
        print "Rendering ",filename ," at position" ,j ,k
        gsi1 = gs1[j, k]
        gsi2 = gs2[j, k]

        fig1 = plt.figure("Temperature/Humidity")
        ax = plt.subplot(gsi1)
        fig2 = plt.figure("Temperature")
        ax2 = plt.subplot(gsi2)

        remove_spines(ax)

        # Read the data and render the graphs
        last_im, splots = read_and_render(filename, ax, ax2)

        # Some logic to control where we display the axis labels
        if k!=0:
            plt.setp(ax.get_yticklabels(), visible=False)
            plt.setp(ax2.get_yticklabels(), visible=False)
        if i< len(filenames) - N_COLUMNS:
            plt.setp(ax.get_xticklabels(), visible=False)
            plt.setp(ax2.get_xticklabels(), visible=False)

    setup_labels_axes(fig1, fig2, last_im, splots)

    # Save images of plots
    fig1.set_size_inches(16, 8, forward=True)
    fig1.savefig("temp_humid.png", dpi=100, facecolor=(0.92,0.92,0.92))

    fig2.set_size_inches(16.5, 9, forward=True)
    fig2.savefig("year_temp.png", dpi=150, facecolor=(1.0,1.0,1.0))

    plt.show()
