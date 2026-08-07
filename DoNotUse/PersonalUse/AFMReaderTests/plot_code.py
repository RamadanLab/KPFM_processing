# Plotting functions
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
import os 
from pathlib import Path


def hex_to_RGB(hex_str):
    
    """ #FFFFFF -> [255,255,255]"""
    
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(n, c1= None, c2 = None):
    #Add automated if no colours given
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]


def plot_gaussian(x, y, x_fit, 
                  x_left = None, x_right = None, 
                  save_path = None, color = None,
                  measurement = '', scale = ''):

    # Add if statements if no spread given.  
    if scale == 'V': 
        x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
        x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
    elif scale == "mV": 
        x=x
        x_fit = x_fit
    else: 
        print("Please correct scale input to either V or mV")

    if color: 
        color = color
    else: 
        color = 'red'

    # All plotting parameters: 
    dpi_setting = 600
    figsize_x, figsize_y = (2227/dpi_setting), (1498/dpi)
    fig, ax = plt.subplots(1, 1, sharey=True, figsize=(figsize_x, figsize_y))

    ax.margins (0.5,0.5) 
    tick_length = 6
    legend_font = 12
    base_font_size = 12
    scatter_size = 6
    line_width = 1.5
    ax = plt.gca()

    # Tick editing
    ax.tick_params(direction='in', axis = 'both', length=tick_length, labelsize = base_font_size)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))  # Max 5 ticks on x-axis
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))  # Max 5 ticks on y-axis
    ax.autoscale(enable=None, axis="x", tight=True)
    

def waterfall_gaussian(x, y, x_fit, 
                       save_path = None, 
                       c1 = None, c2 = None, 
                       scale = '', measurement = ''): 
    # Add if statements for save path as normal
    # Add automation if no colours are given
    if scale == 'V': 
            x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
            x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
    elif scale == "mV": 
        x=x
        x_fit = x_fit
    else: 
        print("Please correct scale input to either V or mV")

def time_series_plot(x, y, 
                     x_left = None, x_right = None, 
                     cuttoff_line1 = None, cutoff_line2 = None, 
                     save_path = None, 
                     color = None,
                     measurement = '', scale = ''): 
    # need to add: 
    # If statement for the spread
    #if statement for if there is a light on/light off time
    # Add standard if statement for save_path
    # Add error if no measurement.
    if scale == 'V': 
        x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
        x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
    elif scale == "mV": 
        x=x
        x_fit = x_fit
    else: 
        print("Please correct scale input to either V or mV")

def stretched_exp_plot (x, y, x_fit, y_fit = None, 
                        save_path = None, 
                        color = None, 
                        measurement = '', scale = '',): 
        # need to add: 
    # If statement for the spread
    # Add standard if statement for save_path
    # Add error if no measurement.
    if scale == 'V': 
        x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
        x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
    elif scale == "mV": 
        x=x
        x_fit = x_fit
    else: 
        print("Please correct scale input to either V or mV")

def compare_gaussians(x1, y1, x_fit1, 
                    x2, y2, x_fit2,
                  save_path = None, 
                  measurement = '', scale = ''): 
    if scale == 'V': 
        x1 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x1]
        x_fit1 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit1]
        x2 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x2]
        x_fit2 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit2]
    elif scale == "mV": 
        x1=x1
        x_fit1 = x_fit1
        x2=x2
        x_fit2 = x_fit2
    else: 
        print("Please correct scale input to either V or mV")
